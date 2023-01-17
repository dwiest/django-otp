from django import forms
from django.conf import settings
import pyotp


class OtpForm(forms.Form):
  secret_key = forms.CharField(
    label='secret_key',
    min_length="32",
    max_length="32",
    initial='',
    required=False,
    widget=forms.TextInput(attrs={'size': '38'}))

  def clean_secret_key(self):
    if self.cleaned_data['secret_key'] == '':
      secret_key = pyotp.random_base32()
      new_data = self.data.copy()
      new_data['secret_key'] = secret_key
      self.data = new_data
      return secret_key
    else:
      return self.cleaned_data['secret_key']

  def get_otp(self):
    totp = pyotp.TOTP(self.cleaned_data['secret_key'])
    return totp.now()
