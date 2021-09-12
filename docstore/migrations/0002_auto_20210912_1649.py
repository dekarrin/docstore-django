# Generated by Django 3.2.7 on 2021-09-12 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docstore', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='contents',
            field=models.TextField(editable=False),
        ),
        migrations.AlterField(
            model_name='folder',
            name='topics',
            field=models.ManyToManyField(blank=True, related_name='folders', to='docstore.Topic'),
        ),
    ]
