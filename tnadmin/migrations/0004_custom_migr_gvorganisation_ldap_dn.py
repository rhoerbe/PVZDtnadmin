# Generated by Django 2.1.4 on 2019-01-04 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tnadmin', '0003_custom_migr_add_gvfederation_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='gvorganisation',
            name='ldap_dn',
            field=models.CharField(default='', max_length=250),
        ),
    ]
