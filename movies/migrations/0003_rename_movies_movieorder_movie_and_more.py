# Generated by Django 4.2 on 2023-04-17 01:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0002_movieorder_movie_order"),
    ]

    operations = [
        migrations.RenameField(
            model_name="movieorder",
            old_name="movies",
            new_name="movie",
        ),
        migrations.AlterField(
            model_name="movieorder",
            name="buyed_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
