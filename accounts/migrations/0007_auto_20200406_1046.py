# Generated by Django 3.0.4 on 2020-04-06 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20200404_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Out of Delivery', 'Out Of Delivery'), ('Delivered', 'Delivered')], default='Pending', max_length=200, null=True),
        ),
    ]