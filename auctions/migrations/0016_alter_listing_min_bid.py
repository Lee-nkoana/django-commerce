# Generated by Django 4.1.3 on 2023-03-07 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_listing_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='min_bid',
            field=models.IntegerField(default=0),
        ),
    ]