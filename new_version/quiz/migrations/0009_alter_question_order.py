# Generated by Django 4.2.4 on 2023-09-08 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_correctanswer_user_alter_correctanswer_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='order',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
