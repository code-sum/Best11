# Generated by Django 3.2.13 on 2022-12-05 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('korea', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sns_url', models.TextField()),
                ('players', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='korea.players')),
            ],
        ),
    ]