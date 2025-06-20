# Generated by Django 5.1.5 on 2025-04-07 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sagyoshiji', '0018_alter_workorder_buy_check_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='process_pattern',
            field=models.CharField(choices=[('1', 'No.1'), ('2', 'No.2'), ('3', 'No.3'), ('4', 'No.4'), ('5', '一般工程'), ('6', 'その他')], default='No.1', max_length=10, verbose_name='製造工程パタン'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='work_group',
            field=models.CharField(choices=[('1', '牛久工場'), ('2', '千葉工場'), ('3', '石下工場'), ('4', 'その他')], default='牛久工場', max_length=10, verbose_name='製作グループ'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='work_range',
            field=models.CharField(default='P00~00.工00~00', max_length=200, verbose_name='作業範囲'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='work_type',
            field=models.CharField(choices=[('1', 'FB'), ('2', 'PL')], default='FB', max_length=2, verbose_name='作業種別'),
        ),
        migrations.AlterField(
            model_name='workorderprogress',
            name='achievement',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=3, verbose_name='出来高（％）'),
        ),
        migrations.AlterField(
            model_name='workorderprogress',
            name='daily_result',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=2, verbose_name='当日実績'),
        ),
        migrations.AlterField(
            model_name='workorderprogress',
            name='work_date',
            field=models.DateField(blank=True, verbose_name='作業日'),
        ),
    ]
