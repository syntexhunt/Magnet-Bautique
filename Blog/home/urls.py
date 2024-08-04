from django.urls import path
from froala_editor import views
from .views import category_list, add_category, delete_category, add_post, post_list, edit_post, delete_post, post_detail, posts_by_category, front_page, back_page, post_activity_graph_view

urlpatterns = [
    path('user-admin/category-list/', category_list, name='category_list'),
    path('user-admin/add-category', add_category, name='add_category'),
    path('categories/delete/<int:category_id>/', delete_category, name='delete_category'),
    path('user-admin/add-post', add_post, name='add_post'),
    path('user-admin/posts-list/', post_list, name='post_list'),
    path('posts/edit/<int:post_id>/', edit_post, name='edit_post'),
    path('posts/delete/<int:post_id>/', delete_post, name='delete_post'),
    path('posts/<slug:slug>/', post_detail, name='post_detail'),
    path('categories/<int:category_id>/', posts_by_category, name='posts_by_category'),
    path('front/', front_page, name='front_page'),
    path('back/', back_page, name='back_page'),
    path('category-posts/', page_show, name='category_posts'),
    path('user-admin/', admin, name='admin'),
    path('user-admin/dashboard/', dashboard, name='dashboard'),
    
]

