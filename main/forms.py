from django.forms import ModelForm, Form, ModelChoiceField, ValidationError

from main.models import Usuario, Folha
from transparencia_fidelense import settings


class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'contato', 'data_nascimento', 'groups', 'is_active', 'is_superuser' ]

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UsuarioForm, self).save(commit=False)

        if not user.pk:
            user.set_password(settings.DEFAULT_PASSWORD) #Set de default password
            user.is_staff = True
        if commit:
            user.save()
        return user
    

class RelatorioGastosForm(Form):
    folha_inicial = ModelChoiceField(queryset=Folha.objects, label='Folha Inicial')
    folha_final = ModelChoiceField(queryset=Folha.objects, label='Folha Final')

    def clean_folha_final(self):
        if self.cleaned_data['folha_inicial'].ordenacao > self.cleaned_data['folha_final'].ordenacao:
            raise ValidationError(u'A data final deve ser mais recente que a folha inicial.')
        return self.cleaned_data['folha_final']
