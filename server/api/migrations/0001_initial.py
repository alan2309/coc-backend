# Generated by Django 4.0 on 2023-03-04 23:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('profile_img', models.CharField(blank=True, max_length=255, null=True)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=100)),
                ('friends', models.JSONField(blank=True, default=list, null=True)),
                ('home', models.CharField(max_length=100)),
                ('phone', models.IntegerField(blank=True, null=True)),
                ('interests', models.JSONField(blank=True, null=True)),
                ('pending_req', models.JSONField(blank=True, default=list, null=True)),
                ('blocked', models.JSONField(blank=True, default=list, null=True)),
                ('req_sent', models.JSONField(blank=True, default=list, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('location', models.JSONField()),
                ('loc_name', models.CharField(blank=True, max_length=100, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('companion', models.JSONField(blank=True, null=True)),
                ('itinerary', models.JSONField(blank=True, null=True)),
                ('feedback', models.IntegerField(default=0)),
                ('pending_req', models.JSONField(blank=True, null=True)),
                ('status', models.IntegerField(default=0)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.myuser')),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('itinerary', models.JSONField()),
                ('location', models.JSONField()),
                ('loc_name', models.CharField(blank=True, max_length=20, null=True)),
                ('time', models.TimeField(auto_now=True)),
                ('review', models.CharField(max_length=200)),
                ('images', models.JSONField()),
                ('trip', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.trip')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.myuser')),
            ],
        ),
    ]
