# Generated by Django 4.0.1 on 2022-01-12 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_transaction_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=20),
        ),
    ]
