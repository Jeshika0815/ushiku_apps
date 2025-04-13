# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import csv
from .forms import WorkOrderForm, WorkOrderProgressFormSet
from .models import WorkOrder, WorkOrderProgress
from django.db.models import Sum


# view the 作業指示票一覧
@login_required
def work_order_list(request):
    work_orders = WorkOrder.objects.all()
    work_progress = WorkOrderProgress.objects.all()
    wo_count = work_orders.count()
    if not work_orders.exists():
        return render(request, 'sagyoshiji/work_order_list.html', {'woerror': '作業指示表のデータが存在しません。登録してください。'})
    return render(request, 'sagyoshiji/work_order_list.html', {'work_orders': work_orders, 'wo_count':wo_count})


# 削除機能のビュー
@login_required
def delete_work_order(request, pk):
    work_order = get_object_or_404(WorkOrder, pk=pk)
    if request.method == "POST":
        work_order.delete()
        return redirect('sagyoshiji:work_order_list')
    return render(request, 'sagyoshiji/delete_work_order.html', {'work_order': work_order})

# view the 作業指示票登録
@login_required
def register_work_order(request):
    if request.method == 'POST':
        form = WorkOrderForm(request.POST)
        #formset = WorkOrderProgressFormSet(request.POST, instance=form.instance)
        print("! Posted")
        print(f"formdata {form}")
        #if form.is_valid() and formset.is_valid():
        if form.is_valid():
            form.save()
            #formset.save()
            print("! all saved")
            return redirect('sagyoshiji:work_order_list')
    else:
        form = WorkOrderForm()
        #formset = WorkOrderProgressFormSet(instance=WorkOrder())
    return render(request, 'sagyoshiji/register_work_order.html', {'form': form})

# view the 作業指示票修正
@login_required
def edit_work_order(request, pk):
    # 修正する作業指示票を取得
    work_order = get_object_or_404(WorkOrder, pk=pk)
    
    if request.method == 'POST':
        form = WorkOrderForm(request.POST, instance=work_order)
        formset = WorkOrderProgressFormSet(request.POST, instance=work_order)
        if form.is_valid() and formset.is_valid():
            form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                # 必要なフィールドが適切に入力されているか確認
                if instance.daily_result is not None and instance.work_date :
                    print("! check successful")
                    instance.save()
            # 削除が選択されたインスタンスを削除
            for instance in formset.deleted_objects:
                print("! instance was delete")
                instance.delete()
            return redirect('sagyoshiji:work_order_list')
    else:
        form = WorkOrderForm(instance=work_order)
        formset = WorkOrderProgressFormSet(instance=work_order)
    
    return render(request, 'sagyoshiji/edit_work_order.html', {'form': form, 'formset': formset, 'work_order': work_order})

# view the 作業指示票詳細
@login_required
def work_order_detail(request, pk):
    # 指定された作業指示票とその進捗データを取得
    work_order = get_object_or_404(WorkOrder, pk=pk)
    work_orders= WorkOrder.objects.all()  # 関連する進捗データを取得
    
    total_worked = WorkOrderProgress.objects.filter(work_order=work_order).aggregate(Sum('daily_result'))['daily_result__sum'] or 0
    progress_rate = (total_worked / work_order.planed_value) * 100 if work_order.planed_value else 0 #caluculations
    print(f"! result is {progress_rate}")
    """
    for order in work_orders:
        total_worked = WorkOrderProgress.objects.filter(work_order=order).aggregate(Sum('daily_result'))['daily_result__sum'] or 0
        progress_rate = (total_worked / order.planed_value) * 100 if order.planed_value else 0 #caluculations
        #saving to db (caluclations result)
        #order.progress_rate = round(progress_rate, 2)
        #order.save()
        print(f"! result is {progress_rate}")
    """

    return render(request, 'sagyoshiji/work_order_detail.html', {
        'work_order': work_order,
        'progresses': work_orders,
        'progress_rate': progress_rate
    })

#CSV and PDF download support

@login_required
def export_sagyoshijihyo_csv(request):
    # CSVレスポンス設定
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sagyoshijihyo.csv"'

    # Shift-JIS エンコーディング
    response.write(u'\ufeff'.encode('utf-8-sig'))  # BOM追加（Excel対応）
    writer = csv.writer(response)
    # ヘッダー行
    writer.writerow([
        '作業指示票番号', '工番', '件名', '製造工程パタン', '製造管理担当者',
        '作業工数時間', '次工程', '作業開始日', '終了予定日'
    ])

    # 作業指示票データを取得してCSVに書き込む
    sagyoshijihyo_list = WorkOrder.objects.all()
    for shiji in sagyoshijihyo_list:
        writer.writerow([
            shiji.id,
            shiji.work_number,
            shiji.subject,
            shiji.process_pattern,
            shiji.manager,
            shiji.work_hours,
            shiji.next_process,
            shiji.start_date,
            shiji.end_date,
        ])

    return response


@login_required
def export_workorderprogress_csv(request):
    # CSVレスポンス設定
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="work_order_progress.csv"'

    # CSVライターを作成
    writer = csv.writer(response, quoting=csv.QUOTE_MINIMAL)

    # ヘッダー行を記述
    writer.writerow([
        '進捗ID', '作業指示票番号', '作業日', '出来高（％）', '当日実績'
    ])

    # WorkOrderProgress の全データを取得してCSVに書き込む
    progress_list = WorkOrderProgress.objects.select_related('work_order').all()
    for progress in progress_list:
        writer.writerow([
            progress.id,
            progress.work_order.work_order_number if progress.work_order else 'なし',
            progress.work_date.strftime('%Y-%m-%d'),
            progress.achievement,
            progress.daily_result,
        ])
    """
    response = HttpResponse(content_type='text/csv; charset=shift_jis')
    response['Content-Disposition'] = 'attachment; filename="work_order_progress.csv"'

    writer = csv.writer(response, quoting=csv.QUOTE_MINIMAL)

    # ヘッダー行
    writer.writerow([
        '進捗ID', '作業指示票番号', '作業日', '出来高（％）', '当日実績'
    ])

    # データ行
    progress_list = WorkOrderProgress.objects.select_related('work_order').all()
    for progress in progress_list:
        writer.writerow([
            progress.id,
            progress.work_order.work_order_number if progress.work_order else 'なし',
            progress.work_date.strftime('%Y-%m-%d'),
            progress.achievement,
            progress.daily_result,
        ])

    return response

#import library for create PDF / PDFを生成するためのライブラリを取得
"""
from weasyprint import HTML #デバイスがわで用意する必要あり
from django.template.loader import get_template

@login_required
def order_detail_to_pdf(request, pk):
    try:
        worder = get_object_or_404(WorkOrder, pk=pk)
    except WorkOrder.DoesNotExist or WorkOrderProgress.DoesNotExist:
        return HttpResponse('WorkOrder can not found.', status=404)
    
    html_content = get_template("sagyoshiji/work_order_detail.html")
    context = {'worder':worder}
    htmls = html_content.render(context)

    # generate pdf
    pdf_file = HTML(string=htmls).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'filename="作業指示票_{worder.subject}"'
    return response
"""
