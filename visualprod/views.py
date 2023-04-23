"""
    Views for Visual Prod
"""

import random
import requests
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
from .forms import RateVideoProduction, OrderProductions, SearchProductions
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


def get_user_interactions(request, id):
    """
        Get all user interactions
    """
    visual_prods = list(UserInteraction.objects.filter(
        user_id=id).values())
    visual_prods_user = list(
        VisualProd.objects.filter(userinteraction__user_id=id).values())
    return JsonResponse({'visual_prods': visual_prods, 'visual_prods_user': visual_prods_user}, safe=False)

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
        return render(request, 'auth/signin.html', {
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
    # return redirect('productions')
    return redirect(request.META.get('HTTP_REFERER'))


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
    return redirect(request.META.get('HTTP_REFERER'))

# Page Views


def home(request):
    return render(request, 'home.html')


def productions(request):
    visual_prods = []

    # if request.method == 'GET':
    #     response_visual = requests.get('http://127.0.0.1:3001/api/v1/items/')
    #     visual_prods = response_visual.json()
    # if request.method == 'POST':
    #     search = request.POST['search']
    #     response = requests.get(f'http://127.0.0.1:3001/api/v1/items/?name={search}')
    #     visual_prods = response.json()

    # response_user_interactions = requests.get(
    #     f'http://127.0.0.1:3001/api/v1/userinteractions/{request.user.id}')
    # user_interactions = response_user_interactions.json()

    # for interaction in user_interactions['visual_prods_user']:
    #     try:
    #         index = visual_prods.index(interaction)
    #         user_interaction = list(filter(
    #             lambda x: x['visual_prod_id'] == interaction['id'], user_interactions['visual_prods']))
    #         visual_prods[index] = {
    #             **visual_prods[index],
    #             'viewed': user_interaction[0]['viewed'],
    #             'ratingUser': user_interaction[0]['rating'],
    #         }
    #     except:
    #         continue

    return render(request, 'pages/productions.html', {
        'visual_prods': visual_prods,
        # 'rate_form': RateVideoProduction,
        # 'search_form': SearchProductions
    })


def movies(request):
    all_movies = []

    if request.method == 'GET':
        response = requests.get(
            'http://127.0.0.1:3001/api/v1/items/?type=movie')
        all_movies = response.json()
    if request.method == 'POST':
        order = request.POST['order_by']
        response = requests.get(
            f'http://127.0.0.1:3001/api/v1/items/Movie/{order}/')
        all_movies = response.json()

    response_user_interactions = requests.get(
        f'http://127.0.0.1:3001/api/v1/userinteractions/{request.user.id}')
    user_interactions = response_user_interactions.json()

    for interaction in user_interactions['visual_prods_user']:
        try:
            index = all_movies.index(interaction)

            user_interaction = list(filter(
                lambda x: x['visual_prod_id'] == interaction['id'], user_interactions['visual_prods']))

            all_movies[index] = {
                **all_movies[index],
                'viewed': user_interaction[0]['viewed'],
                'ratingUser': user_interaction[0]['rating'],
            }
        except:
            continue

    return render(request, 'pages/movies.html', {
        'movies': all_movies,
        'rate_form': RateVideoProduction,
        'order_form': OrderProductions
    })


def series(request):
    all_series = []
    if request.method == 'GET':
        response = requests.get(
            'http://127.0.0.1:3001/api/v1/items/?type=serie')
        all_series = response.json()
    if request.method == 'POST':
        order = request.POST['order_by']
        response = requests.get(
            f'http://127.0.0.1:3001/api/v1/items/Serie/{order}/')
        all_series = response.json()

    response_user_interactions = requests.get(
        f'http://127.0.0.1:3001/api/v1/userinteractions/{request.user.id}')
    user_interactions = response_user_interactions.json()

    for interaction in user_interactions['visual_prods_user']:
        try:
            index = all_series.index(interaction)

            user_interaction = list(filter(
                lambda x: x['visual_prod_id'] == interaction['id'], user_interactions['visual_prods']))

            all_series[index] = {
                **all_series[index],
                'viewed': user_interaction[0]['viewed'],
                'ratingUser': user_interaction[0]['rating'],
            }
        except:
            continue

    return render(request, 'pages/series.html', {
        'series': all_series,
        'rate_form': RateVideoProduction,
        'order_form': OrderProductions
    })


def random_production(request):
    response = requests.get('http://127.0.0.1:3001/api/v1/items/random')
    random_item = response.json()

    response_user_interactions = requests.get(
        f'http://127.0.0.1:3001/api/v1/userinteractions/{request.user.id}')

    user_interactions = response_user_interactions.json()

    user_interaction = list(filter(
        lambda x: x['visual_prod_id'] == random_item['id'], user_interactions['visual_prods']))

    if len(user_interaction) > 0:
        random_item = {
            **random_item,
            'viewed': user_interaction[0]['viewed'],
            'ratingUser': user_interaction[0]['rating'],
        }

    return render(request, 'pages/random.html', {
        'random_item': random_item,
        'rate_form': RateVideoProduction
    })
