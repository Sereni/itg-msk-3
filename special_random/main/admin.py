from django.contrib import admin
from .models import *

# @admin.register(Player)
# class PlayerAdmin(admin.ModelAdmin):
#     pass
#
# @admin.register(PlayersGroup)
# class PlayersGroupAdmin(admin.ModelAdmin):
#     pass
#
# @admin.register(Song)
# class SongAdmin(admin.ModelAdmin):
#     pass
#
# @admin.register(SongsSet)
# class SongsSetAdmin(admin.ModelAdmin):
#     pass
#
# @admin.register(SongTake)
# class SongTakeAdmin(admin.ModelAdmin):
#     pass
#
# @admin.register(ActiveTour)
# class ActiveTourAdmin(admin.ModelAdmin):
#     pass
#
# @admin.register(BanedSongs)
# class BanedSongsAdmin(admin.ModelAdmin):
#     pass

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    pass

@admin.register(SongsSet)
class SongsSetAdmin(admin.ModelAdmin):
    pass

@admin.register(QualTake)
class QualTakeAdmin(admin.ModelAdmin):
    pass

@admin.register(PlayerQualTake)
class PlayerQualTakeAdmin(admin.ModelAdmin):
    pass

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass

@admin.register(QualQueue)
class QualQueueAdmin(admin.ModelAdmin):
    pass

