# Generated by Django 4.0.1 on 2022-03-25 21:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0007_alter_movement_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movement',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='my_app.order'),
        ),
    ]
