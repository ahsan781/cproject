# Generated by Django 2.2.24 on 2021-09-06 09:30

from django.db import migrations, models
import django.db.models.deletion
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_rename_vender_profile_memberprofile_vendor_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adduser',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='eventmember',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='memberprofile',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='multiduplicatetask',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='shiftdetail',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='vendorprofile',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, null=True)),
                ('date', models.DateField()),
                ('start_time', models.TimeField(null=True)),
                ('end_time', models.TimeField(null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('location', models.CharField(max_length=200, null=True)),
                ('note', models.FileField(null=True, upload_to='uploads/')),
                ('job', models.CharField(choices=[('Customer 1', 'Customer 1'), ('Project A', 'Project A'), ('Shift Manager', 'Shift Manager'), ('Work site A', 'Work site A')], max_length=50, null=True)),
                ('tz1', timezone_field.fields.TimeZoneField(blank=True, default='Asia/Calcutta', null=True)),
                ('username', models.CharField(max_length=200, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.MemberProfile')),
            ],
        ),
    ]
