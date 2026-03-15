from django import forms
from ..models import ImportacaoCSV

class CSVUploadForm(forms.ModelForm):

    class Meta:
        model = ImportacaoCSV
        fields = ["arquivo"]