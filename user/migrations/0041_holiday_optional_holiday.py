# Generated by Django 4.1.4 on 2023-01-23 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0040_holiday'),
    ]

    operations = [
        migrations.AddField(
            model_name='holiday',
            name='optional_holiday',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]