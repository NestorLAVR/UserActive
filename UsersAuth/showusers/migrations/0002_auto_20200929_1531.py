# Generated by Django 3.1.1 on 2020-09-29 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showusers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dayval',
            old_name='trDAU',
            new_name='triaDAU',
        ),
        migrations.RenameField(
            model_name='dayval',
            old_name='trMAU',
            new_name='triaMAU',
        ),
        migrations.AddField(
            model_name='dayval',
            name='date',
            field=models.CharField(default='', max_length=40),
        ),
    ]
