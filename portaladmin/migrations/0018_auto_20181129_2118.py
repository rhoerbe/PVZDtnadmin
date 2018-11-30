# Generated by Django 2.1.1 on 2018-11-29 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portaladmin', '0017_auto_20181129_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mdstatement',
            name='content_valid',
            field=models.BooleanField(default=False, null=True, verbose_name='Content validation'),
        ),
        migrations.AlterField(
            model_name='mdstatement',
            name='deletionRequest',
            field=models.BooleanField(default=False, null=True, verbose_name='Deletion Request (unpublish Entity)'),
        ),
        migrations.AlterField(
            model_name='mdstatement',
            name='entity_fqdn',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Entity FQDN'),
        ),
        migrations.AlterField(
            model_name='mdstatementhistory',
            name='content_valid',
            field=models.BooleanField(default=False, null=True, verbose_name='Content validation'),
        ),
        migrations.AlterField(
            model_name='mdstatementhistory',
            name='deletionRequest',
            field=models.BooleanField(default=False, null=True, verbose_name='Deletion Request (unpublish Entity)'),
        ),
        migrations.AlterField(
            model_name='mdstatementhistory',
            name='entity_fqdn',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Entity FQDN'),
        ),
    ]