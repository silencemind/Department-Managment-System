from django.urls import path
#from .views import HomePageView
from . import views
urlpatterns = [
		# path('',views.login,name='login'),
    path('hod_index/', views.hods, name='hods'),
	path('logout/', views.logOut, name='logOut'),

]