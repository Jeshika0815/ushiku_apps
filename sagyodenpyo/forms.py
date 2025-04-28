from django import forms
from .models import WorkLog
from sagyoshiji.models import WorkOrder

class WorkLogForm(forms.ModelForm):
    
    work_number = forms.ModelChoiceField(
        queryset=WorkOrder.objects.values_list('work_number', flat=True).distinct(),
        label='工番',
        required=True,
    )
    work_trenum = forms.ModelChoiceField(
        queryset=WorkOrder.objects.none(),
        label='枝番',
        required=True,
    )
    

    class Meta:
        model = WorkLog
        fields = ['date', 'work_number', 'work_trenum', 'work_code', 'work_hours', 'work_minute']
        labels = {
            'date': '作業日',
            'work_number': '工番',
            'work_trenum': '枝番',
            'work_code': '作業コード',
            'work_hours': '時間',
            'work_minute': '分',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # HTML5の日付入力ウィジェット
            'work_hours': forms.NumberInput(attrs={'min':'0','max':'23'}),
            'work_minute': forms.NumberInput(attrs={'step': '10', 'min':'0', 'max':'50'}),
        }
    
    def __init__(self, *args, **kwargs):
        work_number_selected = None

        if 'initial' in kwargs and 'work_number' in kwargs['initial']:
            work_number_selected = kwargs['initial']['work_number']

        if 'data' in kwargs and 'work_number' in kwargs['data']:
            work_number_selected = kwargs['data']['work_number']

        #work_number_selected = kwargs.pop('work_number_selected', None)
        super().__init__(*args, **kwargs)
        if work_number_selected:
            self.fields['work_trenum'].queryset = WorkOrder.objects.filter(
                work_number=work_number_selected
            ).distinct()
        else:
            self.fields['work_trenum'].queryset = WorkOrder.objects.none()