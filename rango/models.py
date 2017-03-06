from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=30, blank=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    repository_url = models.CharField(_('repository url'), max_length=60, blank=False)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def guid(self):
        '''
        Returns the first eight characters of the email address, this should be
        the guid of the student email.

        ie. '2198230W@student.gla.ac.uk' -> '2198230W'
        '''
        if not email.endswith('@student.gla.ac.uk'):
            return None
        return email[:8]

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


class TestCategory(models.Model):
    name = models.CharField(_('name'), blank=False, max_length=30)


class Test(models.Model):
    case = models.CharField(_('case'), blank=False, max_length=80)
    test = models.CharField(_('test'), blank=False, max_length=80)
    description = models.TextField(_('description'), blank=True)
    category = models.ForeignKey(TestCategory, null=True, on_delete=models.SET_NULL)


class TestRun(models.Model):
    student = models.ForeignKey(User, on_delete=models.PROTECT)
    repository_url = models.CharField(_('repository url'), max_length=60, blank=False)
    date_run = models.DateTimeField(_('date run'), auto_now_add=True)
    test_version = models.CharField(_('tests version'), max_length=10, blank=False)
    log = models.TextField(_('log'), blank=False)
    time_taken = models.PositiveIntegerField(_('time taken'), blank=False)
    status = models.CharField(_('status'), max_length=15, blank=False)


class TestRunDetail(models.Model):
    record = models.ForeignKey(TestRun, on_delete=models.PROTECT)
    test = models.ForeignKey(Test, on_delete=models.PROTECT)
    passed = models.BooleanField(_('passed'), default=False)
    log = models.TextField(_('log'), blank=False)
