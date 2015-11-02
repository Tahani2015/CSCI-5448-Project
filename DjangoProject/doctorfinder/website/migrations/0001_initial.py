# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=30)),
                ('zip', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Bio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('education', models.TextField()),
                ('awards', models.TextField()),
                ('experience', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('phoneNumber', models.CharField(max_length=15)),
                ('officeHours', models.CharField(max_length=100)),
                ('speciality', models.CharField(max_length=30, choices=[(b'Primary Care', b'Primary Care'), (b'Dentist', b'Dentist'), (b'Dermatologist', b'Dermatologist'), (b'ENT', b'ENT'), (b'Eye Doctor', b'Eye Doctor'), (b'Psychiatrist', b'Psychiatrist'), (b'Orthopedist', b'Orthopedist')])),
                ('rating', models.FloatField()),
                ('availability', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteDoctors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('doctor', models.ForeignKey(to='website.Doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, choices=[(b'Aetna', b'Aetna'), (b'Cigna', b'Cigna'), (b'Medicaid', b'Medicaid'), (b'Medicare', b'Medicare'), (b'Tricare', b'Tricare'), (b'Blue', b'Blue'), (b'United', b'United')])),
                ('doctor', models.ForeignKey(to='website.Doctor')),
            ],
        ),
        migrations.CreateModel(
            name='RegisteredPatient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField()),
                ('comment', models.TextField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('doctor', models.ForeignKey(to='website.Doctor')),
                ('patient', models.ForeignKey(to='website.RegisteredPatient')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=256)),
                ('type', models.CharField(max_length=10, choices=[(b'Admin', b'Admin'), (b'Patient', b'Patient'), (b'Doctor', b'Doctor')])),
            ],
        ),
        migrations.AddField(
            model_name='registeredpatient',
            name='username',
            field=models.ForeignKey(to='website.User'),
        ),
        migrations.AddField(
            model_name='favoritedoctors',
            name='patient',
            field=models.ForeignKey(to='website.RegisteredPatient'),
        ),
        migrations.AddField(
            model_name='bio',
            name='doctor',
            field=models.ForeignKey(to='website.Doctor'),
        ),
        migrations.AddField(
            model_name='address',
            name='doctor',
            field=models.ForeignKey(to='website.Doctor'),
        ),
    ]
