"""
    Urls for project
"""

from django.urls import path
from visualprod import views

urlpatterns = [
    # Auth URLS
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),

    # Items URLS
    path('api/v1/items/', views.get_all_visualprods, name='all'),
    path('api/v1/items/random/', views.get_random_visualprod, name='random'),
    path('api/v1/items/<str:type_prod>/<str:order>/', views.get_order_visualprods, name='order'),
    
    # User interaction URLS
    path('api/v1/userinteractions/<int:id>/',views.get_user_interactions, name='userinteractions'),
    path('api/v1/userinteractions/viewed/<int:id>/',views.mark_viewed, name='viewed'),
    path('api/v1/userinteractions/rate/<int:id>/',views.select_rate, name='rate'),

    # Page URLS
    path('', views.home, name='home'),
    path('productions/', views.productions, name='productions'),
    path('movies/', views.movies, name='movies'),
    path('series/', views.series, name='series'),
    path('random_production/', views.random_production, name='random_production'),

]
