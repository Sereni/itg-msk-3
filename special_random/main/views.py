# coding=utf-8
from annoying.decorators import render_to
from special_random.main.models import QualTake, Track, QualQueue, Player, SongTake, TakeOption, PlayerQualTake, EasterEggPlayer, MainQueue
# from special_random.main.models import SongsSet, PlayersGroup, SongTake, TakeOption, Player, BanedSongs
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

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
        tracks = Track.objects.filter(diff=diff, songset__round='Main').all().order_by('?')[:4]
        for track in tracks:
            take.songs.add(track)

        for player in Player.objects.all():
            PlayerQualTake.objects.get_or_create(player=player)
                                                 # , qual_r=take)
        # print tracks

    return {'diff':diff, "take": take}

@render_to('qualifying_q.djhtml')
def qualifying_q(request, diff, pk=False):
    take = QualTake.objects.get(diff=diff)
    q = QualQueue.objects.filter(qual_r=take).all()
    if len(q) == 0:
        queue = []

        players = Player.objects.all()
        for player in players:
            p_t = PlayerQualTake.objects.get(player=player)
            for track in p_t.song.filter(diff=diff):
                queue.append((track, player, None))

        # len queue = кол-во игроков
        # [(<Track: Dustup (9)>, <Player: Pewpew>, None),
        #  (<Track: Hot Air Balloon (9)>, <Player: Neko Atsume>, None),
        #  (<Track: Dustup (9)>, <Player: AmikPusheen>, None),
        #  (<Track: Dustup (9)>, <Player: NoPhotoTest>, None)]
        import random
        random.shuffle(queue)

        # как можно больше игроков должны играть в паре
        def reduce_vs(queue):
            not_full = filter(lambda x: not x[2], queue)
            # print not_full
            for item in not_full:
                can_merge = filter(lambda x: x[0] == item[0],
                                   filter(lambda x: x[1] != item[1], not_full) # filter self
                                   )
                if len(can_merge) > 0:
                    merge = can_merge[0]
                    queue.remove(item)
                    queue.remove(merge)
                    queue.append((
                        item[0],
                        item[1],
                        merge[1]
                    ))
                    return queue, True
            return queue, False

        recall = True
        while recall:
            queue, recall = reduce_vs(queue)

        queue.reverse()

        #  # Каждый следующий трек не похож на прошлый по возмоности
        best_n = len(queue)
        import copy
        best = copy.copy(queue)
        from itertools import permutations, groupby
        for give_me_a_try in permutations(queue):
            track_seq = map(lambda x: x[0], give_me_a_try)
            n = max([len(list(group)) for key, group in groupby(track_seq)])
            if n < best_n:
                best = give_me_a_try
                best_n = n
            if best_n == 1:
                break

        queue = best

        current = False
        for object in queue:
            q = QualQueue(song=object[0], qual_r=take, player=object[1])
            if object[2]:
                q.player_vs = object[2]
            if current:
                q.prev = current
            q.save()
            current = q

        return HttpResponseRedirect(
            reverse('qualifying_q', args=[diff]))

    q = q[0]
    if pk:
        q = QualQueue.objects.get(pk=pk)

    next = QualQueue.objects.filter(prev=q).all()
    if len(next)>0:
        next = next[0]

    all_easter = EasterEggPlayer.objects.all()
    players = {}

    def get_key(player, player_vs):
        return ' '.join(map(
            lambda x: str(x), sorted([player, player_vs])
        ))
    for easter in all_easter:
        players[get_key(easter.player.pk, easter.player_vs.pk)] = easter

    one_photo = False
    if q.player_vs:
        one_photo = players.get(get_key(q.player.pk, q.player_vs.pk), False)

    return {'diff':diff, "take": take, "song": q.song, "q":q, "next": next, "one_photo": one_photo}


@render_to('main_q.djhtml')
def main_q(request, pk=False):
    q = MainQueue.objects.filter().all()

    if len(q) == 0:
        return {}
    q = q[0]
    if pk:
        q = MainQueue.objects.get(pk=pk)

    next = MainQueue.objects.filter(prev=q).all()
    if len(next)>0:
        next = next[0]

    all_easter = EasterEggPlayer.objects.all()
    players = {}

    def get_key(player, player_vs):
        return ' '.join(map(
            lambda x: str(x), sorted([player, player_vs])
        ))
    for easter in all_easter:
        players[get_key(easter.player.pk, easter.player_vs.pk)] = easter

    one_photo = False
    if q.player_vs:
        one_photo = players.get(get_key(q.player.pk, q.player_vs.pk), False)

    return {"q":q, "next": next, "one_photo": one_photo}



@render_to('main.djhtml')
def main(request,  pk=False, take_pk=False):
    # если нет pk то генерим раунд
    # раунд это объект к которому привязано куча песен, и куча вычеркнутых песен
    if not pk:
        take = SongTake()
        take.save()
# - Рандомим 10 треков: по два из [9, 10, 11, 12, 13].
        for diff in [9, 10, 11, 12, 13]:
            random = Track.objects.filter(diff=diff, songset__round='Main').order_by('?')[:2]
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
        if ban.banned is True:
            print 'baaaan'
            ban.banned = False
        else:
            ban.banned = True
        ban.save()
#     return {'group': PlayersGroup.objects.get(pk=group_pk),
#             'set': SongsSet.objects.get(pk=set_pk), 'takes': takes}

    return {'take':take, 'with_animations': settings.WITH_ANIMATION}

@render_to('main_play.djhtml')
def main_play(request,  pk=False):
    take = SongTake.objects.get(pk=pk)
# - Эти 4 трека перемешиваем и выстраиваем по порядку (нужен наглядный порядок, список или что-нибудь)
    songs = take.takeoption_set.filter().order_by('?').all()

    return {'take':take, 'songs': songs}


@render_to('main.djhtml')
def third(request,  pk=False, take_pk=False):
    # если нет pk то генерим раунд
    # раунд это объект к которому привязано куча песен, и куча вычеркнутых песен
    if not pk:
        take = SongTake()
        take.save()
# - Рандомим 10 треков: по два из [9, 10, 11, 12, 13].
        for diff in [9, 10, 11, 12, 13]:
            random = Track.objects.filter(diff=diff, songset__round='Finals').order_by('?')[:2]
            for item in random:
                # take.songs.add(item)
                op = TakeOption(song=item, songtake=take)
                op.save()#             op = TakeOption(song=song, songtake=take)
        return HttpResponseRedirect(
            reverse('third', args=[take.pk]))
    take = SongTake.objects.get(pk=pk)
# - Эти 4 трека перемешиваем и выстраиваем по порядку (нужен наглядный порядок, список или что-нибудь)
    if take_pk:
        ban = TakeOption.objects.get(pk=take_pk)
        if ban.banned is True:
            ban.banned = False
        else:
            ban.banned = True
        ban.save()
#     return {'group': PlayersGroup.objects.get(pk=group_pk),
#             'set': SongsSet.objects.get(pk=set_pk), 'takes': takes}

    return {'take':take, 'with_animations': settings.WITH_ANIMATION}

@render_to('main.djhtml')
def final(request,  pk=False, take_pk=False):
    # если нет pk то генерим раунд
    # раунд это объект к которому привязано куча песен, и куча вычеркнутых песен
    if not pk:
        take = SongTake()
        take.save()
# - Рандомим 10 треков: по два из [9, 10, 11, 12, 13].
        for diff in [9, 10, 11, 12, 13]:
            random = Track.objects.filter(diff=diff, songset__round='Finals').order_by('?')[:2]
            for item in random:
                # take.songs.add(item)
                op = TakeOption(song=item, songtake=take)
                op.save()#             op = TakeOption(song=song, songtake=take)
        return HttpResponseRedirect(
            reverse('final', args=[take.pk]))
    take = SongTake.objects.get(pk=pk)
# - Эти 4 трека перемешиваем и выстраиваем по порядку (нужен наглядный порядок, список или что-нибудь)
    if take_pk:
        ban = TakeOption.objects.get(pk=take_pk)
        if ban.banned is True:
            ban.banned = False
        else:
            ban.banned = True
        ban.save()
#     return {'group': PlayersGroup.objects.get(pk=group_pk),
#             'set': SongsSet.objects.get(pk=set_pk), 'takes': takes}

    return {'take':take, 'with_animations': settings.WITH_ANIMATION}
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
