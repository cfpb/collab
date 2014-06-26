from unittest import TestCase as UnitTestCase

import django
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import connection
from django.test import TestCase, TransactionTestCase
from django.test.utils import override_settings

from core.taggit.managers import TaggableManager
from core.taggit.models import Tag, TaggedItem, TagCategory
from .forms import (FoodForm, DirectFoodForm, CustomPKFoodForm,
                    OfficialFoodForm)
from .models import (Food, Pet, HousePet, DirectFood, DirectPet,
                     DirectHousePet, TaggedPet, CustomPKFood, CustomPKPet, CustomPKHousePet,
                     TaggedCustomPKPet, OfficialFood, OfficialPet, OfficialHousePet,
                     OfficialThroughModel, OfficialTag, Photo, Movie, Article)
from core.taggit.utils import parse_tags, edit_string_for_tags, add_tags
from django.contrib.auth import get_user_model
import random
import string


class BaseTaggingTest(object):

    def random_user(self):
        return get_user_model().objects.create_user(
            ''.join(random.choice(string.lowercase) for _ in range(12)))

    def random_tag_category(self):
        start = ''.join(random.choice(string.lowercase) for _ in range(12))
        end = ''.join(random.choice(string.lowercase) for _ in range(12))
        name = '%s %s' % (start, end)
        slug = '%s-%s' % (start, end)
        tag_category = TagCategory(name=name, slug=slug)
        tag_category.save()
        return tag_category

    def assert_tags_equal(self, qs, tags, sort=True, attr="name"):
        got = map(lambda tag: getattr(tag, attr), qs)
        if sort:
            got.sort()
            tags.sort()
        self.assertEqual(got, tags)

    def assert_tagged_items_equal(self, qs, tag_item_pairs):
        got = map(lambda ti: (ti.content_object.name, ti.tag.name), qs)
        self.assertEqual(got, tag_item_pairs)

    def assert_num_queries(self, n, f, *args, **kwargs):
        original_DEBUG = settings.DEBUG
        settings.DEBUG = True
        current = len(connection.queries)
        try:
            f(*args, **kwargs)
            self.assertEqual(
                len(connection.queries) - current,
                n,
            )
        finally:
            settings.DEBUG = original_DEBUG

    def _get_form_str(self, form_str):
        if django.VERSION >= (1, 3):
            form_str %= {
                "help_start": '<span class="helptext">',
                "help_stop": "</span>"
            }
        else:
            form_str %= {
                "help_start": "",
                "help_stop": ""
            }
        return form_str

    def assert_form_renders(self, form, html):
        self.assertEqual(str(form), self._get_form_str(html))


class BaseTaggingTestCase(TestCase, BaseTaggingTest):
    pass


class BaseTaggingTransactionTestCase(TransactionTestCase, BaseTaggingTest):
    pass


class TagModelTestCase(BaseTaggingTransactionTestCase):
    food_model = Food
    tag_model = Tag

    def test_unique_slug(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("Red", "red")

    def test_update(self):
        special = self.tag_model.objects.create(name="special")
        special.save()

    def test_add(self):
        apple = self.food_model.objects.create(name="apple")
        yummy = self.tag_model.objects.create(name="yummy")
        apple.tags.add(yummy)

    def test_slugify(self):
        a = Article.objects.create(title="django-taggit 1.0 Released")
        a.tags.add("awesome", "release", "AWESOME")
        self.assert_tags_equal(a.tags.all(), [
            "category-awesome",
            "category-release",
            "category-awesome-1"
        ], attr="slug")


class TagModelDirectTestCase(TagModelTestCase):
    food_model = DirectFood
    tag_model = Tag


class TagModelCustomPKTestCase(TagModelTestCase):
    food_model = CustomPKFood
    tag_model = Tag


class TagModelOfficialTestCase(TagModelTestCase):
    food_model = OfficialFood
    tag_model = OfficialTag


class TagUtilTestCase(BaseTaggingTestCase):

    def test_add_tags_util(self):
        food_model = Food
        apple = food_model.objects.create(name="apple")
        self.assertEqual(list(apple.tags.all()), [])
        self.assertEqual(list(food_model.tags.all()), [])

        user1 = self.random_user()
        category1 = self.random_tag_category()
        add_tags(apple, 'green', category1.slug, user1, 'food')
        self.assert_tags_equal(apple.tags.all(), ['green'])
        self.assert_tags_equal(food_model.tags.all(), ['green'])
        self.assert_tagged_items_equal(TaggedItem.objects.filter(content_type__name='food'),
                                       [('apple','green')])
        self.assert_tagged_items_equal(TaggedItem.objects.filter(tag_category=category1),
                                       [('apple','green')])
        self.assert_tagged_items_equal(TaggedItem.objects.filter(tag_creator=user1),
                                       [('apple','green')])

        # test null category
        user2 = self.random_user()
        add_tags(apple, 'yellow', None, user2, 'food')
        self.assert_tags_equal(apple.tags.all(), ['green', 'yellow'])
        self.assert_tags_equal(food_model.tags.all(), ['green', 'yellow'])
        self.assert_tagged_items_equal(TaggedItem.objects.filter(content_type__name='food'),
                                       [('apple','green'), ('apple','yellow')])
        self.assert_tagged_items_equal(TaggedItem.objects.filter(tag_category=None),
                                       [('apple','yellow')])
        self.assert_tagged_items_equal(TaggedItem.objects.filter(tag_creator=user2),
                                       [('apple','yellow')])

        # test null user
        category2 = self.random_tag_category()
        add_tags(apple, 'red', category2.slug, None, 'food')
        self.assert_tags_equal(apple.tags.all(), ['green', 'yellow', 'red'])
        self.assert_tags_equal(food_model.tags.all(), ['green', 'yellow', 'red'])
        self.assert_tagged_items_equal(TaggedItem.objects.filter(content_type__name='food'),
                                       [('apple','green'), ('apple','yellow'), ('apple','red')])
        self.assert_tagged_items_equal(TaggedItem.objects.filter(tag_category=category2),
                                       [('apple','red')])
        self.assert_tagged_items_equal(TaggedItem.objects.filter(tag_creator=None),
                                       [('apple','red')])

        # test null content_type
        self.assertRaises(IndexError, add_tags, apple, 'red', category2.slug, user2, 'bad_content_type')
        self.assertRaises(IndexError, add_tags, apple, 'red', category2.slug, user2, None)

    def test_add_tags_duplicate_tag(self):
        """
        add_tags function should only create a Tag if it doesn't already exist
        """
        food_model = Food
        apple = food_model.objects.create(name="apple")
        self.assertEqual(list(apple.tags.all()), [])
        self.assertEqual(list(food_model.tags.all()), [])

        user1 = self.random_user()
        category1 = self.random_tag_category()
        add_tags(apple, 'green', category1.slug, user1, 'food')
        self.assert_tags_equal(apple.tags.all(), ['green'])
        self.assert_tags_equal(food_model.tags.all(), ['green'])

        #  test exact duplicate
        add_tags(apple, 'green', category1.slug, user1, 'food')
        self.assert_tags_equal(apple.tags.all(), ['green'])
        self.assert_tags_equal(food_model.tags.all(), ['green'])

        #  test duplicate with different category/user/content_type
        user2 = self.random_user()
        category2 = self.random_tag_category()
        food_model2 = Pet
        food_model2.objects.create(name="apple")
        add_tags(apple, 'green', category2.slug, user2, 'pet')
        self.assert_tags_equal(apple.tags.all(), ['green'])
        self.assert_tags_equal(food_model.tags.all(), ['green'])

    def test_add_tags_new_taggeditem(self):
        """
        add_tags function should only create a Tag if it doesn't already exist
        """
        food_model = Food
        apple = food_model.objects.create(name="apple")
        self.assertEqual(list(apple.tags.all()), [])
        self.assertEqual(list(food_model.tags.all()), [])

        user1 = self.random_user()
        category1 = self.random_tag_category()
        add_tags(apple, 'green', category1.slug, user1, 'food')
        self.assert_tags_equal(apple.tags.all(), ['green'])
        self.assert_tags_equal(food_model.tags.all(), ['green'])

        #  test existing tag with different taggeditem
        orange = food_model.objects.create(name="orange")
        add_tags(orange, 'green', category1.slug, user1, 'food')
        self.assert_tags_equal(apple.tags.all(), ['green'])
        self.assert_tags_equal(orange.tags.all(), ['green'])
        self.assert_tags_equal(food_model.tags.all(), ['green'])
        self.assert_tagged_items_equal(TaggedItem.objects.filter(content_type__name='food'),
                                       [('apple','green'),('orange','green')])
        self.assert_tagged_items_equal(TaggedItem.objects.filter(tag_category=category1),
                                       [('apple','green'),('orange','green')])
        self.assert_tagged_items_equal(TaggedItem.objects.filter(tag_creator=user1),
                                       [('apple','green'),('orange','green')])

    def test_add_tags_duplicate_taggeditem(self):
        """
        add_tags function should only create a TaggedItem if it doesn't
        already exist
        """
        food_model = Food
        apple = food_model.objects.create(name="apple")
        self.assertEqual(list(apple.tags.all()), [])
        self.assertEqual(list(food_model.tags.all()), [])

        user1 = self.random_user()
        category1 = self.random_tag_category()
        add_tags(apple, 'green', category1.slug, user1, 'food')
        self.assert_tags_equal(apple.tags.all(), ['green'])
        self.assert_tags_equal(food_model.tags.all(), ['green'])
        self.assert_tagged_items_equal(TaggedItem.objects.filter(content_type__name='food'),
                                       [('apple','green')])
        self.assert_tagged_items_equal(TaggedItem.objects.filter(tag_category=category1),
                                       [('apple','green')])
        self.assert_tagged_items_equal(TaggedItem.objects.filter(tag_creator=user1),
                                       [('apple','green')])

        #  test exact duplicate
        add_tags(apple, 'green', category1.slug, user1, 'food')
        self.assert_tagged_items_equal(TaggedItem.objects.filter(content_type__name='food'),
                                       [('apple','green')])
        self.assert_tagged_items_equal(TaggedItem.objects.filter(tag_category=category1),
                                       [('apple','green')])
        self.assert_tagged_items_equal(TaggedItem.objects.filter(tag_creator=user1),
                                       [('apple','green')])

        #  test duplicate with different category
        category2 = self.random_tag_category()
        add_tags(apple, 'green', category2.slug, user1, 'food')
        self.assert_tagged_items_equal(TaggedItem.objects.filter(content_type__name='food'),
                                       [('apple','green'), ('apple','green')])
        self.assert_tagged_items_equal(TaggedItem.objects.filter(tag_category=category2),
                                       [('apple','green')])
        self.assert_tagged_items_equal(TaggedItem.objects.filter(tag_creator=user1),
                                       [('apple','green'),('apple','green')])

        #  test duplicate with different content_type
        food_model2 = Pet
        food_model2.objects.create(name="apple", id=apple.id)
        add_tags(apple, 'green', category2.slug, user1, 'pet')
        self.assert_tagged_items_equal(TaggedItem.objects.filter(content_type__name='pet'),
                                       [('apple','green')])
        self.assert_tagged_items_equal(TaggedItem.objects.filter(tag_category=category2),
                                       [('apple','green'),('apple','green')])
        self.assert_tagged_items_equal(TaggedItem.objects.filter(tag_creator=user1),
                                       [('apple','green'),('apple','green'),('apple','green')])

        #  test duplicate with different creator
        user2 = self.random_user()
        add_tags(apple, 'green', category2.slug, user2, 'food')
        self.assert_tagged_items_equal(TaggedItem.objects.filter(content_type__name='pet'),
                                       [('apple','green')])
        self.assert_tagged_items_equal(TaggedItem.objects.filter(tag_category=category2),
                                       [('apple','green'), ('apple','green')])
        self.assert_tagged_items_equal(TaggedItem.objects.filter(tag_creator=user2),
                                       [])
        #  ensure the old user didn't change either
        self.assert_tagged_items_equal(TaggedItem.objects.filter(tag_creator=user1),
                                       [('apple','green'),('apple','green'),('apple','green')])


class TaggableManagerTestCase(BaseTaggingTestCase):
    food_model = Food
    pet_model = Pet
    housepet_model = HousePet
    taggeditem_model = TaggedItem
    tag_model = Tag

    def test_add_tag(self):
        apple = self.food_model.objects.create(name="apple")
        self.assertEqual(list(apple.tags.all()), [])
        self.assertEqual(list(self.food_model.tags.all()), [])

        apple.tags.add('green')
        self.assert_tags_equal(apple.tags.all(), ['green'])
        self.assert_tags_equal(self.food_model.tags.all(), ['green'])

        pear = self.food_model.objects.create(name="pear")
        pear.tags.add('green')
        self.assert_tags_equal(pear.tags.all(), ['green'])
        self.assert_tags_equal(self.food_model.tags.all(), ['green'])

        apple.tags.add('red')
        self.assert_tags_equal(apple.tags.all(), ['green', 'red'])
        self.assert_tags_equal(self.food_model.tags.all(), ['green', 'red'])

        self.assert_tags_equal(
            self.food_model.tags.most_common(),
            ['green', 'red'],
            sort=False
        )

        apple.tags.remove('green')
        self.assert_tags_equal(apple.tags.all(), ['red'])
        self.assert_tags_equal(self.food_model.tags.all(), ['green', 'red'])
        tag = self.tag_model.objects.create(name="delicious")
        apple.tags.add(tag)
        self.assert_tags_equal(apple.tags.all(), ["red", "delicious"])

        apple.delete()
        self.assert_tags_equal(self.food_model.tags.all(), ["green"])

    @override_settings(TAGGIT_FORCE_LOWERCASE=False)
    def test_add_mixed_case_tags(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add('red')
        apple.tags.add('Marlene')
        self.assert_tags_equal(apple.tags.all(), ["red", "Marlene"])

    @override_settings(TAGGIT_FORCE_LOWERCASE=True)
    def test_add_mixed_case_tags_with_lowercase_forced(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add('red')
        apple.tags.add('Marlene')
        self.assert_tags_equal(apple.tags.all(), ["red", "marlene"])

    def test_require_pk(self):
        food_instance = self.food_model()
        self.assertRaises(ValueError, lambda: food_instance.tags.all())

    def test_delete_obj(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("red")
        self.assert_tags_equal(apple.tags.all(), ["red"])
        strawberry = self.food_model.objects.create(name="strawberry")
        strawberry.tags.add("red")
        apple.delete()
        self.assert_tags_equal(strawberry.tags.all(), ["red"])

    def test_delete_bulk(self):
        apple = self.food_model.objects.create(name="apple")
        kitty = self.pet_model.objects.create(pk=apple.pk, name="kitty")

        apple.tags.add("red", "delicious", "fruit")
        kitty.tags.add("feline")

        self.food_model.objects.all().delete()

        self.assert_tags_equal(kitty.tags.all(), ["feline"])

    def test_lookup_by_tag(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("red", "green")
        pear = self.food_model.objects.create(name="pear")
        pear.tags.add("green")

        self.assertEqual(
            list(self.food_model.objects.filter(tags__name__in=["red"])),
            [apple]
        )
        self.assertEqual(
            list(self.food_model.objects.filter(tags__name__in=["green"])),
            [apple, pear]
        )

        kitty = self.pet_model.objects.create(name="kitty")
        kitty.tags.add("fuzzy", "red")
        dog = self.pet_model.objects.create(name="dog")
        dog.tags.add("woof", "red")
        self.assertEqual(
            list(self.food_model.objects.filter(
                tags__name__in=["red"]).distinct()),
            [apple]
        )

        tag = self.tag_model.objects.get(name="woof")
        self.assertEqual(
            list(self.pet_model.objects.filter(tags__in=[tag])), [dog])

        cat = self.housepet_model.objects.create(name="cat", trained=True)
        cat.tags.add("fuzzy")

        self.assertEqual(
            map(lambda o: o.pk, self.pet_model.objects.filter(
                tags__name__in=["fuzzy"])).sort(),
            [kitty.pk, cat.pk].sort()
        )

    def test_exclude(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("red", "green", "delicious")

        pear = self.food_model.objects.create(name="pear")
        pear.tags.add("green", "delicious")

        guava = self.food_model.objects.create(name="guava")

        self.assertEqual(
            map(lambda o: o.pk, self.food_model.objects.exclude(
                tags__name__in=["red"])).sort(),
            [pear.pk, guava.pk].sort(),
        )

    def test_similarity_by_tag(self):
        """Test that pears are more similar to apples than watermelons"""
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("green", "juicy", "small", "sour")

        pear = self.food_model.objects.create(name="pear")
        pear.tags.add("green", "juicy", "small", "sweet")

        watermelon = self.food_model.objects.create(name="watermelon")
        watermelon.tags.add("green", "juicy", "large", "sweet")

        similar_objs = apple.tags.similar_objects()
        self.assertEqual(similar_objs, [pear, watermelon])
        self.assertEqual(map(lambda x: x.similar_tags, similar_objs), [3, 2])

    def test_tag_reuse(self):
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("juicy", "juicy")
        self.assert_tags_equal(apple.tags.all(), ['juicy'])

    def test_query_traverse(self):
        spot = self.pet_model.objects.create(name='Spot')
        spike = self.pet_model.objects.create(name='Spike')
        spot.tags.add('scary')
        spike.tags.add('fluffy')
        lookup_kwargs = {
            '%s__name' % self.pet_model._meta.module_name: 'Spot'
        }
        self.assert_tags_equal(
            self.tag_model.objects.filter(**lookup_kwargs),
            ['scary']
        )

    def test_taggeditem_unicode(self):
        ross = self.pet_model.objects.create(name="ross")
        # I keep Ross Perot for a pet, what's it to you?
        ross.tags.add("president")

        self.assertEqual(
            unicode(self.taggeditem_model.objects.all()[0]),
            "ross tagged with president"
        )

    def test_abstract_subclasses(self):
        p = Photo.objects.create()
        p.tags.add("outdoors", "pretty")
        self.assert_tags_equal(
            p.tags.all(),
            ["outdoors", "pretty"]
        )

        m = Movie.objects.create()
        m.tags.add("hd")
        self.assert_tags_equal(
            m.tags.all(),
            ["hd"],
        )


class TaggableManagerDirectTestCase(TaggableManagerTestCase):
    food_model = DirectFood
    pet_model = DirectPet
    housepet_model = DirectHousePet
    taggeditem_model = TaggedPet


class TaggableManagerCustomPKTestCase(TaggableManagerTestCase):
    food_model = CustomPKFood
    pet_model = CustomPKPet
    housepet_model = CustomPKHousePet
    taggeditem_model = TaggedCustomPKPet

    def test_require_pk(self):
        # TODO with a charfield pk, pk is never None, so taggit has no way to
        # tell if the instance is saved or not
        pass


class TaggableManagerOfficialTestCase(TaggableManagerTestCase):
    food_model = OfficialFood
    pet_model = OfficialPet
    housepet_model = OfficialHousePet
    taggeditem_model = OfficialThroughModel
    tag_model = OfficialTag

    def test_extra_fields(self):
        self.tag_model.objects.create(name="red")
        self.tag_model.objects.create(name="delicious", official=True)
        apple = self.food_model.objects.create(name="apple")
        apple.tags.add("delicious", "red")

        pear = self.food_model.objects.create(name="Pear")
        pear.tags.add("delicious")

        self.assertEqual(
            map(lambda o: o.pk, self.food_model.objects.filter(
                tags__official=False)),
            [apple.pk],
        )


class TaggableFormTestCase(BaseTaggingTestCase):
    form_class = FoodForm
    food_model = Food

    def test_form(self):
        self.assertEqual(self.form_class.base_fields.keys(), ['name', 'tags'])

        f = self.form_class({'name': 'apple', 'tags': 'green, red, yummy'})
        self.assert_form_renders(f, """<tr><th><label for="id_name">Name:</label></th><td><input id="id_name" maxlength="50" name="name" type="text" value="apple" /></td></tr>
<tr><th><label for="id_tags">Tags:</label></th><td><input id="id_tags" name="tags" type="text" value="green, red, yummy" /><br />%(help_start)sA comma-separated list of tags.%(help_stop)s</td></tr>""")
        f.save()
        apple = self.food_model.objects.get(name='apple')
        self.assert_tags_equal(apple.tags.all(), ['green', 'red', 'yummy'])

        f = self.form_class({'name': 'apple', 'tags':
                            'green, red, yummy, delicious'}, instance=apple)
        f.save()
        apple = self.food_model.objects.get(name='apple')
        self.assert_tags_equal(
            apple.tags.all(), ['green', 'red', 'yummy', 'delicious'])
        self.assertEqual(self.food_model.objects.count(), 1)

        f = self.form_class({"name": "raspberry"})
        self.assertFalse(f.is_valid())

        f = self.form_class(instance=apple)
        self.assert_form_renders(f, """<tr><th><label for="id_name">Name:</label></th><td><input id="id_name" maxlength="50" name="name" type="text" value="apple" /></td></tr>
<tr><th><label for="id_tags">Tags:</label></th><td><input id="id_tags" name="tags" type="text" value="delicious, green, red, yummy" /><br />%(help_start)sA comma-separated list of tags.%(help_stop)s</td></tr>""")

        apple.tags.add('has,comma')
        f = self.form_class(instance=apple)
        self.assert_form_renders(f, """<tr><th><label for="id_name">Name:</label></th><td><input id="id_name" maxlength="50" name="name" type="text" value="apple" /></td></tr>
<tr><th><label for="id_tags">Tags:</label></th><td><input id="id_tags" name="tags" type="text" value="&quot;has,comma&quot;, delicious, green, red, yummy" /><br />%(help_start)sA comma-separated list of tags.%(help_stop)s</td></tr>""")

        apple.tags.add('has space')
        f = self.form_class(instance=apple)
        self.assert_form_renders(f, """<tr><th><label for="id_name">Name:</label></th><td><input id="id_name" maxlength="50" name="name" type="text" value="apple" /></td></tr>
<tr><th><label for="id_tags">Tags:</label></th><td><input id="id_tags" name="tags" type="text" value="&quot;has space&quot;, &quot;has,comma&quot;, delicious, green, red, yummy" /><br />%(help_start)sA comma-separated list of tags.%(help_stop)s</td></tr>""")

    def test_formfield(self):
        tm = TaggableManager(verbose_name='categories',
                             help_text='Add some categories', blank=True)
        ff = tm.formfield()
        self.assertEqual(ff.label, 'Categories')
        self.assertEqual(ff.help_text, u'Add some categories')
        self.assertEqual(ff.required, False)

        self.assertEqual(ff.clean(""), [])

        tm = TaggableManager()
        ff = tm.formfield()
        self.assertRaises(ValidationError, ff.clean, "")


class TaggableFormDirectTestCase(TaggableFormTestCase):
    form_class = DirectFoodForm
    food_model = DirectFood


class TaggableFormCustomPKTestCase(TaggableFormTestCase):
    form_class = CustomPKFoodForm
    food_model = CustomPKFood


class TaggableFormOfficialTestCase(TaggableFormTestCase):
    form_class = OfficialFoodForm
    food_model = OfficialFood


class TagStringParseTestCase(UnitTestCase):

    """
    Ported from Jonathan Buchanan's `django-tagging
    <http://django-tagging.googlecode.com/>`_
    """

    def test_with_simple_space_delimited_tags(self):
        """
        Test with simple space-delimited tags.
        """
        self.assertEqual(parse_tags('one'), [u'one'])
        self.assertEqual(parse_tags('one two'), [u'one', u'two'])
        self.assertEqual(
            parse_tags('one two three'), [u'one', u'three', u'two'])
        self.assertEqual(parse_tags('one one two two'), [u'one', u'two'])

    def test_with_comma_delimited_multiple_words(self):
        """
        Test with comma-delimited multiple words.
        An unquoted comma in the input will trigger this.
        """
        self.assertEqual(parse_tags(',one'), [u'one'])
        self.assertEqual(parse_tags(',one two'), [u'one two'])
        self.assertEqual(parse_tags(',one two three'), [u'one two three'])
        self.assertEqual(parse_tags('a-one, a-two and a-three'),
                         [u'a-one', u'a-two and a-three'])

    def test_with_double_quoted_multiple_words(self):
        """
        Test with double-quoted multiple words.
        A completed quote will trigger this.  Unclosed quotes are ignored.
        """
        self.assertEqual(parse_tags('"one'), [u'one'])
        self.assertEqual(parse_tags('"one two'), [u'one', u'two'])
        self.assertEqual(
            parse_tags('"one two three'), [u'one', u'three', u'two'])
        self.assertEqual(parse_tags('"one two"'), [u'one two'])
        self.assertEqual(parse_tags('a-one "a-two and a-three"'),
                         [u'a-one', u'a-two and a-three'])

    def test_with_no_loose_commas(self):
        """
        Test with no loose commas -- split on spaces.
        """
        self.assertEqual(
            parse_tags('one two "thr,ee"'), [u'one', u'thr,ee', u'two'])

    def test_with_loose_commas(self):
        """
        Loose commas - split on commas
        """
        self.assertEqual(
            parse_tags('"one", two three'), [u'one', u'two three'])

    def test_tags_with_double_quotes_can_contain_commas(self):
        """
        Double quotes can contain commas
        """
        self.assertEqual(parse_tags('a-one "a-two, and a-three"'),
                         [u'a-one', u'a-two, and a-three'])
        self.assertEqual(parse_tags('"two", one, one, two, "one"'),
                         [u'one', u'two'])

    def test_with_naughty_input(self):
        """
        Test with naughty input.
        """
        # Bad users! Naughty users!
        self.assertEqual(parse_tags(None), [])
        self.assertEqual(parse_tags(''), [])
        self.assertEqual(parse_tags('"'), [])
        self.assertEqual(parse_tags('""'), [])
        self.assertEqual(parse_tags('"' * 7), [])
        self.assertEqual(parse_tags(',,,,,,'), [])
        self.assertEqual(parse_tags('",",",",",",","'), [u','])
        self.assertEqual(parse_tags('a-one "a-two" and "a-three'),
                         [u'a-one', u'a-three', u'a-two', u'and'])

    def test_recreation_of_tag_list_string_representations(self):
        plain = Tag.objects.create(name='plain')
        spaces = Tag.objects.create(name='spa ces')
        comma = Tag.objects.create(name='com,ma')
        self.assertEqual(edit_string_for_tags([plain]), u'plain')
        self.assertEqual(
            edit_string_for_tags([plain, spaces]), u'"spa ces", plain')
        self.assertEqual(edit_string_for_tags(
            [plain, spaces, comma]), u'"com,ma", "spa ces", plain')
        self.assertEqual(
            edit_string_for_tags([plain, comma]), u'"com,ma", plain')
        self.assertEqual(
            edit_string_for_tags([comma, spaces]), u'"com,ma", "spa ces"')
