# Generated by Django 2.1.4 on 2019-02-01 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fedop', '0005_auto_20190131_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='policyjournal',
            name='policy_journal',
            field=models.BinaryField(help_text='Policy Journal signed with an enveloping XML signature', verbose_name='Policy Journal'),
        ),
    ]