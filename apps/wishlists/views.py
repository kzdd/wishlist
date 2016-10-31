from django.shortcuts import render, redirect
from .models import Product
from ..logreg.models import User
from django.core.urlresolvers import reverse
from django.contrib import messages


def dashboard(request):
    if 'id' not in request.session:
        return redirect(reverse('login:index'))
    user = User.usrMgr.get(id=request.session['id'])
    context = {
        'products': user.product_set.all().exclude(adder__id=request.session['id']),
        'myproducts': Product.objects.filter(adder__id=request.session['id']),
        'otherproducts': Product.objects.exclude(users__id=request.session['id']),
    }
    return render(request, 'wishlists/dashboard.html', context)

def create(request):
    return render(request, 'wishlists/adding.html')

def add(request):
    if request.method != 'POST':
        return redirect(reverse('wishlists:dashboard'))
    pname = request.POST['product']
    if len(pname) < 3:
        messages.error('Product name must be longer than 3')
        return redirect(reverse('wishlists:create'))
    user = User.usrMgr.get(id=request.session['id'])
    try:
        p = Product.objects.get(name=pname)
    except:
        p = Product.objects.create(name=pname, adder=user)
    p.users.add(user)
    return redirect(reverse('wishlist:dashboard'))

def delete(request, id):
    try:
        p = Product.objects.get(id=id)
    except:
        return redirect(reverse('wishlist:dashboard'))
    #only creator can delete the item
    if p.adder.id != request.session['id']:
        return redirect(reverse('wishlist:dashboard'))
    p.delete()
    return redirect(reverse('wishlist:dashboard'))

def addproduct(request, id):
    try:
        p = Product.objects.get(id=id)
    except:
        return redirect(reverse('wishlist:dashboard'))
    user = User.objects.get(id=request.session['id'])
    p.users.add(user)
    return redirect(reverse('wishlist:dashboard'))

def removeproduct(request, id):
    try:
        p = Product.objects.get(id=id)
    except:
        return redirect(reverse('wishlist:dashboard'))
    user = User.objects.get(id=request.session['id'])
    p.users.remove(user)
    return redirect(reverse('wishlist:dashboard'))

def product(request, id):
    try:
        p = Product.objects.get(id=id)
    except:
        return redirect(reverse('wishlist:dashboard'))
    context = {
    'users': p.users.all(),
    'name': p.name,
    }
    return render(request, 'wishlists/product.html', context)
from django.shortcuts import render

# Create your views here.
