from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product, Review , Category
from django.shortcuts import get_object_or_404
from .forms import ReviewForm
from .models import CartItem
from django.contrib.auth.views import LoginView
from .forms import RegisterForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cart
from django.contrib import messages
from .forms import ContactForm
from django.db.models import Q


from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse 
from urllib import request




@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user 
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all() 
    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,       
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.review_set.all()
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'reviews': reviews,
    })

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()
    return render(request, 'shop/add_review.html', {'form': form, 'product': product})

def search_by_category(request):
    category_name = request.GET.get('category', '')
    categories = Category.objects.all()
    
    products = Product.objects.filter(category__name__icontains=category_name) if category_name else []
    
    return render(request, 'shop/search.html', {
        'products': products,
        'categories': categories,
        'selected': category_name
    })
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    quantity = int(request.POST.get('quantity', 1)) 

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()

    messages.success(request, f"تم إضافة {quantity} × {product.name} إلى سلة الشراء.")
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart = request.user.cart
    items = cart.items.select_related('product')
    total_price = sum(item.product.price * item.quantity for item in items)

    return render(request, 'shop/cart.html', {
        'items': items,
        'total_price': total_price
    })

@login_required
def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    CartItem.objects.filter(cart=cart, product_id=product_id).delete()
    return redirect('view_cart')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  
            user.save()
            return redirect('login') 
    else:
        form = RegisterForm()
    return render(request, 'shop/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'shop/login.html'
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True

@login_required
def profile_view(request):
    user_products = Product.objects.filter(user=request.user)
    return render(request, 'shop/profile.html', {'products': user_products})


@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, user=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProductForm(instance=product)

    return render(request, 'shop/edit_product.html', {'form': form})
@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id, user=request.user)
    product.delete()
    return redirect('profile')



@receiver(post_save, sender=User)
def create_cart_for_new_user(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)


@login_required
def checkout(request):
    cart = request.user.cart
    items = cart.items.select_related('product')
    total_price = sum(item.product.price * item.quantity for item in items)
    cart.items.all().delete()

    return render(request, 'shop/checkout.html', {
        'items': items,
        'total_price': total_price
    })

def contact_view(request):
    return render(request, 'shop/contact.html')

def home_view(request):
    return render(request, 'shop/product_list.html')

from django.contrib import messages

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks! We will get back to you soon.")
            return redirect('product_list')
    else:
        form = ContactForm()
    return render(request, 'shop/contact.html', {'form': form})

def search_by_name(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)
    categories = Category.objects.all()
    return render(request, 'shop/product_list.html', {  
        'products': products,
        'categories': categories,
        'search_term': query
    })
