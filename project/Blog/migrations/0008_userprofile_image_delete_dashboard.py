# Generated by Django 4.2.6 on 2024-01-31 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0007_userprofile_delete_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.DeleteModel(
            name='dashboard',
        ),
    ]
