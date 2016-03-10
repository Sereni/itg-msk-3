from django.core.management.base import BaseCommand, CommandError
from special_random.main.models import Player
from django.core.files.base import ContentFile
# from django.db import transaction


class Command(BaseCommand):

    # @transaction.commit_manually()
    def handle(self, *args, **options):
        cats = ['My', 'Neko Atsume', 'Pusheen']
        for cat in cats:
            p = Player(username=cat)
            if cat == 'My':
                binary = open('fake/' + cat + '.jpg').read()
            else:
                binary = open('fake/' + cat + '.png').read()
            p.photo.save('{0}.png'.format(cat),
                                               ContentFile(binary))
            p.save()
        # try :
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

