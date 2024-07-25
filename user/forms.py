from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UpdateFormulario(UserChangeForm):
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        required=False,
        help_text='Deixe em branco se não quiser alterar a senha.',
    )

    password2 = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        required=False,
        help_text='Digite a mesma senha novamente para confirmação.',
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error('password2', ValidationError('As senhas não coincidem.'))
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error('password1', errors)
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get('password1')

        if password1:
            user.set_password(password1)
        
        if commit:
            user.save()
        return user


class FormularioRegistro(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=3,
    )

    last_name = forms.CharField(
        required=True,
        min_length=3,
    )

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este email já está cadastrado.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password1 != password2:
            self.add_error('password2', ValidationError('As senhas não coincidem.'))

        try:
            password_validation.validate_password(password1)
        except ValidationError as errors:
            self.add_error('password1', errors)

        return cleaned_data
