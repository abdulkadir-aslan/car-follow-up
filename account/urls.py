from django.urls import  path
from . import views

urlpatterns = [
    path("login",views.login_request,name="login"),
    path("logout",views.logout_request,name="logout"),
    path("register",views.register_request,name="register"),
    path("users_home",views.users_home,name="users_home"),
    path("user_delete/<int:myid>/",views.userDelete,name="user_delete"),
    path("update_user/<int:myid>/",views.updateUser,name="update_user"),
    path("register_edit/<int:myid>/",views.userEdit,name="register_edit"),
    path("Şifre_Güncelleme/<str:myid>/",views.update_password,name="update_password"),
]