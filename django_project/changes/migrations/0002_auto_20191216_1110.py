# Generated by Django 2.2 on 2019-12-16 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sponsor',
            options={'ordering': ['project', 'name'], 'verbose_name': 'Sustaining Member', 'verbose_name_plural': 'Sustaining Members'},
        ),
        migrations.AlterModelOptions(
            name='sponsorshiplevel',
            options={'ordering': ['project', '-value'], 'verbose_name': 'Sustaining Member Level', 'verbose_name_plural': 'Sustaining Member Levels'},
        ),
        migrations.AlterModelOptions(
            name='sponsorshipperiod',
            options={'ordering': ['project', '-end_date'], 'verbose_name': 'Sustaining Member Period', 'verbose_name_plural': 'Sustaining Member Periods'},
        ),
        migrations.AddField(
            model_name='sponsor',
            name='rejected',
            field=models.BooleanField(default=False, help_text='Whether this sustaining member has been rejected for use by the project manager.'),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='remarks',
            field=models.CharField(blank=True, help_text='Remarks regarding status of this sustaining members, i.e. Rejected, because lacks of information', max_length=500, null=True),
        ),
    ]
