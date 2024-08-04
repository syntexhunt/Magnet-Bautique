"""
URL configuration for Blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from home import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),


     path('froala_editor/',include('froala_editor.urls')),
     


    path('user-admin/category-list/', views.category_list, name='category_list'),
    path('user-admin/add-category', views.add_category, name='add_category'),
    path('user-admin/posts-list/', views.post_list, name='post_list'), 
    path('user-admin/add-post', views.add_post, name='add_post'),  # Ensure this line is correct
    path('categories/<int:category_id>/', views.posts_by_category, name='posts_by_category'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('posts/<slug:slug>/', views.post_detail, name='post_detail'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('front/', views.front_page, name='front_page'),
    path('back/', views.back_page, name='back_page'),
    path('category-posts/<int:category_id>/', views.page_show, name='page_show'),
    path('user-admin/', views.admin, name='admin'),
    path('user-admin/dashboard/', views.dashboard, name='dashboard'),
    path('index/', views.index, name='index')
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()