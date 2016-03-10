# coding=utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#
class Player(models.Model):
    username = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos', null=True, blank=True)

    def __unicode__(self):
        return unicode(self.username)
#
# # группа. скока хошь групп. скока хошь людей
# class PlayersGroup(models.Model):
#     title = models.CharField(max_length=100)
#     players = models.ManyToManyField(Player)
#
#     def __unicode__(self):
#         return unicode(self.title)

# сет. любой произвольный набор. Песни для сетов берутся из файлов, где названия перечислены в столбик. По файлу на каждый сет. Левел и сложность в файлах отделены от названия и друг от друга вертикальными чертами. Баннеры имеют то же имя, что и песня (без указания сложности).
# class Song(models.Model):
#     title = models.CharField(max_length=200)
#     # lvl = models.CharField(max_length=200)
#     difficulty = models.CharField(max_length=200)
#     banner = models.ImageField(upload_to='banners', null=True, blank=True)
#
#     def __unicode__(self):
#         return unicode(self.title)

class SongsSet(models.Model):
    title = models.CharField(max_length=200)
    # songs = models.ManyToManyField(Song)
    #
    def __unicode__(self):
        return unicode(self.title)





#
# class ActiveTour(models.Model):
#     title = models.CharField(max_length=200)
#
# class BanedSongs(models.Model):
#     song = models.ForeignKey(Song)
#     songset = models.ForeignKey(SongsSet)
#     group = models.ForeignKey(PlayersGroup)
#     take = models.ForeignKey(SongTake)
#
#     def __unicode__(self):
#         return unicode(u'{0.song} {0.take}'.format(self))





from django.db import models
from django.contrib.admin import ModelAdmin

LEVELS = (
    ('Beginner', 'Beginner'),
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Hard', 'Hard'),
    ('Challenge', 'Expert'),
    ('Edit', 'Edit')
)

STYLES = (
    ('single', 'Single'),
    ('double', 'Double'),
    ('routine', 'Routine')
)


class StepchartAdmin(ModelAdmin):
    list_filter = ('diff_num', 'style', 'track__pack')


class TrackAdmin(ModelAdmin):
    list_filter = ('pack',)


class Track(models.Model):

    def __str__(self):
        return '%s (%s)' % (self.name, self.diff)

    name = models.CharField(max_length=100)
    min_bpm = models.IntegerField()
    max_bpm = models.IntegerField()
    pack = models.CharField(max_length=100)
    songset = models.ForeignKey(SongsSet)
    author = models.CharField(max_length=100)
    diff = models.IntegerField()
    banner = models.ImageField(upload_to='banners', null=True, blank=True)


#
# class Stepchart(models.Model):
#
#     def __str__(self):
#         return '%s (%s %s)' % (self.track.name, self.style, self.diff_num)
#
#     diff_num = models.IntegerField()
#     diff_text = models.CharField(choices=LEVELS, max_length=20)
#     comment = models.TextField(null=True)
#     track = models.ForeignKey('Track')
#     style = models.CharField(choices=STYLES, max_length=20)
#
#
# class Tracklist(models.Model):
#     def __str__(self):
#         return self.name
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     stepcharts = models.ManyToManyField('Stepchart')
#
#
# class Tag(models.Model):
#     def __str__(self):
#         return self.tag
#     tag = models.CharField(max_length=20)
#     stepcharts = models.ManyToManyField('Stepchart')

#
# class Result(models.Model):
#
#     # todo meta ordering by date descending
#     def __str__(self):
#         return '%s: %.2f' % (self.stepchart.__str__(), self.percentage)
#     percentage = models.FloatField()
#     date = models.DateField(auto_now_add=True)
#     comment = models.TextField(null=True)
#     modifiers = models.ForeignKey('Mods')
#     stepchart = models.ForeignKey('Stepchart')
#
#
# class Mods(models.Model):
#     speed = models.FloatField()
#     mini = models.IntegerField()
#     rate = models.FloatField(default=1)
#     others = models.TextField(null=True)

class QualTake(models.Model):
    songs = models.ManyToManyField(Track)
    # songset = models.ForeignKey(SongsSet)
    diff = models.IntegerField()

    def __str__(self):
        return '%s' % (self.diff)

class PlayerQualTake(models.Model):
    song = models.ForeignKey(Track)
    qual_r = models.ForeignKey(QualTake)
    player = models.ForeignKey(Player)

    def __str__(self):
        return '%s - %s - %s' % (self.qual_r, self.player, self.song.name)

class QualQueue(models.Model):
    song = models.ForeignKey(Track)
    qual_r = models.ForeignKey(QualTake)
    player = models.ForeignKey(Player, related_name='1+')
    player_vs = models.ForeignKey(Player, related_name='2+',null=True, blank=True)
    prev = models.ForeignKey("self", null=True, blank=True)
    score = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return '%s: %s vs %s (%s)' % (self.qual_r, self.player, self.player_vs, self.song.name)

    class Meta():
        ordering = ['pk']


class TakeOption(models.Model):
    song = models.ForeignKey(Track)
    songtake = models.ForeignKey('SongTake')
    banned = models.NullBooleanField(null=True, blank=True)
#
#     def __unicode__(self):
#         return unicode(u'{0.song} {0.songtake}'.format(self))

# # тейк(take) - набор песен из сета. для этой группы выбор песен это рандом из сета минус отработанный тейк. для группы может быть несколько треков. скока надо
class SongTake(models.Model):
    songs = models.ManyToManyField(Track, through='TakeOption')
    # songs = models.ManyToManyField(Track)
    # songset = models.ForeignKey(Songs,Set)
    # group = models.ForeignKey(PlayersGroup)

    @property
    def is_finished(self):
        if self.songs.all().filter(takeoption__banned_by__isnull=True).count() == 1:
            return True
        else:
            return False

    @property
    def finish_song(self):
        return self.songs.all().filter(takeoption__banned_by__isnull=True).get()

    # def __unicode__(self):
    #     return unicode(u'{0.songset} {0.group}'.format(self))