# Generated by Django 4.1.3 on 2023-03-06 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_listing_bidactive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image_url',
            field=models.CharField(max_length=200),
        ),
    ]
