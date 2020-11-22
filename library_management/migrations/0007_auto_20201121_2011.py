# Generated by Django 3.1.3 on 2020-11-21 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library_management', '0006_auto_20201121_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_category', to='library_management.category'),
        ),
    ]