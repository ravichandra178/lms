# Generated by Django 3.0.8 on 2020-08-26 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0002_module_pdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='pdf',
            field=models.FileField(blank=True, default='mozilla.pdf', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='module',
            name='pdf',
            field=models.FileField(blank=True, default='mozilla.pdf', null=True, upload_to=''),
        ),
    ]