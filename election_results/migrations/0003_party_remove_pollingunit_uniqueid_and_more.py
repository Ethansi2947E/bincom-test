# Generated by Django 5.0.2 on 2025-03-01 01:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election_results', '0002_alter_pollingunit_long_alter_lga_table_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Party',
            fields=[
                ('party_id', models.AutoField(primary_key=True, serialize=False)),
                ('party_name', models.CharField(max_length=100)),
                ('party_abbreviation', models.CharField(max_length=10, unique=True)),
            ],
            options={
                'verbose_name_plural': 'parties',
                'db_table': 'party',
            },
        ),
        migrations.RemoveField(
            model_name='pollingunit',
            name='uniqueid',
        ),
        migrations.AddField(
            model_name='announcedlgaresults',
            name='lga',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='election_results.lga'),
        ),
        migrations.AddField(
            model_name='pollingunit',
            name='uniquewardid',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='announcedlgaresults',
            name='date_entered',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='announcedlgaresults',
            name='lga_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='announcedlgaresults',
            name='party_abbreviation',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='announcedpuresults',
            name='date_entered',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='announcedpuresults',
            name='party_abbreviation',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='announcedpuresults',
            name='polling_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='election_results.pollingunit'),
        ),
        migrations.AlterField(
            model_name='pollingunit',
            name='date_entered',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pollingunit',
            name='lga',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='election_results.lga'),
        ),
        migrations.AlterField(
            model_name='pollingunit',
            name='ward',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='election_results.ward'),
        ),
        migrations.AddField(
            model_name='announcedlgaresults',
            name='party',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='election_results.party'),
        ),
        migrations.AddField(
            model_name='announcedpuresults',
            name='party',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='election_results.party'),
        ),
    ]
