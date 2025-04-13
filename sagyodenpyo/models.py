from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    employee_number = models.CharField("従業員番号", max_length=10, unique=True)
    name = models.CharField("氏名", max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee")

    def __str__(self):
        return self.name

class WorkLog(models.Model):
    WORK_CODE_CHOICES = [
        ('001', 'P001'),
        ('002', 'P002'),
        ('003', 'P003'),
        ('004', 'P004'),
        ('005', 'P005'),
        ('006', 'P006'),
        ('007', 'P007'),
        ('008', 'P008'),
        ('009', 'P009'),
        ('010', 'P010'),
        ('011', 'P011'),
        ('012', 'P012'),
        ('013', 'P013'),
        ('014', 'P014'),
        ('015', 'P015'),
        ('016', 'P016'),
        ('017', 'P017'),
        ('018', 'P018'),
        ('019', 'P019'),
        ('402', 'P402'),
        ('602', 'P602'),
        ('701', 'P701'),
        ('903', 'P903'),
        ('908', 'P908'),
        ('909', 'P909'),
        ('999', 'P999'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="work_logs")
    work_number = models.CharField("工番", max_length=4)
    work_trenum = models.CharField("枝番", max_length=3, default=000)
    subject = models.CharField("件名", max_length=20)
    work_code = models.CharField("作業コード", max_length=3, choices=WORK_CODE_CHOICES)
    work_hours = models.DecimalField("時間", max_digits=4, decimal_places=0, default=0)
    work_minute = models.DecimalField("分", max_digits=2, decimal_places=0, default=0)
    date = models.DateField("作業日", auto_now_add=False)

    def __str__(self):
        return f"{self.employee.name} - {self.work_number} ({self.date})"

#display user name(all)
"""
from django.contrib.auth.models import User

users = User.objects.all().values('id', 'username', 'first_name', 'last_name')

for user in users:
    full_name = f"{user['first_name']} {user['last_name']}"
    print(f"ユーザID：{user['id']}, ユーザ名：{user['username']},  フルネーム：({full_name})")

#display user name(select)
def get_full_name(user_name):
    try:
        user = User.objects.get(username=user_name)
        full_name = f"{user.first_name} {user.last_name}"
        print(f"ユーザ名：{user.username}, フルネーム：{full_name}")
    except User.DoesNotExist:
        print(f"指定したIDのユーザIDのユーザは存在しません.")
get_full_name('tid100')
"""