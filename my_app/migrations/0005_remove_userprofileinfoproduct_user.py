# Generated by Django 4.0.1 on 2022-03-24 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0004_userprofileinfoproduct_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofileinfoproduct',
            name='user',
        ),
    ]