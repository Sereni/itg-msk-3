# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-15 23:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EasterEggPlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to=b'photos')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=b'photos')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerQualTake',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Player')),
            ],
        ),
        migrations.CreateModel(
            name='QualQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.CharField(blank=True, max_length=100, null=True)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='1+', to='main.Player')),
                ('player_vs', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='2+', to='main.Player')),
                ('prev', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.QualQueue')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='QualTake',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diff', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SongsSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('round', models.CharField(choices=[(b'Main', b'Main'), (b'Finals', b'Finals')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='SongTake',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TakeOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banned', models.NullBooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('min_bpm', models.IntegerField()),
                ('max_bpm', models.IntegerField()),
                ('pack', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('diff', models.IntegerField()),
                ('banner', models.ImageField(blank=True, null=True, upload_to=b'banners')),
                ('songset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.SongsSet')),
            ],
            options={
                'ordering': ['diff', 'name'],
            },
        ),
        migrations.AddField(
            model_name='takeoption',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Track'),
        ),
        migrations.AddField(
            model_name='takeoption',
            name='songtake',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.SongTake'),
        ),
        migrations.AddField(
            model_name='songtake',
            name='songs',
            field=models.ManyToManyField(through='main.TakeOption', to='main.Track'),
        ),
        migrations.AddField(
            model_name='qualtake',
            name='songs',
            field=models.ManyToManyField(to='main.Track'),
        ),
        migrations.AddField(
            model_name='qualqueue',
            name='qual_r',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.QualTake'),
        ),
        migrations.AddField(
            model_name='qualqueue',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Track'),
        ),
        migrations.AddField(
            model_name='playerqualtake',
            name='song',
            field=models.ManyToManyField(blank=True, null=True, to='main.Track'),
        ),
        migrations.AddField(
            model_name='eastereggplayer',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='e1+', to='main.Player'),
        ),
        migrations.AddField(
            model_name='eastereggplayer',
            name='player_vs',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='e2+', to='main.Player'),
        ),
    ]
