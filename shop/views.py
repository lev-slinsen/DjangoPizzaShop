"""
Page views.
"""
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .bepaid import Bepaid
from .models import OrderItem, Order, PageTextGroup, File
from .forms import OrderForm, LunchForm

from catalog.models import Pizza
from accounts.models import User
from accounts.forms import UserCreationForm
from timetable.models import Date


def home(request):
    """
    Home page view.
    """
    template_name = 'shop/home.html'
    pizzas = Pizza.objects.filter(is_active=True)
    context = {
        'pizzas': pizzas
    }
    return render(request, template_name, context)


def about(request):
    """
    About page view.
    """
    template_name = 'shop/about.html'
    path = request.path.strip('/')
    text_group = PageTextGroup.objects.filter(page_name=path).first()
    if text_group is None:
        context = {'text': text_group}
    else:
        variables = [(text.text_name, text.text) for text in text_group.texts.all()]
        context = {'text': text_group, **dict(variables)}
    return render(request, template_name, context)


def lunch(request):
    template_name = 'shop/lunch.html'
    form = LunchForm(request.POST)
    path = request.path.strip('/')
    context = {'form': form}

    if request.method == 'GET':
        text_group = PageTextGroup.objects.filter(page_name=path).first()
        menu_link = File.objects.filter(name='lunch-menu').first().url() or None
        if text_group is None:
            context.update({'text': text_group})
        else:
            variables = [(text.text_name, text.text) for text in text_group.texts.all()]
            context.update({'text': text_group, **dict(variables)})
            context.update({'menu_file': menu_link})
        return render(request, template_name, context)

    elif request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Спасибо за обращение! Мы свяжемся с Вами в ближайшее время.')
            return HttpResponseRedirect(request.path_info)
        else:
            if settings.DEBUG:
                print(form.data)
                print('feedback is NOT valid')
            return HttpResponse(form.errors, content_type='application/json')


def cart(request):
    """
    Cart page view.
    """
    template_name = 'shop/cart.html'
    pizzas = Pizza.objects.all()
    context = {
        'pizzas': pizzas
    }
    return render(request, template_name, context)


def order(request):
    form = OrderForm(data=request.POST)
    if request.method == 'POST':
        mutable_request_data = request.POST.copy()
        order_items = json.loads(mutable_request_data.pop('order')[0])
        order_details = OrderForm(mutable_request_data)

        if order_details.is_valid():

            with transaction.atomic():
                if settings.DEBUG:
                    print('order is valid')

                order_obj = order_details.save()

                # create object OrderItem item for each item in the order
                for order_item in order_items:
                    item = Pizza.objects.get(id=order_item['id'])
                    params = dict(
                        order=order_obj,
                        item=item,
                        size=order_item['size'],
                        quantity=order_item['quantity'],
                    )
                    OrderItem.objects.create(**params)

                total_price = int(Order.objects.all().last().total_price()*100)
                bepaid = Bepaid()
                response_data = bepaid.bp_token(total_price)
            return HttpResponse(response_data, content_type='application/json')

        else:
            if settings.DEBUG:
                print('order is NOT valid')
            return HttpResponse('error', content_type='application/json')

    else:
        form = OrderForm()

    dates = Date.objects.all()
    dates_list = []
    for d in dates:
        date = str(d).replace('-', '/')
        dates_list.append(date)
    js_data = json.dumps(dates_list)
    return render(request, 'shop/order.html', {'form': form, "dates": js_data})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, f'You can log in now')
            return redirect('shop:shop-home')

    else:
        form = UserCreationForm()
    return render(request, 'shop/registration.html', {'form': form})


def profile(request):
    """
    User profile page view.
    """
    template_name = 'shop/profile.html'

    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('shop:shop-home')
        else:
            messages.error(request, f'Please correct errors {form.errors}.')
    else:
        form = PasswordChangeForm(request.user)

    user = User.objects.get(phone=request.user.phone)
    context = {
        'orders': Order.objects.filter(phone=user.phone),
        'form': form
    }

    return render(request, template_name, context)