from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Image

@registry.register_document
class ImageDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'image_index'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 1}

    class Django:
        model = Image

        fields = [
            'id',
            'image_name',
            'image_desc',
        ]

        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        # ignore_signals = True
        # Don't perform an index refresh after every update (overrides global setting):
        # auto_refresh = False
        # Paginate the django queryset used to populate the index with the specified size
        # (by default there is no pagination)
        # queryset_pagination = 5000
