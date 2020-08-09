# Generated by Django 3.0.8 on 2020-08-08 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('scheduled_date', models.DateField()),
                ('stadium', models.CharField(max_length=200)),
                ('round', models.CharField(choices=[('Final', 'Final Round'), ('Semi Final', 'Semi Final Round'), ('Qualifying Round', 'Qualifying Round'), ('Quarter Final', 'Quarter Final')], default='Qualifying Round', max_length=20)),
                ('team1_score', models.PositiveIntegerField(default=0)),
                ('team2_score', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('average_score', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('height', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('average_score', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
                ('matches', models.IntegerField(default=0)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tms_web.Team')),
            ],
        ),
        migrations.CreateModel(
            name='MatchTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField(default=0)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tms_web.Match')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tms_web.Team')),
            ],
        ),
        migrations.CreateModel(
            name='MatchPlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField(default=0)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tms_web.Match')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tms_web.Player')),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='team1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team1_name', to='tms_web.Team'),
        ),
        migrations.AddField(
            model_name='match',
            name='team2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team2_name', to='tms_web.Team'),
        ),
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('team', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tms_web.Team')),
            ],
        ),
    ]
