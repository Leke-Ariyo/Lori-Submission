# Generated by Django 3.1.3 on 2020-11-20 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_management', '0003_remove_book_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='booklending',
            name='days_borrowed',
            field=models.IntegerField(default=0),
        ),
    ]
