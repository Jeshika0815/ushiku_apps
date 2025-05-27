from django import forms
from .models import WorkLog
from sagyoshiji.models import WorkOrder

class WorkLogForm(forms.ModelForm):
    work_number = forms.ChoiceField(
        choices=[('', '----')] + [(work_number, work_number) for work_number in WorkOrder.objects.filter(work_number__isnull=False).values_list('work_number', flat=True).distinct().order_by('-release_date')],
        label='工番',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    work_trenum = forms.ChoiceField(
        choices=[('', '----')] + [(work_trenum, work_trenum) for work_trenum in WorkOrder.objects.filter(work_trenum__isnull=False, work_number__isnull=False).values_list('work_trenum', flat=True).distinct().order_by('-release_date')],
        label='枝番',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    subject = forms.ChoiceField(
        choices=[('', '----')] + [(subject, subject) for subject in WorkOrder.objects.filter(subject__isnull=False).values_list('subject', flat=True).distinct().order_by('-release_date')],
        label='件名',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    """
    work_number = forms.ModelChoiceField(
        queryset = WorkOrder.objects.filter(work_number__isnull=False).values_list('work_number', flat=True).distinct().order_by('-release_date'),
        empty_label="----",
        label='工番',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    work_trenum = forms.ModelChoiceField(
        queryset=WorkOrder.objects.filter(work_trenum__isnull=False, work_number__isnull=False).values_list('work_trenum', flat=True).distinct().order_by('-release_date'),
        empty_label="----",
        label='枝番',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    subject = forms.ModelChoiceField(
        queryset=WorkOrder.objects.filter(subject__isnull=False).values_list('subject', flat=True).distinct().order_by('-release_date'),
        empty_label="----",
        label='件名',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        work_number = kwargs.pop('work_number', None)
        super().__init__(*args, **kwargs)
        if work_number:
            self.fields['work_trenum'].queryset = WorkOrder.objects.filter(
                work_number=work_number,
                work_trenum__isnull = False
            ).distinct().order_by('-release_date')
        else:
            self.fields['work_trenum'].queryset = WorkOrder.objects.none()
    """

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


        