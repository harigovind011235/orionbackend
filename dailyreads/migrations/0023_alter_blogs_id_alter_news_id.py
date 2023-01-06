# Generated by Django 4.1.4 on 2023-01-05 05:08

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dailyreads', '0022_alter_blogs_id_alter_news_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='id',
            field=models.UUIDField(default=uuid.UUID('4d427b2c-c30e-4ea6-87c4-2b6cb239476c'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='news',
            name='id',
            field=models.UUIDField(default=uuid.UUID('02dcdc18-0282-4e96-a7ed-5b9b8343ad09'), editable=False, primary_key=True, serialize=False),
        ),
    ]
