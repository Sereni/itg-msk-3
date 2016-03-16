# coding=utf8
import os
import re
import csv

#os.environ['DJANGO_SETTINGS_MODULE'] = 'itg.settings'  # apps aren't loaded yet

# import django  # app_label error
# from django.conf import settings
# if not settings.configured:
#     settings.configure()
# django.setup()

from .main.models import Track

# from django.apps import AppConfig

TITLE = re.compile(r'#TITLE:(.+?);')
AUTHOR = re.compile(r'#ARTIST:(.+?);')
BANNER = re.compile(r'#BANNER:(.+?);')
BPM = re.compile(r'#BPMS:(.+?);')  # fixme doesn't work with multiline
CHART = re.compile(r'Challenge:.*', re.DOTALL)
# CHART = re.compile(r'#NOTES:(.+?);')
STOPS = re.compile(r'#STOPS:(.+?)')


def get_bpms(s):
    """
    Parse the BPM string and determine min and max BPM
    :param s: string containing BPM information from simfile
    """
    bpms = sorted([round(float(point.split('=')[-1])) for point in s.split(',')])
    return bpms[0], bpms[-1]


def get_info(s):
    """
    Parse chart string and extract data
    :param s: string containing chart information
    """
    data = s.split([':'])
    style = data[0].split('-')[-1]
    difficulty = data[2]
    num = int(data[3])
    return style, difficulty, num


def process_track(path, sset):
    """
    Create track and stepchart info from .sm file
    :param path: path to .sm file
    :param sset: name of pack
    """
    with open(path) as sm:
        simfile = sm.read()

        # get track info
        title = re.search(TITLE, simfile).group(1)
        author = re.search(AUTHOR, simfile).group(1)
        try:
            banner = None
            banner = re.search(BANNER, simfile).group(1)
        except:
            print 'Не нашел секцию BANNER в файле ', title, path
        try:
            bpm_string = re.search(BPM, simfile).group(1)
        except:
            bpm_string = '0'
        min_bpm, max_bpm = get_bpms(bpm_string)

        charts = re.findall(CHART, simfile)
        # print charts
        diff = charts[0].split('Challenge:')[1].split(':')[0].strip()
        # print diff

        # save track
        track, created = Track.objects.get_or_create(
            name=title,
            author=author,
            songset=sset,
            min_bpm=min_bpm,
            max_bpm=max_bpm,
            diff=diff,
        )
        filename = path
        stitle = title
        from django.core.files.base import ContentFile
        # self.stdout.write(baner_file)
        try:
            baner_file = '/'.join(filename.split('.')[0].split('/')[0:-1]) + '/' + title + '.png'
            if banner is not None:
                baner_file = '{0}/{1}'.format('/'.join(filename.split('.')[0].split('/')[0:-1]), banner)
            binary = open(baner_file).read()
            track.banner.save('{0}'.format(banner),
                                           ContentFile(binary))
        except:
            if banner is  None:
                print 'mew :( ', baner_file, path
                track.delete()

        # print charts
        # for chart in charts:
        #     style, diff_text, diff_num = get_info(chart)
        #     chart_obj, created = Stepchart.objects.get_or_create(
        #         track=track,
        #         diff_num=diff_num,
        #         diff_text=diff_text,
        #         style=style
        #     )


def import_pack(path, sset):
    """
    Import all songs located in a given pack
    :param path: path to song pack
    """
    pack = os.path.basename(path)
    tracks = os.listdir(path)
    for track in tracks:

        # if this is a track directory, process track
        track_dir = os.path.join(path, track)
        if os.path.isdir(track_dir):
            files = os.listdir(track_dir)
            for f in files:
                if f.lower().endswith('.sm'):  # todo add support for .ssc?

                    # this will open .sm and pull stepchart info
                    # track is also created there
                    process_track(os.path.join(track_dir, f), sset=sset)


def get_bpms_unrounded(s):
    bpms = sorted([float(point.split('=')[-1]) for point in s.split(',')])
    return bpms[0], bpms[-1]

def get_sync_info(path):
    """
    Given a path to .sm file, read it and get:
    bpm change or float bpm | stops | name | author | difficulty
    """
    bpm_change = False  # assume constant bpm
    float_bpm = False

    with open(path) as sm:
        simfile = sm.read().replace('\n', ' ')  # this is an ugly hack, don't use it in database

        # get track info
        title = re.search(TITLE, simfile).group(1)
        author = re.search(AUTHOR, simfile).group(1)
        bpm_string = re.search(BPM, simfile).group(1)
        stops = re.search(STOPS, simfile).group(1)
        min_bpm, max_bpm = get_bpms_unrounded(bpm_string)

        if min_bpm != max_bpm:
            bpm_change = True

        if round(max_bpm) != max_bpm:
            float_bpm = True

        first_cell = ''
        if bpm_change:
            first_cell += 'ch '
        if float_bpm:
            first_cell += 'fl'
        if stops != ';':
            stops = 'st'
        else:
            stops = ''

#        chart = re.findall(CHART, simfile)[-1]  # for files with multiple difficulties, most likely last one
 #       style, diff_text, diff_num = get_info(chart)

    return (first_cell, stops, title, author, '')


def process_pack_sync(path):
    """
    Processes pack for sync purposes.
    Analyze all simfiles in the pack and output to csv:
    bpm change or float bpm | stops | name | author | difficulty
    """
    out = open('sync_info.csv', 'w')
    w = csv.writer(out, delimiter=';')

    tracks = os.listdir(path)
    for track in tracks:
        track_dir = os.path.join(path, track)
        if os.path.isdir(track_dir):
            files = os.listdir(track_dir)
            for f in files:
                if f.endswith('.sm'):
                    row = get_sync_info(os.path.join(track_dir, f))
                    w.writerow(row)
                    print('Processed file: %s' % row[2])

# process pack sync is a different kind of parser I needed for syncing the tracklist.
# in the same file, yes.
# process_pack_sync('/Users/Sereni/Downloads/ITG Moscow Tournament 3')


# import_pack('/Applications/StepMania/Songs/Ideal Sync')