# Generated by Django 4.2.5 on 2023-11-03 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_data', '0008_alter_credential_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credential',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]