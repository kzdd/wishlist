from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.dateparse import parse_date
from .models import User


# Create your views here.
# initialing the main page(index page).
def index(request):
    if 'id' in request.session:
        return redirect(reverse('wishlist:dashboard'))
    return render(request, 'logreg/index.html')

#processing the login action
def process(request):
    if request.POST['form_button'] == 'Register':
        data = {
            'name': request.POST['name'],
            'username': request.POST['username'],
            'password': request.POST['password'],
            'confirm': request.POST['confirm'],
            'doh': parse_date(request.POST['doh'])
        }
        x = User.usrMgr.validation(data)
        if not x[0]:
            for errors in x[1]:
                messages.error(request, errors)
            return redirect(reverse('login:login'))
        request.session['id']= x[1].id
        return redirect(reverse('wishlist:dashboard'))

    elif request.POST['form_button'] == 'Login':
        data = {
            'username': request.POST['username'],
            'password': request.POST['password']
        }
        x = User.usrMgr.login(data)
        if not x[0]:
            for errors in x[1]:
                messages.info(request, errors)
            return redirect(reverse('login:login'))
        request.session['id']= x[1].id
        # request.seesion['name'] = user.name
        return redirect(reverse('wishlist:dashboard'))

# for logout from logged in secion
def logout(request):
    request.session.clear()
    return redirect(reverse('login:login'))
