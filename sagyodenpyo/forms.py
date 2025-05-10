from django import forms
from .models import WorkLog

class WorkLogForm(forms.ModelForm):
    class Meta:
        model = WorkLog
        fields = ['date', 'work_number', 'work_trenum', 'subject', 'work_code', 'work_hours', 'work_minute']
        labels = {
            'date': '作業日',
            'work_number': '工番',
            'work_trenum': '枝番',
            'subject': '件名',
            'work_code': '作業コード',
            'work_hours': '時間',
            'work_minute': '分',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # HTML5の日付入力ウィジェット
            'work_hours': forms.NumberInput(attrs={'min':'0','max':'23'}),
            'work_minute': forms.NumberInput(attrs={'step': '10', 'min':'0', 'max':'50'}),
        }
