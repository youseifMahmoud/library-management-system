# Generated by Django 5.1.1 on 2024-09-30 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_alter_book_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='photo',
        ),
        migrations.AddField(
            model_name='book',
            name='cover_image',
            field=models.ImageField(default='default_cover.jpg', upload_to='book_covers/'),
        ),
    ]
