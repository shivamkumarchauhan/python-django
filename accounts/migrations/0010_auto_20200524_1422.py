# Generated by Django 3.0.5 on 2020-05-24 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20200524_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placeordermodel',
            name='product_price',
            field=models.IntegerField(editable=False),
        ),
    ]
