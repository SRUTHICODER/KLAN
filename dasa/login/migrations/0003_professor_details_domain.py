# Generated by Django 3.2.4 on 2022-07-10 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_answer_jpg_answer_verified_question_jpg_question_verified_time_out'),
    ]

    operations = [
        migrations.AddField(
            model_name='professor_details',
            name='domain',
            field=models.CharField(default='lang', max_length=50),
            preserve_default=False,
        ),
    ]
