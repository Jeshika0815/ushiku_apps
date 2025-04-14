from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from sagyodenpyo.models import WorkLog
from sagyoshiji.models import WorkOrder, WorkOrderProgress
from sagyodenpyo.forms import WorkLogForm
from django.db.models import Sum

import os

from django.contrib.auth.views import LogoutView
class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        """GET リクエストでもログアウトを許可"""
        return self.post(request, *args, **kwargs)

#　ダッシュボードを表示する関数    
@login_required
def home(request):
    try:
        employee = request.user.employee
    except employee.DoesNotExist:
        return HttpResponseForbidden('このユーザーには対応する従業員情報がありません。管理者に問い合わせてください。')
    
    work_logs = WorkLog.objects.filter(employee=employee).order_by('-date')
    work_orders = WorkOrder.objects.all()

    for order in work_orders:
        total_worked = WorkOrderProgress.objects.filter(work_order=order).aggregate(Sum('daily_result'))['daily_result__sum'] or 0
        progress_rate = (total_worked / order.planed_value) * 100 if order.planed_value else 0 #caluculations
        #saving to db (caluclations result)
        order.progress_rate = round(progress_rate, 2)
        order.save()

    work_order_count = work_orders.count()
    return render(request, 'home/dashboard.html', {'work_logs': work_logs, 'work_orders': work_orders, 'work_order_count':work_order_count })

