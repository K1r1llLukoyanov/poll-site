# Generated by Django 4.2.4 on 2023-08-21 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_alter_category_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='img',
            field=models.ImageField(default=None, null=True, upload_to='polls/images'),
        ),
    ]