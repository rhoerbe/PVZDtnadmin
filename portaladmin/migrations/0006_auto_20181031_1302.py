# Generated by Django 2.1.2 on 2018-10-31 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portaladmin', '0005_auto_20181018_2209'),
    ]

    operations = [
        migrations.CreateModel(
            name='MDstatementHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entityID', models.CharField(max_length=128, unique=True)),
                ('Status', models.CharField(choices=[('uploaded', 'hochgeladen'), ('request_queue', 'signiert und eingebracht'), ('rejected', 'fehlerhaft'), ('published', 'veröffentlicht'), ('deleted', 'gelöscht')], default='uploaded', max_length=14, null=True, verbose_name='Status')),
                ('Validation_message', models.CharField(blank=True, max_length=1000, null=True)),
                ('ed_uploaded', models.TextField(blank=True, help_text='SAML EntityDescriptor (uploaded, signiert)', max_length=100000, null=True, verbose_name='EntityDescriptor uploaded')),
                ('ed_signed', models.TextField(blank=True, help_text='SAML EntityDescriptor (signiert)', max_length=100000, null=True, verbose_name='EntityDescriptor signiert')),
                ('delete', models.BooleanField(default=False, help_text='EntitiyDescriptor vom Metadaten Aggregat löschen')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Eingangsdatum')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Metadaten Statement',
                'ordering': ['entityID', 'updated_at'],
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='mdstatement',
            options={'ordering': ['entityID', 'updated_at'], 'verbose_name': 'Metadaten Statement'},
        ),
        migrations.AddField(
            model_name='mdstatementhistory',
            name='MDstatement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portaladmin.MDstatement'),
        ),
    ]