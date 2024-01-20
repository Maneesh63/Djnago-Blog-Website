from django.urls import path
from . import views


urlpatterns=[
    path('',views.home,name='home'),

   path('signup/', views.signup, name='signup'),

    path('login/',views.login,name='login'),

    path('logout/',views.logout,name='logout'),

    path('create/',views.create,name='create'),

    path('post_list/',views.post_list,name='list'),

    path('update_post/<int:post_id>/', views.update_post, name='update_post'),

    path('individual_post/<int:post_id>/', views.individual_post, name='individual_post'),

    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
 
    path('test/',views.test,name='test'),

    path('search/',views.search,name='search'),

    path('dashboard/<int:user_id>/',views.dashboard,name='dashboard'),

    path('post_like/<int:post_id>/', views.post_like , name='like'),

     

]

