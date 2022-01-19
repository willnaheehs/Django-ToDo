# Generated by Django 4.0.1 on 2022-01-19 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('memo', models.CharField(max_length=250)),
                ('dateCreated', models.DateField(auto_now=True)),
                ('dateCompleted', models.DateField(auto_now=True)),
            ],
        ),
    ]