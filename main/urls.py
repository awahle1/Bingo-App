from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("boards", views.boards, name="boards"),
    path("boardmaker", views.boardmaker, name ="boardmaker"),
    path("createBoard", views.createBoard, name ="createBoard"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("toSignUp", views.toSignUp_view, name="toSignUp"),
    path("signUp", views.signUp_view, name="signUp"),
    path('bingo', views.bingo, name="bingo"),
    path('showbingos', views.showbingos, name="showbingos"),
    path('getbingos', views.getbingos, name="getbingos"),
    path('feed', views.feed, name="feed"),
    path('search', views.search, name="search"),
    path('runsearch', views.runsearch, name="runsearch"),
    path('getuserbingos', views.getuserbingos, name="getuserbingos"),
    path('follow', views.follow, name="follow"),
    path('boards/<str:username>', views.userprofile),
    path('bingos/<str:username>', views.showuserbingos, name="showuserbingos"),
    path('isfollowing', views.isfollowing, name="isfollowing"),
    path('delete/<str:id>', views.delete),
]
