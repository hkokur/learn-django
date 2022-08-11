# Generated by Django 4.0.6 on 2022-08-09 05:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('dr', 'draft'), ('pu', 'published'), ('de', 'deleted')], default='dr', max_length=2)),
                ('title', models.CharField(max_length=100)),
                ('update', models.DateField(auto_now=True)),
                ('create', models.DateField(auto_now_add=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
