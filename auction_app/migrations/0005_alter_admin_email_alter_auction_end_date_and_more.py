# Generated by Django 4.2.13 on 2024-06-05 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction_app', '0004_alter_customer_document_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='auction',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='auction',
            name='start_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='customer',
            name='document_number',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='customer',
            name='document_type',
            field=models.CharField(max_length=50),
        ),
    ]
