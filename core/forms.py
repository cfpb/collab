from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from core.models import CollabUser
from core.models import OrgGroup, OfficeLocation
from django.conf import settings

required_validator = {
    'first_name': 'Your first name is required.',
    'last_name': 'Your last name is required.',
    'title': 'Your title is required.',
    #'office_location':'Please select your primary CFPB office location.',
    'team': 'Please choose which team you are on.',
    'email': 'Please enter an authorized email address.',
    'email_dupe': 'This email address is already in use.',
    'office_phone': 'Your office phone number is required.',
}


def valid_domain(email):
    valid_domain = False
    for domain in settings.VALID_DOMAINS:
        if email.endswith(domain):
            valid_domain = True

    return valid_domain


def email_exists(email):
    if len(CollabUser.objects.filter(email=email)) > 0:
        return True
    else:
        return False


class RegistrationForm(forms.Form):
    first_name = forms.CharField(
        max_length=100, label="First name",
        error_messages={'required': required_validator['first_name']})
    last_name = forms.CharField(
        max_length=100, label="Last name",
        error_messages={'required': required_validator['last_name']})
    title = forms.CharField(max_length=100, error_messages={'required':
                            required_validator['title']},
                            label="Role")
    office_location = forms.ModelChoiceField(
        queryset=OfficeLocation.objects.all(), required=False,
        empty_label="- - - - - - Select  - - - - -")
    org_group = forms.ModelChoiceField(queryset=OrgGroup.objects.all().order_by(
        'title'), error_messages={'required': required_validator['team']},
        label="Office")
    email = forms.CharField(max_length=100, error_messages={'required':
                            required_validator['email']})
    office_phone = forms.CharField(max_length=100, required=False)
    mobile_phone = forms.CharField(max_length=100, required=False)
    home_phone = forms.CharField(max_length=100, required=False,
                                 label="Alternate phone")
    photo_file = forms.FileField(required=False)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not valid_domain(email):
            raise forms.ValidationError(required_validator['email'])
        if email_exists(email):
            raise forms.ValidationError(required_validator['email_dupe'])
        return email


class AccountForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(AccountForm, self).__init__(*args, **kwargs)

    first_name = forms.CharField(
        max_length=100, label="First name",
        error_messages={'required': required_validator['first_name']})
    last_name = forms.CharField(
        max_length=100, label="Last name",
        error_messages={'required': required_validator['last_name']})
    email = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'size': '50'}),
        error_messages={'required': required_validator['email']})
    office_phone = forms.CharField(max_length=100, required=False)
    mobile_phone = forms.CharField(max_length=100, required=False)
    home_phone = forms.CharField(max_length=100, required=False,
                                 label="Alternate phone")
    office_location = forms.ModelChoiceField(
        queryset=OfficeLocation.objects.all(), required=False,
        empty_label="- - - - - - Select  - - - - -", label="Building")
    desk_location = forms.CharField(
        max_length=50, required=False, label="Room")
    org_group = forms.ModelChoiceField(
        queryset=OrgGroup.objects.all().order_by('title'),
        error_messages={'required': required_validator['team']},
        label="Office")
    title = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'size': '50'}),
        error_messages={'required': required_validator['title']},
        label='Role')
    what_i_do = forms.CharField(
        widget=forms.Textarea(attrs={'rows': '8', 'cols': '100'}),
        required=False, label="My expertise")
    current_projects = forms.CharField(
        widget=forms.Textarea(attrs={'rows': '8', 'cols': '100'}),
        required=False, label="My projects")
    things_im_good_at = forms.CharField(
        widget=forms.Textarea(attrs={'rows': '8', 'cols': '100'}),
        required=False, label="Other things about me")
    allow_tagging = forms.BooleanField(required=False)
    email_notifications = forms.BooleanField(required=False)
    photo_file = forms.FileField(required=False)

    def clean_email(self):
        email = self.cleaned_data['email']
        email_changed = self.user.email != email
        if not valid_domain(email):
            raise forms.ValidationError(
                required_validator['email'])  # found bug. squish.
        if email_changed and email_exists(email):
            raise forms.ValidationError(required_validator['email_dupe'])
        return email


class CollabUserCreationForm(UserCreationForm):
    """
    Modify the Django UserCreationForm with upated char limits for username
    """
    username = forms.RegexField(max_length=75, regex=r"^[\w.'@+-]+$",
        help_text="Required. 75 characters or fewer. Letters, digits and " +
                  "@/./'/+/-/_ only.",
        error_messages={
            'invalid': "This value may contain only letters, numbers and " +
                       "@/./'/+/-/_ characters."})

    class Meta:
        model = CollabUser
        fields = ("username",)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            CollabUser._default_manager.get(username=username)
        except CollabUser.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


class CollabUserChangeForm(UserChangeForm):
    """
    Modify the Django UserChangeForm with upated char limits for username
    """
    username = forms.RegexField(
        max_length=75, regex=r"^[\w.@'+-]+$",
        help_text="Required. 75 characters or fewer. Letters, digits and " +
                  "@/./'/+/-/_ only.",
        error_messages={
            'invalid': "This value may contain only letters, numbers and " +
                       "@/./'/+/-/_ characters."})

    class Meta:
        model = CollabUser

    def __init__(self, *args, **kwargs):
        super(CollabUserChangeForm, self).__init__(*args, **kwargs)
