# Generated by Django 4.2.4 on 2023-08-20 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='img',
            field=models.ImageField(default=None, upload_to='images/'),
        ),
    ]
