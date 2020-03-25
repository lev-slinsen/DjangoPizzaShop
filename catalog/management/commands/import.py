import json
from django.core.management.base import BaseCommand, CommandError
from catalog.models import Pizza, Category, Size
from accounts.models import User


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('json_path')

    def handle(self, *args, **options):
        filename = options['json_path']
        try:
            with open(filename, 'r') as json_dump:
                data = json.load(json_dump)
        except FileNotFoundError:
            raise CommandError("Cannot open file `{}`".format(filename))

        items = data.get('items')
        if items:
            print('Loading items')
            for item in items:
                cat_ids = []
                categories = item.pop('categories')
                for cat in categories:
                    cat_id = Category.objects.get_or_create(name=cat)[0].id
                    cat_ids.append(cat_id)
                sizes = item.pop('sizes')
                photo = item.pop('photo')
                pizza, created = Pizza.objects.get_or_create(**item)
                pizza.category.add(*cat_ids)
                for size in sizes:
                    size['pizza'] = pizza
                    Size.objects.get_or_create(**size)
                with open(photo, "rb") as image:
                    filename = photo.split('/')[-1]
                    pizza.photo.save(filename, image)
        else:
            self.stdout.write('No Items field')

        users = data.get('users')
        if users:
            print('Loading users')
            for item in users:
                password = item.pop('password')
                user, created = User.objects.get_or_create(**item)
                user.set_password(password)
                user.save()
        else:
            self.stdout.write('No User field')
