# Generated by Django 4.2.5 on 2023-09-22 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=50)),
                ('f_name', models.CharField(default='', max_length=50)),
                ('l_name', models.CharField(default='', max_length=50)),
                ('email', models.EmailField(default='', max_length=30)),
            ],
        ),
    ]
