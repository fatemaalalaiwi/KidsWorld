from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_previous_migration'),  # replace with your last migration
    ]

    operations = [
        migrations.AddField(
            model_name='kids_games',
            name='create_date',
            field=models.DateField(auto_now_add=True, null=True, blank=True),
        ),
    ]
