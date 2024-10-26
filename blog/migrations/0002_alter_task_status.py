# Generated by Django 4.1.3 on 2023-08-13 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('TODO', 'TODO'), ('In progress', 'In progress'), ('Done', 'Done'), ('In revision', 'In revision')], default='TODO', max_length=50),
        ),
    ]
