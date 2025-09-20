from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
# urls.py

urlpatterns = [
    path('', views.home, name='home'),
    path('games/', views.games_index, name='index'),
    path('games/<int:game_id>', views.games_detail, name='detail'),
    path('games/create' ,views.GameCreate.as_view(), name='games_create'),
    path('games/<int:pk>/update/', views.GameUpdate.as_view(), name='games_update'),
    path('games/<int:pk>/delete/', views.GameDelete.as_view(), name='games_delete'),
    # path('games/<int:game_id>/add_feeding/', views.add_feeding, name='add_feeding'),



    # CBV's fpt Kids Model
    path('dashboard/', views.dashboard, name='dashboard'),
    # urls.py
    path('game_dashboard/<int:game_id>/', views.game_dashboard, name='game_dashboard'),


    path('kids/', views.KidList.as_view(), name='kid_index'),
    path('kids/<int:pk>/', views.KidDetail.as_view(), name='kid_detail'),
    path('kids/create/', views.KidCreate.as_view(), name='kid_create'),
    path('kids/<int:pk>/update/', views.KidUpdate.as_view(), name='kid_update'),
    path('kids/<int:pk>/delete/', views.KidDelete.as_view(), name='kid_delete'),

    path('kids/<int:kids_id>/assoc_kid/<int:game_id>/' , views.assoc_kid, name='assoc_kid'),
    path('kids/<int:kids_id>/unassoc_kid/<int:game_id>/' , views.unassoc_kid, name='unassoc_kid'),
    # ... To update the status after thime out
    path('update_kid_status/<int:kid_game_id>/', views.update_kid_status, name='update_kid_status'),
    path('nfc_generate/<str:hash>/<str:token>/', views.nfc_generate, name='nfc_generate'),
    path('accounts/signup/' , views.signup , name='signup')
   
]



