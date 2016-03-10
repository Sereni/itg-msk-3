# coding=utf-8
from annoying.decorators import render_to
from special_random.main.models import QualTake, Track, QualQueue, Player, SongTake, TakeOption
# from special_random.main.models import SongsSet, PlayersGroup, SongTake, TakeOption, Player, BanedSongs
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# @render_to('sets.djhtml')
# def sets(request):
#     return {'sets': SongsSet.objects.all()}

@render_to('index.djhtml')
def index(request):
    return {}
    # return {'sets': SongsSet.objects.all()}

@render_to('qualifying.djhtml')
def qualifying(request):
    return {}
    # return {'sets': SongsSet.objects.all()}

@render_to('qualifying_d.djhtml')
def qualifying_d(request, diff):
    take, created = QualTake.objects.get_or_create(diff=diff)
    if created:
        tracks = Track.objects.filter(diff=diff).all().order_by('?')[:4]
        for track in tracks:
            take.songs.add(track)
        print tracks

    return {'diff':diff, "take": take}

@render_to('qualifying_q.djhtml')
def qualifying_q(request, diff, pk=False):
    take = QualTake.objects.get(diff=diff)
    q = QualQueue.objects.filter(qual_r=take).all()
    if len(q) == 0:
        return  {'diff':diff, "take": take}
    q = q[0]
    if pk:
        q = QualQueue.objects.get(pk=pk)
    # try:
    #     q = QualQueue.objects.filter(qual_r=take, pk=pk).all()[0]
    # except:
    #     qq = QualQueue(qual_r=take, player=Player.objects.get(pk=1), player_vs=Player.objects.get(pk=2), song=Track.objects.get(pk=1))
    #     qq.save()
    #
    #     qq2 = QualQueue(qual_r=take, player=Player.objects.get(pk=3), song=Track.objects.get(pk=2), prev=qq)
    #     qq2.save()
    #
    #     q = QualQueue.objects.filter(qual_r=take).all()[0]
# Найти всех кто в эту сложноть выбрали треки. И их выборы.
#
# Найти все 4 трека.
#
# Создать QQ по правилам:
# Каждый следующий трек не похож на прошлый по возмоности
# Игрок не играет несколько раз подряд.
# Делать список чойсов. Ставить ему скор. Выбирать лучший по скору.


# Потом нужно выбрать так чтобы чуваки играли парами. Но не один чувак подряд много раз.
# Условия такие: как можно больше игроков должны играть в паре, чтобы отбор прошёл быстрее. Желательно, чтобы треки чередовались: например, если только что играли BlaBlaBla, лучше следующим поставить что-то другое, чтоб зрители не скучали. Порядок должен быть хотя бы как-то похож на рандом, чтобы какие-то чуваки не играли постоянно в начале, а какие-то в конце.

    next = QualQueue.objects.filter(prev=q).all()
    if len(next)>0:
        next = next[0]

    return {'diff':diff, "take": take, "song": q.song, "q":q, "next": next}

@render_to('main.djhtml')
def main(request,  pk=False, take_pk=False):
    # если нет pk то генерим раунд
    # раунд это объект к которому привязано куча песен, и куча вычеркнутых песен
    if not pk:
        take = SongTake()
        take.save()
# - Рандомим 10 треков: по два из [9, 10, 11, 12, 13].
        for diff in [9, 10, 11, 12, 13]:
            random = Track.objects.filter(diff=diff).order_by('?')[:2]
            for item in random:
                # take.songs.add(item)
                op = TakeOption(song=item, songtake=take)
                op.save()#             op = TakeOption(song=song, songtake=take)
        return HttpResponseRedirect(
            reverse('main', args=[take.pk]))
    take = SongTake.objects.get(pk=pk)
# - Эти 4 трека перемешиваем и выстраиваем по порядку (нужен наглядный порядок, список или что-нибудь)
    if take_pk:
        ban = TakeOption.objects.get(pk=take_pk)
        print 'baaaan'
        if ban.banned is True:
            ban.banned = False
        else:
            ban.banned = True
        ban.save()
#     return {'group': PlayersGroup.objects.get(pk=group_pk),
#             'set': SongsSet.objects.get(pk=set_pk), 'takes': takes}

    return {'take':take}

@render_to('main_play.djhtml')
def main_play(request,  pk=False):
    take = SongTake.objects.get(pk=pk)
# - Эти 4 трека перемешиваем и выстраиваем по порядку (нужен наглядный порядок, список или что-нибудь)
    songs = take.takeoption_set.order_by('?').all()

    return {'take':take, 'songs': songs}
#
#
# @render_to('set.djhtml')
# def set(request, set_pk):
#     return { 'set': SongsSet.objects.get(pk=set_pk), 'set_pk': set_pk, 'groups': PlayersGroup.objects.all()} #нажатие на группу генерит новый набор песен для группы
#
#
# @render_to('random.djhtml')
# def random(request, set_pk, group_pk):
#     # создать take. редирект
#     takes = SongTake.objects.filter(group__pk=group_pk, songset__pk=set_pk)
#     if request.POST:
#         banned = BanedSongs.objects.filter(songset__pk=set_pk).values(
#             'song__pk')
#         need_songs = PlayersGroup.objects.get(pk=group_pk).players.count() + 1
#         songs = SongsSet.objects.get(pk=set_pk).songs.exclude(
#             pk__in=banned).all().order_by('?')[:need_songs]
#         if need_songs > SongsSet.objects.get(pk=set_pk).songs.exclude(
#                 pk__in=banned).all().count():
#             return {'group': PlayersGroup.objects.get(pk=group_pk),
#                     'set': SongsSet.objects.get(pk=set_pk), 'takes': takes,
#                     'no_more_songs': True}
#
#         take = SongTake()
#         take.songset = SongsSet.objects.get(pk=set_pk)
#         take.group = PlayersGroup.objects.get(pk=group_pk)
#         # take.songs.add()
#         take.save()
#
#         for song in songs:
#             op = TakeOption(song=song, songtake=take)
#             op.save()
#         return HttpResponseRedirect(
#             reverse('real_random', args=[take.pk, 'f', 'f']))
#     return {'group': PlayersGroup.objects.get(pk=group_pk),
#             'set': SongsSet.objects.get(pk=set_pk), 'takes': takes}
#
#
# @render_to('real_random.djhtml')
# def real_random(request, take_pk, ban_pk=False, player_pk=False):
#     # создать take. редирект
#     take = SongTake.objects.get(pk=take_pk)
#
#     try:
#         ban_pk = int(ban_pk)
#     except:
#         ban_pk = False
#
#     try:
#         last_chooser = int(player_pk)
#         prev_player = Player.objects.get(pk=last_chooser)
#
#     except:
#         last_chooser = False
#         prev_player = False
#
#     if ban_pk and last_chooser:
#         option = TakeOption.objects.filter(songtake=take.pk, song=ban_pk).get()
#         option.banned_by = prev_player
#         option.save()
#         banned_song = option.song
#     else:
#         banned_song = False
#
#     banned = take.songs.all().filter(takeoption__banned_by__isnull=False).values_list('takeoption__banned_by', flat=True)
#     players = take.group.players.exclude(pk__in=banned).order_by('?')
#     chooser = False
#     if len(players) >= 1:
#         chooser = players[0]
#     else:
#
#         if ban_pk == take.finish_song.pk:
#             ban = BanedSongs()
#             ban.song = take.finish_song
#             ban.songset = take.songset
#             ban.group = take.group
#             ban.take = take
#             ban.save()
#             return HttpResponseRedirect('/')
#
#     return {'take': take, 'players': players, 'player': chooser,
#             'prev_player': prev_player,
#             'banned': banned_song}
