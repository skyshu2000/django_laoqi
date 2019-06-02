from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core import mail
from django.urls import reverse
from django.urls import resolve
from django.test import TestCase

# Create your tests here.
class PasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('account:password_reset')
        self.response = self.client.get(url)
    
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_view_function(self):
        view = resolve('/account/password-reset/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetView)
    
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
    
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)
    
    def test_form_input(self):
        '''
        The view must contain two inputs: csrf and email
        '''
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)

class SuccessfulPasswordResetTests(TestCase):
    def setUp(self):
        email = 'john@doe.com'
        User.objects.create_user(username='john', email=email, password='1234abcdef')
        url = reverse('account:password_reset')
        self.response = self.client.post(url, {'email': email})
    
    def test_redirection(self):
        '''
        A valid form submission should redirect the user to 'password_reset_done' view.
        '''
        url = reverse('account:password_reset_done')
        self.assertRedirects(self.response, url)
    
    def test_send_password_reset_email(self):
        self.assertEquals(1, len(mail.outbox))

class InvalidPasswordRestTests(TestCase):
    def setUp(self):
        url = reverse('account:password_reset')
        self.response = self.client.post(url, {'email': 'donotexist@email.com'})
    
    def test_redirection(self):
        '''
        Even invalid emails in the database should
        redirect the user to 'password_reset_doen' view
        '''
        url = reverse('account:password_reset_done')
        self.assertRedirects(self.response, url)
    
    def test_no_password_reset_email_sent(self):
        self.assertEquals(0, len(mail.outbox))