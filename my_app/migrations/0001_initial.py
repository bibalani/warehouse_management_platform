# Generated by Django 4.0.1 on 2022-03-23 16:25

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
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('produced_date', models.DateField(blank=True)),
                ('expired_date', models.DateField(blank=True)),
                ('company', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('warehouse_type', models.CharField(choices=[('supplier', 'SUPPLIER'), ('drugstore', 'DRUGSTORE'), ('regular_customer', 'REGULAR_CUSTOMER')], default='', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='WarehouseProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inventory', models.IntegerField()),
                ('delivery_date', models.DateField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.product')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.warehouse')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfileInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membership_type', models.CharField(choices=[('site_admin', 'SITE_ADMIN'), ('supplier', 'SUPPLIER'), ('drugstore', 'DRUGSTORE'), ('regular_customer', 'REGULAR_CUSTOMER')], max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.CharField(max_length=20)),
                ('quantity', models.IntegerField()),
                ('order_date', models.DateField()),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_destination', to='my_app.warehouse')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.product')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_source', to='my_app.warehouse')),
            ],
        ),
        migrations.CreateModel(
            name='Movement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('remain_quantity', models.IntegerField()),
                ('movement_date', models.DateField()),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movement_destination', to='my_app.warehouse')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.product')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movement_source', to='my_app.warehouse')),
            ],
        ),
        migrations.CreateModel(
            name='DemandSupplyMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quant', models.IntegerField()),
                ('demand_movement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='demand_movement', to='my_app.movement')),
                ('supply_movement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supply_movement', to='my_app.movement')),
            ],
        ),
    ]
