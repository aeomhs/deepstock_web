# Generated by Django 2.2.7 on 2019-12-02 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0008_auto_20191202_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrapyitem',
            name='date',
            field=models.TextField(default='기사 날짜', null=True, verbose_name='날짜'),
        ),
    ]
