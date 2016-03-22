from models import *
from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.ModelForm):
		class Meta:
			model = User
			fields = ['username', 'password']

class RegisterForm(forms.Form):
	username = forms.CharField(max_length = 20)
	password1 = forms.CharField(max_length = 200,
				label='Password',
				widget = forms.PasswordInput())
	password2 = forms.CharField(max_length = 200,
				label='Confirm password',
				widget = forms.PasswordInput())

	def clean(self):

		cleaned_data = super(RegisterForm, self).clean()

		password1 = cleaned_data.get('password1')
		password2 = cleaned_data.get('password2')

		if password1 and password2 and password1 != password2:
			raise forms.ValidationError('Passwords did not match.')

		return cleaned_data

	def clean_username(self):

		username = self.cleaned_data.get('username')
		if User.objects.filter(username__exact=username):
			raise forms.ValidationError('Username already exists.')

		return username

class SearchForm(forms.Form):
	search_text = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Search for...', 'class': 'form-control'}))

	def clean(self):

		cleaned_data = super(SearchForm, self).clean()

		return cleaned_data

class UpdateCharacterForm(forms.Form):

	char_name = forms.CharField(max_length=42)
	description = forms.CharField(max_length=255)
	img = forms.CharField()
	svg_text = forms.CharField()
	snap_json = forms.CharField()

	def clean(self):

		cleaned_data = super(UpdateCharacterForm, self).clean()

		return cleaned_data

class SortRankingsForm(forms.Form):

	data = forms.CharField(max_length=10)
	ascending = forms.CharField(max_length=10)

	def clean(self):

		cleaned_data = super(SortRankingsForm, self).clean()

		return cleaned_data

class WriteBattleForm(forms.Form):
	html = forms.CharField()
	challenge = forms.CharField()

	def clean(self):

		cleaned_data = super(WriteBattleForm, self).clean()

		return cleaned_data

class VoteForm(forms.Form):
	battle = forms.IntegerField()
	character = forms.IntegerField()

	def clean(self):

		cleaned_data = super(VoteForm, self).clean()

		return cleaned_data

