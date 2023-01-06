# Generated by Django 4.1.4 on 2023-01-03 07:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dailyreads', '0009_alter_blogs_id_alter_news_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='id',
            field=models.UUIDField(default=uuid.UUID('ad82bf03-a411-4405-8a71-074c4527613d'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='news',
            name='id',
            field=models.UUIDField(default=uuid.UUID('c5381a96-6463-42e5-b7ef-9f0b9925f4e6'), editable=False, primary_key=True, serialize=False),
        ),
    ]
