# Generated by Django 3.2.16 on 2023-02-27 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('life', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorymodel',
            name='category_name',
            field=models.CharField(max_length=10),
        ),
    ]
