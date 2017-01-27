from django import forms
from .models import Comentario

class ComentForm(forms.ModelForm):
	Texto_Comentario = forms.CharField(widget=forms.Textarea)

	class Meta:
		model = Comentario
		fields = ('Texto_Comentario',)