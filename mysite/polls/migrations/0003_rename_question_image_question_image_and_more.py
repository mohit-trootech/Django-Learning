# Generated by Django 5.0.4 on 2024-08-06 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0002_alter_question_question_tag"),
    ]

    operations = [
        migrations.RenameField(
            model_name="question",
            old_name="question_image",
            new_name="image",
        ),
        migrations.RenameField(
            model_name="question",
            old_name="question_tag",
            new_name="tag",
        ),
    ]
