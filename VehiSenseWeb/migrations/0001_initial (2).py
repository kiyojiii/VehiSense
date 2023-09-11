# Generated by Django 4.2.5 on 2023-09-11 16:00

import VehiSenseWeb.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carbrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=VehiSenseWeb.models.filepath)),
                ('brand', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(max_length=100)),
                ('status', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cartypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=100)),
                ('status', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=6, null=True)),
                ('email', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=1000)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('zipcode', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=VehiSenseWeb.models.vehicle_filepath)),
                ('brand', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('enginetype', models.CharField(max_length=100)),
                ('transmission', models.CharField(max_length=100)),
                ('technology', models.CharField(max_length=100)),
                ('mvfileno', models.CharField(max_length=100)),
                ('plate', models.CharField(max_length=100)),
                ('variant', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=100)),
                ('mileage', models.CharField(max_length=100)),
                ('engineno', models.CharField(max_length=100)),
                ('chasisno', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000, null=True)),
                ('status', models.CharField(max_length=15, null=True)),
                ('price', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
