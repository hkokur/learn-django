# Generated by Django 4.0.6 on 2022-12-07 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_alter_profile_profile_picture'),
        ('authorization', '0008_alter_review_published_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.creator'),
        ),
        migrations.AlterField(
            model_name='review',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.creator'),
        ),
    ]
