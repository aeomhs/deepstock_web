# Generated by Django 2.2.7 on 2019-12-02 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0007_scrapyitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scrapyitem',
            name='data',
        ),
        migrations.AddField(
            model_name='scrapyitem',
            name='info',
            field=models.TextField(default='기사 사이트', null=True, verbose_name='사이트'),
        ),
        migrations.AddField(
            model_name='scrapyitem',
            name='title',
            field=models.TextField(default='기사 제목', null=True, verbose_name='제목'),
        ),
        migrations.AddField(
            model_name='scrapyitem',
            name='url',
            field=models.TextField(default='기사 링크', null=True, verbose_name='링크'),
        ),
        migrations.AlterField(
            model_name='scrapyitem',
            name='date',
            field=models.DateField(default='기사 날짜', null=True, verbose_name='날짜'),
        ),
    ]
