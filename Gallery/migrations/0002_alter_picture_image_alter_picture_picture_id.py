# Generated by Django 5.0.6 on 2024-05-28 12:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Gallery", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="picture",
            name="image",
            field=models.BinaryField(db_column="image"),
        ),
        migrations.AlterField(
            model_name="picture",
            name="picture_id",
            field=models.IntegerField(
                auto_created=True,
                db_column="picture_id",
                primary_key=True,
                serialize=False,
            ),
        ),
    ]