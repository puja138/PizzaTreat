# Generated by Django 5.2.1 on 2025-06-17 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_tablebooking'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tablebooking',
            old_name='created_at',
            new_name='booked_at',
        ),
        migrations.AddField(
            model_name='tablebooking',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tablebooking',
            name='payment_method',
            field=models.CharField(default='Cash', max_length=50),
            preserve_default=False,
        ),
    ]
