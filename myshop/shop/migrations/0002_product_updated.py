# Generated by Django 4.2.3 on 2023-07-30 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
    ]
