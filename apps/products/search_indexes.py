
# 1.2.x:
#from haystack.indexes import *
#from haystack import site

# 2.0.0b:
from haystack import indexes

from products.models import Product, Categories

# could move to its own quickpages/search_index.py
from quickpages.models import QuickPage


# 1.2.x:
#class ProductIndex(SearchIndex):

# 2.0.0b:
class ProductIndex (indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    #author = indexes.CharField(model_attr='user')
    #pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Product

    #def index_queryset(self):
    # Upd 9/22/13 for using=none
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return Product.objects.published()  # filter(pub_date__lte=datetime.datetime.now())

# 1.2.x:
#site.register(Product, ProductIndex)


class CategoryIndex (indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    #author = indexes.CharField(model_attr='user')
    #pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Categories

    #def index_queryset(self):
    # Upd 9/22/13 for using=none
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return Categories.objects.published()


class QuickPageIndex (indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    #author = indexes.CharField(model_attr='user')
    #pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return QuickPage

    #def index_queryset(self):
    # Upd 9/22/13 for using=none
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return QuickPage.objects.published()
