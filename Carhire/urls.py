from django.urls import path
from . import views

from knox import views as knox_views
urlpatterns = [
    path('', views.Index, name='home'),
    path('car/view', views.CarView, name='car_view'),
    path('car/detail/<int:id>/', views.DetailView, name='car_detail'),
    path('car/book',views.book_car, name='reservation'),
    path('car/booking_detail/<int:id>/', views.booking_detail, name ='reservation_detail'),
    # path('booking/view', views.bookView, name='book_view'),
    path('login', views.login_api, name='login'),
    path('user', views.get_user_data, name='user'),
    path('register', views.register, name='register'),
    path('logout', knox_views.LogoutView.as_view()),
    path('logout/all', knox_views.LogoutAllView.as_view()),
    path('search', views.get_objects),
    path('car/search', views.get_car),
]