# Generated by Django 4.2 on 2023-04-22 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualprod', '0004_visualprod_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='visualprod',
            name='image',
            field=models.CharField(default='https://web9.unl.edu.ar/noticias/img/thumbs/news/37787/foto%20peli_vga.jpg', max_length=200),
        ),
    ]
