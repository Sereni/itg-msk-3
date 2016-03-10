from django.core.management.base import BaseCommand, CommandError
from special_random.main.models import SongsSet
from django.core.files.base import ContentFile
# from django.db import transaction


class Command(BaseCommand):
    args = '<set_filename>'
    help = 'Load the specified set'

    # @transaction.commit_manually()
    def handle(self, *args, **options):
        from special_random import k_utils

        sset = SongsSet()
        sset.title = args[0]
        sset.save()

        k_utils.import_pack(args[0], sset)
        # try:
        #     filename = args[0]
        #     self.stdout.write(filename+':')
        # except:
        #     raise CommandError('>: set filename?')
        #
        # if SongsSet.objects.filter(title=filename).count() > 0:
        #     raise CommandError('Set with title %s exists.' % filename)
        # sset = SongsSet()
        # sset.title = filename
        # sset.save()
        #
        # f = open(filename)
        # for line in f.readlines():
        #     self.stdout.write(line)
        #     title, difficulty = line.split('|')
        #     self.stdout.write(' '.join((title, difficulty)))
        #     song = Song()
        #     song.title = title
        #     song.difficulty = difficulty
        #     stitle = title.replace(' ', '-')
        #     baner_file = '{0}/{1}-bn.jpg'.format(filename.split('.')[0], stitle)
        #     self.stdout.write(baner_file)
        #     binary = open(baner_file).read()
        #     song.banner.save('{0.title}|{0.difficulty}.jpg'.format(song),
        #                                        ContentFile(binary))
        #     song.save()
        #
        #
        #     sset.songs.add(song)
        # f.close()
        # transaction.commit()

