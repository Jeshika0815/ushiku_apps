from django.db import models

class WorkOrder(models.Model):
    # FB・PL選択
    work_sp_choices = [
        ('FB','FB'),
        ('PL','PL'),
    ]
    # 製作グループ選択
    work_groups = [
        ('牛久工場','牛久工場'),
        ('千葉工場','千葉工場'),
        ('石下工場','石下工場'),
        ('その他','その他'),
    ]
    # 製造工程パターン
    p_pattern = [
        ('No.1','No.1'),
        ('No.2','No.2'),
        ('No.3','No.3'),
        ('No.4','No.4'),
        ('一般工程','一般工程'),
        ('その他','その他'),
    ]


    work_order_number = models.PositiveIntegerField("作業指示票番号", unique=True)  # 7桁の整数
    release_date = models.DateField("発行日", auto_now_add=True)
    work_number = models.CharField("工番", max_length=4)  # 英数字4文字
    work_trenum = models.CharField('枝番', max_length=3, default="") # 英数字３文字
    subject = models.CharField("件名", max_length=20)  # 漢字20文字
    process_pattern = models.CharField("製造工程パタン", max_length=10, choices=p_pattern, default="No.1")  # 英数字10文字
    manager = models.CharField("製造管理担当者", max_length=16)  # 漢字16文字
    work_group = models.CharField('製作グループ', max_length=10, choices=work_groups, default="牛久工場") # 漢字10文字
    work_hours = models.DecimalField("作業工数時間", max_digits=4, decimal_places=1)  # 小数点以下1桁
    next_process = models.CharField("次工程", max_length=20)  # 漢字20文字
    start_date = models.DateField("作業開始日", default="2021/01/01")
    end_date = models.DateField("終了予定日", default="2021/01/10")
    work_type = models.CharField('', max_length=2, choices=work_sp_choices, default="FB")
    work_range = models.CharField('作業範囲', max_length=200, default="P00~00.工00~00")
    planed_value = models.DecimalField('計画数', max_digits=3, decimal_places=0, default="")
    syounin_check = models.CharField('承認', max_length=30, default="", blank=True)
    publish_check = models.CharField('作成', max_length=30, default="", blank=True)
    workset_check = models.CharField('工数設定', max_length=30, default="", blank=True)
    buy_check = models.CharField('購買確認', max_length=30, default="", blank=True)
    recive_check = models.CharField('受け取り確認', max_length=30, default="", blank=True)
    

    def __str__(self):
        return f"{self.work_order_number} - {self.subject}"

    class Meta:
        verbose_name = "作業指示票"
        verbose_name_plural = "作業指示票"

class WorkOrderProgress(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name="progresses")
    work_date = models.DateField("作業日", blank=True)
    achievement = models.DecimalField("出来高（％）", max_digits=3, decimal_places=0, default=0, blank=True)
    daily_result = models.DecimalField("当日実績", max_digits=2, decimal_places=0, blank=True)

    def __str__(self):
        return f"{self.work_order} - {self.work_date}"
        

    class Meta:
        verbose_name = "作業進捗"
        verbose_name_plural = "作業進捗"

print(f"startdate >>> {WorkOrder.start_date}")