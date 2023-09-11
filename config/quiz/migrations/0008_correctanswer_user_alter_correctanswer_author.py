# Generated by Django 4.2.4 on 2023-08-26 05:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0007_delete_info_user_leaduser_active_leaduser_date_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='correctanswer',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='correctanswer',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lead_answers', to='quiz.leaduser'),
        ),
    ]