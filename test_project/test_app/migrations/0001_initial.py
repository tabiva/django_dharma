# Generated by Django 4.2.16 on 2024-09-07 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TestModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("field1", models.CharField(max_length=30)),
                ("field2", models.CharField(max_length=30)),
            ],
        ),
    ]