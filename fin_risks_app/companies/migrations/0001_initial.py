# Generated by Django 3.2.16 on 2024-01-21 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254, verbose_name='Наименование компании')),
                ('bin', models.CharField(error_messages={'unique': 'Компания с таким БИН уже существует.'}, max_length=12, unique=True, verbose_name='БИН')),
            ],
            options={
                'verbose_name': 'компания',
                'verbose_name_plural': 'компании',
                'ordering': ['name'],
            },
        ),
    ]
