from django.contrib import admin
from .models import *

from django import forms
from django.db.models import Q


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

# class QualTakeAdminForm(forms.ModelForm):
#     class Meta:
#         model = QualTake
#
#     exclude = []

    # def __init__(self, *args, **kwargs):
    #     super(EventAdminForm, self).__init__(*args, **kwargs)
    #     if 'event_dates' in self.initial:
    #         self.fields['event_dates'].queryset = EventDate.objects.filter(Q(pk__in=self.initial['event_dates']) | Q(event_date__gte=date.today()))
    #     else:
    #         self.fields['event_dates'].queryset = EventDate.objects.filter(event_date__gte=date.today())

@admin.register(QualTake)
class QualTakeAdmin(admin.ModelAdmin):
    pass
    # form = QualTakeAdminForm

@admin.register(MainQueue)
class MainQueueAdmin(admin.ModelAdmin):
    pass
    # form = QualTakeAdminForm

@admin.register(PlayerQualTake)
class PlayerQualTakeAdmin(admin.ModelAdmin):
    pass

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass

@admin.register(EasterEggPlayer)
class EasterEggPlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(QualQueue)
class QualQueueAdmin(admin.ModelAdmin):
    pass

