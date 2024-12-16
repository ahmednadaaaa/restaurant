from django.urls import path, include
from .import views
from .views import MealListCreateView, MealDetailView

from django.contrib.auth import views as authViews

urlpatterns = [
    path('',views.index,name="index"),
    path('menu/', views.menu, name="menu"),
    path('service/', views.serv, name="service"),

    path('dashboard/', views.admin, name="dashboard"),
    path('dashboard/table/', views.table, name="table"),
    path('dashboard/meals/', views.meals, name="mealss"),
    path('dashboard/emp/', views.emp, name="emp"),
    path('dashboard/users/', views.users, name="users"),
    path('dashboard/messages', views.message, name="messages"),

    path('booking', views.booking, name="booking"),
    path('meal/<str:meal_id>', views.meal_detail, name='meal_detail'),
    path('contact/', views.contactus, name='contactus'),
    path('register/' ,views.register, name="register"),
    path('login/' ,views.userLogin, name="login"),
    path('logout/' ,views.userLogout, name="logout"),

    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('cart', views.cart, name='cart'),
    path('<int:orderdetails_id>', views.remove_from_cart, name='remove_from_cart'),
    path('add_qty/<int:orderdetails_id>', views.add_qty, name='add_qty'),
    path('sub_qty/<int:orderdetails_id>', views.sub_qty, name='sub_qty'),
    path('payment/', views.payment, name="payment"),

    path('reset_password/', authViews.PasswordResetView.as_view(template_name="password_reset.html"),
         name="reset_password"),
    path('reset_password_sent/',
         authViews.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         authViews.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         authViews.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),
         name="password_reset_complete"),

    path('meals/', MealListCreateView.as_view(), name='meal-list'),
    path('meals/<int:pk>/', MealDetailView.as_view(), name='meal-detail'),
    
]