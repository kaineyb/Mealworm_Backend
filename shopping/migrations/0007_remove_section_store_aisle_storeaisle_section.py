# Generated by Django 4.0.2 on 2022-02-16 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0006_store_aisles_storeaisle_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='store_aisle',
        ),
        migrations.AddField(
            model_name='storeaisle',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shopping.section'),
        ),
    ]
