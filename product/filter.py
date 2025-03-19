import django_filters

from .models import Product



#filtrer le produit selon des données spécifiques.
#keyword faire un recherche  avec le nom du produit
class ProductsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')
    keyword = django_filters.filters.CharFilter(field_name="name",lookup_expr="icontains")
    minPrice = django_filters.filters.NumberFilter(field_name="price" or 0,lookup_expr="gte")
    
    class Meta:
        model = Product
       # fields = ['category', 'brand'] #selon le prix et le date ou bien  category on peut choisir selon quoi !
        fields = ('category','brand','keyword','minPrice')
        