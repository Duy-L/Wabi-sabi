from django.http import Http404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from carts.models import Cart
from .models import Product, ProductForm

User = get_user_model()

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


class ProductFeaturedListView(ListView):
	template_name = "products/featured-detail.html"

	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.active().featured()

class ProductFeaturedDetailView(DetailView):
	queryset = Product.objects.active().featured()
	template_name = "products/featured-detail.html"

#display ENTIRE SHOP
class ProductListView(ListView):
	template_name = "products/list.html"

	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.active()

def product_list_view(request):
	queryset = Product.objects.active()
	context = {
		'object_list': queryset
	}
	return render(request, "products/list.html", context)

#SORT FILTER (lowest price)
def product_by_price_lowest(request):
	queryset = Product.objects.active().order_by('price')
	context = {
		'object_list':queryset
	}
	return render(request, "products/price.html", context)

#SORT FILTER (highest price)
def product_by_price_highest(request):
	queryset = Product.objects.active().order_by('-price')
	context = {
		'object_list':queryset
	}
	return render(request, "products/price.html", context)

#SORT FILTER (oldest date created)
def product_by_date_oldest(request):
	queryset = Product.objects.active().order_by('timestamp')
	context = {
		'object_list':queryset
	}
	return render(request, "products/price.html", context)

#SORT FILTER (latest date created)
def product_by_date_newest(request):
	queryset = Product.objects.active().order_by('-timestamp')
	context = {
		'object_list':queryset
	}
	return render(request, "products/price.html", context)

#display CURRENT USER's products
class UserProductListView(ListView):
	template_name = "products/user_list.html"

	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.all().order_by('-timestamp')


def user_product_list_view(request):
	queryset = Product.objects.all()
	context = {
		'object_list': queryset
	}
	return render(request, "products/user_list.html", context)

#display ANOTHER USER'S products
def user_profile_list_view(request, author):
	queryset = Product.objects.active()
	context = {
		'object_list': queryset,
		'author': author
	}
	return render(request, "products/user_profile.html", context)

#Create new Product
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['title', 'brand', 'article', 'image', 'description', 'price' ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProductDetailSlugView(DetailView):
	queryset = Product.objects.active()
	template_name = "products/detail.html"

	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
		cart_obj, new_obj = Cart.objects.new_or_get(self.request)
		context['cart']= cart_obj
		return context

	def get_object(self, *args, **kwargs):
		request = self.request
		slug = self.kwargs.get('slug')
		#instance = get_object_or_404(Product, slug=slug, active=True)
		try:
			instance = Product.objects.get(slug=slug)
		except Product.DoesNotExist:
			raise Http404("Not found")
		except Product.MultipleObjectsReturned:
			qs = Product.objects.filter(slug=slug)
			instance = qs.first()
		except:
			raise Http404("Ummm")
		return instance

#Edit a Product
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['title', 'brand', 'article', 'image', 'description', 'price']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def product_update_view(request, slug):
	obj = get_object_or_404(Product, slug = slug)
	product_form = ProductForm(instance=obj)
	if product_form.is_valid():
			print(product_form.cleaned_data)
			product_form.author = request.user
	context = {
		"title":"Contact Page",
		"content":"Welcome to the new product page.",
		"form": product_form,
	}
	return render(request, "products/product_form.html", context)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
		
#delete product
def product_delete_view (request,  slug):
	obj = get_object_or_404(Product, slug = slug)
	obj.delete()
	queryset = Product.objects.all()
	context = {
		'object_list': queryset
	}
	return render(request, "products/user_list.html", context)
#Marks a product as "inactive" aka SOLD
def product_inactive_view (request,  slug):
	obj = get_object_or_404(Product, slug = slug)
	obj.active = False
	obj.buyer = request.user
	obj.save()
	return render(request, "products/user_list.html")

#display DETAILS of ONE PRODUCT
class ProductDetailView(DetailView):
	#queryset = Product.objects.all()
	template_name = "products/detail.html"

	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
		print(context)
		return context

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk')
		instance = Product.objects.get_by_id(pk)
		if instance is None:
			raise Http404("Product does not exist.")
		return instance


def product_detail_view(request, pk=None, *args, **kwargs):

	instance = Product.objects.get_by_id(pk)
	if instance is None:
		raise Http404("Product does not exist")

	context = {
		'object': instance
	}
	return render(request, "products/detail.html", context)
