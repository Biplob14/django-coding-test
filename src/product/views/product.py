from django.views import generic
from django.utils import timezone
from django.views.generic import ListView
from product.models import Variant
from product.forms import ProductForm
from product.models import Product, ProductVariant


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

#######################################
class ProductsView(ListView):
    form_class = ProductForm
    # model = Product
    template_name = 'products/list.html'
    # context_object_name = 'title__icontains'
    paginate_by = 3
    # success_url = '/product/list'

    def get_queryset(self):
        filter_string = {}
        for key in self.request.GET:
            print("get key: ", key)
            if self.request.GET.get(key):
                if key != 'page':
                    filter_string[key] = self.request.GET.get(key)
            
        #  http://127.0.0.1:8000/product/list/?title__icontains=a&productvariant__variant_title__icontains=m&productvariantprice__price
        queryset = Product.objects.filter(**filter_string)
        # queryset = Product.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        variants = Variant.objects.all()
        product_variant = ProductVariant.objects.values('variant_title').distinct()
        # product_price = ProductVariantPrice.objects.filter(price__range())
        # print("price from: ", context['price_from'])

        context['product_variant_list'] = product_variant
        context['variants'] = variants
        context['product'] = True
        context['request'] = ''
        context['current_time'] = timezone.now()
        # if self.request.GET:
        #     context['request'] = self.request.GET['title__icontains']
        print("in context: ", context["product"])
        return context
    