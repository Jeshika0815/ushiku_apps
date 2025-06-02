from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from django.db.models import Sum
from collections import defaultdict
from sagyoshiji.models import WorkOrder
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
    selected_date = request.GET.get('date') or str(datetime.date.today()) 

    try:
        target_date = datetime.date.fromisoformat(selected_date)
    except ValueError:
        target_date = datetime.date.today()

    summary = totaling(target_date)
    context = {
        'selected_date':target_date,
        'count_logss':summary['count_logss'],
        'total_hours': summary['total_hours'],
        'total_minute': summary['total_minute'],
        'order_summary': summary['onum_summary']
    }
    
    return render(request , 'sagyodenpyo/view_totals.html', context)

# 作業伝票登録
@login_required
def log_work(request):
    work_orders = WorkOrder.objects.all().order_by('-release_date')
    if request.method == "POST":
        form = WorkLogForm(request.POST)
        if form.is_valid():
            work_log = form.save(commit=False)
            work_log.employee = request.user.employee  # ログイン中の従業員を紐付け
            work_log.save()
            return redirect('sagyodenpyo:work_logs')
    else:
        form = WorkLogForm()
    return render(request, 'sagyodenpyo/log_work.html', {'form': form, 'work_orders':work_orders})

# 作業伝票修正
@login_required
def edit_work_log(request, pk):
    work_orders = WorkOrder.objects.all().order_by('-release_date')
    work_log = get_object_or_404(WorkLog, pk=pk, employee=request.user.employee)
    if request.method == "POST":
        form = WorkLogForm(request.POST, instance=work_log)
        if form.is_valid():

            form.save()
            return redirect('sagyodenpyo:work_logs')
    else:
        form = WorkLogForm(instance=work_log)
    return render(request, 'sagyodenpyo/edit_work_log.html', {'form': form, 'work_orders':work_orders})

from django.http import HttpResponseForbidden

# 作業履歴一覧(不使用)
@login_required
def work_log_list(request):
    try:
        employee = request.user.employee
    except Employee.DoesNotExist:
        return HttpResponseForbidden("このユーザーには対応する従業員情報がありません。管理者に問い合わせてください。")

    work_logs = WorkLog.objects.filter(employee=employee).order_by('-date')
    return render(request, 'sagyodenpyo/work_log_list.html', {'work_logs': work_logs})

# 全員の作業履歴を取得し、日付ごとにグループ化してテンプレートに渡すビュー(不使用)
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
    from urllib.parse import quote
    # CSVレスポンス設定
    filename = f"全体の作業伝票 - {datetime.datetime.now().strftime('%Y%m%d')}.csv"
    encoded_fname = quote(filename)
    response = HttpResponse(content_type='text/csv; charset=shift_jis')
    response['Content-Disposition'] = f"attachment; filename*=UTF-8\'\'{encoded_fname}"

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

#個人の作業履歴の出力
"""
@login_required
def export_personal_work_logs_csv(request):
    from urllib.parse import quote
    work_logs = WorkLog.objects.filter(employee=employee).order_by('-date')

    filename = f"{request.user.name}の作業伝票 - {datetime.datetime.now().strftime('%Y%m%d')}.csv"
    encoded_fname = quote(filename)
    response = HttpResponse(content_type='text/csv')
    response['Content-Dispostion'] = f'attachment; filename*=UTF-8\'\'{encoded_fname}'
        # Shift-JIS でエンコードされた CSV データを生成
    writer = csv.writer(response, quoting=csv.QUOTE_MINIMAL)

    # ヘッダー行（日本語）
    header = ['従業員名', '工番', '枝番', '件名', '作業コード', '作業時間(時間)', '作業時間(分)', '作業日']
    response.write(",".join(header).encode('shift_jis') + b"\r\n")

    # データ行
    for log in work_logs:
        row = [
            str(items)

            for items in [
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
"""

# other functions

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
def totaling(target_date):
    logs = WorkLog.objects.filter(date=target_date) #作業履歴を取得
    # 作業伝票個数表示
    count_logss = logs.count()

    totals = logs.aggregate(
        total_hour = Sum('work_hours'),
        total_minute = Sum('work_minute')
    )
    total_hours = totals.get('total_hour',0) or 0
    total_minute = totals.get('total_minute',0) or 0
    
    # 工番ごとの集計データを保持する辞書
    onum_summary = defaultdict(lambda: {'total_hours':0, 'total_minute':0, 'trenum_details':[], 'trenum_group':set(), 'subject':set()}) #工番ごとの_合計

    # 工番ごとの集計
    for log in logs:
        onum = log.work_number
        trenum_details = {
            'trenum': log.work_trenum,
            'employee': log.employee,
            'work_code': log.work_code,
            'work_hours': log.work_hours,
            'work_minute': log.work_minute
        }
        onum_summary[onum]['total_hours'] += log.work_hours
        onum_summary[onum]['total_minute'] += log.work_minute
        onum_summary[onum]['trenum_details'].append(trenum_details)
        onum_summary[onum]['trenum_group'].add(log.work_trenum)
        onum_summary[onum]['subject'].add(log.subject)

    # 必要に応じてセットをリストに変換
    for onum, summary in onum_summary.items():
        summary['trenum_group'] = list(summary['trenum_group'])
        summary['subject'] = ', '.join(summary['subject'])
        #summary['subject'] = list(summary['subject'])

        
    return {
        'count_logss': count_logss,
        'total_hours':total_hours,
        'total_minute':total_minute,
        'onum_summary':dict(onum_summary)
    }
