# Generated by Django 5.0 on 2023-12-08 05:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("board", "0003_comment_author"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="modify_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="post",
            name="modify_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
