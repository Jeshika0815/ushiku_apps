# Generated by Django 5.2 on 2025-05-09 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sagyodenpyo', '0005_alter_worklog_work_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worklog',
            name='work_code',
            field=models.CharField(choices=[('001', '001'), ('002', '002'), ('003', '003'), ('004', '004'), ('005', '005'), ('006', '006'), ('007', '007'), ('008', '008'), ('009', '009'), ('010', '010'), ('011', '011'), ('012', '012'), ('013', '013'), ('014', '014'), ('015', '015'), ('016', '016'), ('017', '017'), ('018', '018'), ('019', '019'), ('402', '402'), ('602', '602'), ('701', '701'), ('903', '903'), ('908', '908'), ('909', '909'), ('999', '999')], max_length=3, verbose_name='作業コード'),
        ),
    ]
