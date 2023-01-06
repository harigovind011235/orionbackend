# Generated by Django 4.1.4 on 2023-01-04 06:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0021_alter_dailyhour_id_alter_employee_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyhour',
            name='id',
            field=models.UUIDField(default=uuid.UUID('776c1ac0-7039-4794-afd9-94396060c0f4'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='id',
            field=models.UUIDField(default=uuid.UUID('5dd7cdb1-09df-4a3d-8b24-ee9b9d221bc2'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='leave',
            name='leave_type',
            field=models.CharField(choices=[('1', 'causal leave'), ('2', 'sick leave'), ('3', 'emergency leave'), ('4', 'Comp OFF'), ('5', 'optional holiday')], default='1', max_length=20),
        ),
    ]
