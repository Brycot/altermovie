"""
    Views for Visual Prod
"""

import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.db.models import Prefetch
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import VisualProd, UserInteraction
from .forms import RateVideoProduction
# ============================================
# Routes for Audiovisual Producctions
# ============================================


def get_random_visualprod(request):
    """
        Get Random Movie/Serie
    """
    count = VisualProd.objects.count()
    num_aleatorio = random.randint(0, count)
    visual_prod = model_to_dict(VisualProd.objects.get(id=num_aleatorio))
    return JsonResponse(visual_prod)


def get_all_visualprods(request):
    """
    Get All Movies/Series or Get All filtered
    """
    type = request.GET.get('type') or ''
    name = request.GET.get('name') or ''
    genre = request.GET.get('genre') or ''

    if type or name or genre:
        visual_prods = VisualProd.objects.filter(
            type__contains=type, name__contains=name, genre__contains=genre)
        visual_prods = list(visual_prods.values())
        return JsonResponse(visual_prods, safe=False)

    visual_prods = list(VisualProd.objects.values())
    return JsonResponse(visual_prods, safe=False)


def get_order_visualprods(request, type_prod, order):
    """
        Get All Movies/Series ordered by Type and param
    """
    visual_prods_db = VisualProd.objects.filter(
        type=type_prod).order_by(order).values()
    visual_prods_ordered = list(visual_prods_db)
    return JsonResponse(visual_prods_ordered, safe=False)

# ============================================
# Routes for Auth
# ============================================


def signup(request):
    if request.method == "GET":
        return render(request, 'auth/signup.html', {
            'form': UserCreationForm
        })

    if request.POST['password1'] == request.POST['password2']:
        try:
            # register user
            new_user = User.objects.create_user(
                username=request.POST['username'], password=request.POST['password1'])
            new_user.save()
            login(request, new_user)
            return redirect('home')
        except IntegrityError:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                "error": "Username already exists"
            })

    return render(request, 'auth/signup.html', {
        'form': UserCreationForm,
        "error": "Passwords don't match"
    })


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == "GET":
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })

    user = authenticate(
        request, username=request.POST['username'], password=request.POST['password'])
    if user is None:
        return render(request, 'auth/signin.html', {
            'form': AuthenticationForm,
            "error": "Username or password incorrect"
        })
    login(request, user)
    return redirect('productions')

# ============================================
# Routes for User Interactions
# ============================================


def mark_viewed(request, id):
    visual_prod = get_object_or_404(VisualProd, id=id)
    user_interaction, created = UserInteraction.objects.get_or_create(
        user=request.user, visual_prod=visual_prod)

    if not created and user_interaction.viewed:
        # If the user has already marked the visual_prod as viewed, return to home
        return redirect('productions')
    visual_prod.number_visualizations += 1
    visual_prod.save()
    user_interaction.viewed = True
    user_interaction.save()
    return redirect('productions')


def select_rate(request, id):
    count_rates = UserInteraction.objects.filter(
        visual_prod=id, rating__isnull=False).count()

    count_rates += 1

    rates = list(UserInteraction.objects.filter(
        visual_prod=id, rating__isnull=False).values_list('rating', flat=True))

    rate_visual_prod = sum(rates, int(request.POST['rate'])) / count_rates

    visual_prod = get_object_or_404(VisualProd, id=id)
    user_interaction, created = UserInteraction.objects.get_or_create(
        user=request.user, visual_prod=visual_prod)

    if not created and user_interaction.rating != None:
        return redirect('productions')

    visual_prod.rating = rate_visual_prod
    visual_prod.save()
    user_interaction.rating = request.POST['rate']
    user_interaction.save()
    return redirect('productions')

# Page Views


def home(request):
    return render(request, 'home.html')


def productions(request):

    visual_prods = list(VisualProd.objects.values())

    visual_prods_user = list(VisualProd.objects.filter(
        userinteraction__user=request.user
    ).prefetch_related(Prefetch('userinteraction_set', queryset=UserInteraction.objects.filter(user=request.user))))

    # Add Properties to visual_prods
    for visualprod in visual_prods_user:
        index = visual_prods.index(model_to_dict(visualprod))
        visual_prods[index] = {
            **visual_prods[index],
            'viewed': visualprod.userinteraction_set.filter(user=request.user).first().viewed,
            'ratingUser': visualprod.userinteraction_set.filter(user=request.user).first().rating,
        }

    return render(request, 'pages/productions.html', {
        'visual_prods': visual_prods,
        'rate_form': RateVideoProduction
    })


def movies(request):
    return render(request, 'pages/movies.html')


def series(request):
    return render(request, 'pages/series.html')


def random_production(request):
    return render(request, 'pages/random.html')
