# Generated by Django 3.1.1 on 2020-09-29 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showusers', '0002_auto_20200929_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayval',
            name='DAUgrowth',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='dayval',
            name='MAUgrowth',
            field=models.CharField(max_length=10),
        ),
    ]
