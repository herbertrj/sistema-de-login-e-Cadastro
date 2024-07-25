from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"), # principal de apresentacao
    path("cadastro/", views.cadastro, name="cadastro"), #tela de cadastro
    path("login/", views.login_view, name="login"), # tela de login
    path("logout/", views.logout_view, name="logout"),# tela apos o logout
    path("sistema/", views.sistema, name="sistema"),# tela de acesso ao sistema apos o login
    path("update/", views.user_update, name="user_update"),
]
