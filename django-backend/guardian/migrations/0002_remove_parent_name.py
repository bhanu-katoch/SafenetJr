# Generated by Django 5.1.6 on 2025-04-12 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("guardian", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="parent",
            name="name",
        ),
    ]
