from gallery.models import Tag

def init_tags():
    count = Tag.objects.all().count()
    print(">>> init_tags: ", count)
    if count == 0:
        tags = ['Cat','Dog','Animals',
            'Flowers','Scenery','Monkey',
             'Mammals','Lion','Human',
            'Rabbit', 'Gorilla', 'Bird',
             'Owl','Pig','Fish', 'Bear',
             'Reptile', 'Insect', "Sponge",
             'Elephant', 'Whale', 'Shark',
             'Penguin', "Wolf", 'Turtle',
             "Mouse", "Goose", "Kangaroo", 'plants']
        for tag in tags:
          Tag.objects.create(tag_name=tag)
