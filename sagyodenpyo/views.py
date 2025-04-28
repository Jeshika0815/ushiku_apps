from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from django.db.models import Sum
from collections import defaultdict
from .models import WorkLog
from .forms import WorkLogForm
import datetime
from django.db.models import Prefetch
from itertools import groupby
from operator import itemgetter


from django.contrib.auth.views import LogoutView
class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        """GET リクエストでもログアウトを許可"""
        return self.post(request, *args, **kwargs)

@login_required
def work_logs(request):
    # 従業員情報の取得
    try:
        employee = request.user.employee
    except employee.DoesNotExist:
        return HttpResponseForbidden("このユーザーには対応する従業員情報がありません。管理者に問い合わせてください。")
        #return render(request, '403.html', {"message":"このユーザーには対応する従業員情報がありません。管理者に問い合わせてください。"})
    
    # 日付範囲の指定
    initial_date = now().date()
    selected_date_str = request.GET.get('selected_date', datetime.datetime.now().strftime('%Y-%m-%d'))
    if selected_date_str:
        try:
            selected_date = datetime.datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = initial_date

    else:
        selected_date = initial_date

    start_date = selected_date
    end_date = start_date + timedelta(days=7)
        
    # 作業履歴を日付順に取得
    work_logs = WorkLog.objects.filter(employee=employee,date__range=(start_date,end_date)).order_by('date')
    awork_logs = WorkLog.objects.select_related('employee').filter(date__range=(start_date,end_date)).order_by('date', 'employee__name')
    
    # 作業時間の自動計算
    total_hours,remining_minutes = calc_p_wlogs(work_logs)
    # 作業伝票個数表示
    count_logs = work_logs.count()
    # 個人の作業履歴の取得
    an_work_log = WorkLog.objects.filter(employee=employee).order_by('-date') 
    # テンプレートで返す変数群
    context = {
        'work_logs': awork_logs,
        'work_log':an_work_log,
        'total_hours': total_hours,
        'remining_minutes': remining_minutes,
        'cout_logs': count_logs,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'sagyodenpyo/view_wlogs.html', context)

# 作業伝票集計
@login_required
def log_totals(request):
    return render(request , 'sagyodenpyo/view_totals.html')

@login_required
def log_work(request):
    if request.method == "POST":
        form = WorkLogForm(request.POST)
        if form.is_valid():
            work_log = form.save(commit=False)
            work_log.employee = request.user.employee  # ログイン中の従業員を紐付け
            work_log.save()
            return redirect('sagyodenpyo:work_logs')
    else:
        form = WorkLogForm()
    return render(request, 'sagyodenpyo/log_work.html', {'form': form})

@login_required
def edit_work_log(request, pk):
    work_log = get_object_or_404(WorkLog, pk=pk, employee=request.user.employee)
    if request.method == "POST":
        form = WorkLogForm(request.POST, instance=work_log)
        if form.is_valid():

            form.save()
            return redirect('sagyodenpyo:work_logs')
    else:
        form = WorkLogForm(instance=work_log)
    return render(request, 'sagyodenpyo/edit_work_log.html', {'form': form})

from django.http import HttpResponseForbidden

@login_required
def work_log_list(request):
    try:
        employee = request.user.employee
    except Employee.DoesNotExist:
        return HttpResponseForbidden("このユーザーには対応する従業員情報がありません。管理者に問い合わせてください。")

    work_logs = WorkLog.objects.filter(employee=employee).order_by('-date')
    return render(request, 'sagyodenpyo/work_log_list.html', {'work_logs': work_logs})

# 全員の作業履歴を取得し、日付ごとにグループ化してテンプレートに渡すビュー
@login_required
def all_work_logs_by_date(request):
    # 全ての作業履歴を日付順に取得
    work_logs = WorkLog.objects.select_related('employee').order_by('date', 'employee__name')

    # 日付ごとにグループ化
    grouped_logs = {}
    for date, logs in groupby(work_logs, key=lambda log: log.date):
        grouped_logs[date] = list(logs)

    return render(request, 'sagyodenpyo/all_work_logs_by_date.html', {'grouped_logs': grouped_logs})

#全体の作業履歴のテーブル出力
@login_required
def all_logs(request):
    # 全ての作業履歴を取得
    work_log = WorkLog.objects.all()
    # 存在する日数のカウント
    wl_count = work_log.count()
    return render(request, 'sagyodenpyo/all_wlogs.html', {'work_log':work_log, 'wl_count':wl_count})

#for CSV download
import csv
from django.http import HttpResponse
from .models import WorkLog

@login_required
def export_work_logs_csv(request):
    # Shift-JIS 対応のレスポンス設定
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="work_logs.csv"'

    # Shift-JIS でエンコードされた CSV データを生成
    writer = csv.writer(response, quoting=csv.QUOTE_MINIMAL)

    # ヘッダー行（日本語）
    header = ['従業員名', '工番', '枝番', '件名', '作業コード', '作業時間(時間)', '作業時間(分)', '作業日']
    response.write(",".join(header).encode('shift_jis') + b"\r\n")

    # データ行
    work_logs = WorkLog.objects.select_related('employee').all()
    for log in work_logs:
        row = [
            str(items)

            for items in [
            log.employee.name,
            log.work_number,
            log.work_trenum,
            log.subject,
            log.work_code,
            log.work_hours,
            log.work_minute,
            log.date.strftime("%Y-%m-%d")
            ]
        ]
        response.write(",".join(row).encode('shift_jis') + b"\r\n")

    return response

# other functions

# 個人の履歴周り
def p_work_logs():
    pass

# 個人の作業時間計算周り
def calc_p_wlogs(work_logs):
    # work_hours and work_minutes
    total_work_hours = work_logs.aggregate(total_hours=Sum('work_hours'),total_minute=Sum('work_minute'))

    # calucration of total work hours
    total_hours = total_work_hours['total_hours'] or 0
    total_minute = total_work_hours['total_minute'] or 0
    total_hours += total_minute // 60
    remining_minutes = total_minute % 60

    return total_hours, remining_minutes

# 作業伝票集計・工番とその中に枝番ごとにグループ化
def totaling():
    

    pass
