


#
# MOVED TO PRODUCTS 6/10/12  JJW
#



# 1.2.x:
#from haystack.indexes import *
#from haystack import site

# 2.0.0b:
from haystack import indexes

from legacy.models import Product, Categories


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
    # upd 9/22/13 JJW
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
    # upd 9/22/13 JJW
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return Categories.objects.published()  # filter(pub_date__lte=datetime.datetime.now())
