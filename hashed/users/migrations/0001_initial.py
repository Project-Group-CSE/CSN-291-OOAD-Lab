# Generated by Django 4.2.5 on 2023-10-07 05:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('hashed_password', models.CharField(max_length=200)),
                ('hashed_pin', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='credential',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.user')),
                ('title', models.CharField(blank=True, max_length=50)),
                ('website', models.URLField()),
                ('hash_pwd', models.CharField(max_length=200)),
                ('strength', models.IntegerField()),
            ],
        ),
    ]
