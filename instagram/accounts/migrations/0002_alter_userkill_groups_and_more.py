# Generated by Django 4.2.4 on 2024-01-16 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userkill',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='userkill_groups', to='auth.group'),
        ),
        migrations.AlterField(
            model_name='userkill',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='userkill_user_permissions', to='auth.permission'),
        ),
        migrations.AlterModelTable(
            name='userkill',
            table='userkills',
        ),
    ]
