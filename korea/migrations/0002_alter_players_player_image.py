# Generated by Django 3.2.13 on 2022-11-28 05:52

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('korea', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='players',
            name='player_image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, upload_to='media/'),
        ),
    ]
