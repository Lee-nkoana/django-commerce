# Generated by Django 4.1.3 on 2023-03-07 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_alter_listing_min_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='min_bid',
        ),
        migrations.AddField(
            model_name='listing',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]
