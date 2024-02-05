# Generated by Django 5.0 on 2024-01-22 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('cname', models.CharField(max_length=50, verbose_name='customer name')),
                ('cemail', models.CharField(max_length=100)),
                ('cphn', models.CharField(max_length=15)),
                ('fbdesc', models.TextField(null=True)),
                ('fbdate', models.DateField()),
                ('fbid', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
    ]