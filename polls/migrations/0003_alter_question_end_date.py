# Generated by Django 4.1.1 on 2022-09-12 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_question_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='null'),
        ),
    ]
