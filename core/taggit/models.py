import django
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.db import models, IntegrityError, transaction
from django.template.defaultfilters import slugify as default_slugify
from django.utils.translation import ugettext_lazy as _, ugettext
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse


class TagBase(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=150)
    slug = models.SlugField(
        verbose_name=_('Slug'), unique=True, max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True

    def taggers(self, category_slug, object_id, content_type):
        users = []
        for user in get_user_model().objects.filter(
                taggit_taggeditem_related__tag_category__slug=category_slug,
                taggit_taggeditem_related__tag__slug=self.slug,
                taggit_taggeditem_related__object_id=object_id,
                taggit_taggeditem_related__content_type__name=content_type):
            try:
                user.get_profile()
                users.append(user)
            except ObjectDoesNotExist:
                pass

        return users

    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:
            self.slug = self.slugify(self.name)
            from django.db import router
            using = kwargs.get("using") or router.db_for_write(
                type(self), instance=self)
            # Make sure we write to the same db for all attempted writes,
            # with a multi-master setup, theoretically we could try to
            # write and rollback on different DBs
            kwargs["using"] = using
            trans_kwargs = {"using": using}

            i = 0
            while True:
                i += 1
                try:
                    sid = transaction.savepoint(**trans_kwargs)
                    res = super(TagBase, self).save(*args, **kwargs)
                    transaction.savepoint_commit(sid, **trans_kwargs)
                    return res
                except IntegrityError:
                    transaction.savepoint_rollback(sid, **trans_kwargs)
                    self.slug = self.slugify(self.name, i)
        else:
            return super(TagBase, self).save(*args, **kwargs)

    def slugify(self, tag, i=None):
        slug = default_slugify(tag)
        if i is not None:
            slug += "_%d" % i
        return slug


class Tag(TagBase):

    def get_absolute_url(self):
        return reverse('staff_directory:show_by_tag', args=(self.slug,))

    # Search fields
    @classmethod
    def search_category(cls):
        return 'Staff Directory'

    @property
    def to_search_result(self):
        return 'Tag: ' + self.name

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class ItemBase(models.Model):

    def __unicode__(self):
        return ugettext("%(object)s tagged with %(tag)s") % {
            "object": self.content_object,
            "tag": self.tag
        }

    class Meta:
        abstract = True

    @classmethod
    def tag_model(cls):
        return cls._meta.get_field_by_name("tag")[0].rel.to

    @classmethod
    def tag_relname(cls):
        return cls._meta.get_field_by_name('tag')[0].rel.related_name

    @classmethod
    def lookup_kwargs(cls, instance):
        return {
            'content_object': instance
        }

    @classmethod
    def bulk_lookup_kwargs(cls, instances):
        return {
            "content_object__in": instances,
        }


class TaggedItemBase(ItemBase):
    tag = models.ForeignKey(
        Tag, related_name="%(app_label)s_%(class)s_items")

    class Meta:
        abstract = True

    @classmethod
    def tags_for(cls, model, instance=None):
        if instance is not None:
            return cls.tag_model().objects.filter(**{
                '%s__content_object' % cls.tag_relname(): instance
            })
        return cls.tag_model().objects.filter(**{
            '%s__content_object__isnull' % cls.tag_relname(): False
        }).distinct()


class TagCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    def __unicode__(self):
        return u"%s" % self.name


class GenericTaggedItemBase(ItemBase):
    object_id = models.IntegerField(verbose_name=_('Object id'),
                                    db_index=True)
    tag_creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                    related_name='%(app_label)s_%(class)s_related')
    create_timestamp = models.DateTimeField(auto_now=True)
    tag_category = models.ForeignKey(TagCategory, null=True)
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_('Content type'),
        related_name="%(app_label)s_%(class)s_tagged_items")
    content_object = GenericForeignKey()

    class Meta:
        abstract = True

    @classmethod
    def lookup_kwargs(cls, instance):
        return {
            'object_id': instance.pk,
            'content_type': ContentType.objects.get_for_model(instance)
        }

    @classmethod
    def bulk_lookup_kwargs(cls, instances):
        # TODO: instances[0], can we assume there are instances.
        return {
            "object_id__in": [instance.pk for instance in instances],
            "content_type": ContentType.objects.get_for_model(instances[0]),
        }

    @classmethod
    def tags_for(cls, model, instance=None):
        ct = ContentType.objects.get_for_model(model)
        kwargs = {
            "%s__content_type" % cls.tag_relname(): ct
        }
        if instance is not None:
            kwargs["%s__object_id" % cls.tag_relname()] = instance.pk
        return cls.tag_model().objects.filter(**kwargs).distinct()


class TaggedItem(GenericTaggedItemBase, TaggedItemBase):

    class Meta:
        verbose_name = _("Tagged Item")
        verbose_name_plural = _("Tagged Items")
