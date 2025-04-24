from django import forms
from .models import OrganismoSectorial, PPDA, MedidaAvance

class OrganismoSectorialForm(forms.ModelForm):
    class Meta:
        model = OrganismoSectorial
        fields = ['nombre', 'contacto', 'telefono']
        widgets = {
            'nombre': forms.Select(attrs={'class': 'form-control'}),
            'contacto': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PPDAForm(forms.ModelForm):
    class Meta:
        model = PPDA
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_termino', 'organismo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_termino': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'organismo': forms.Select(attrs={'class': 'form-control'}),
        }

class MedidaAvanceForm(forms.ModelForm):
    class Meta:
        model = MedidaAvance
        fields = ['descripcion', 'fecha_limite', 'avance', 'estado', 'observaciones']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_limite': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'avance': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
