
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, BlogModel
from .forms import CategoryForm, BlogForm
from django.utils import timezone
from django.db.models.functions import TruncDay
from django.db.models import Count




def index(request):
    page_type = 'front'  # Set dynamically as needed
    categories = Category.objects.filter(page=page_type)
    posts = Post.objects.filter(category__in=categories)
    return render(request, 'index.html', {
        'page_type': page_type,
        'categories': categories,
        'posts': posts,
    })
    return render(request, 'index.html')


def post_list(request):
    posts = BlogModel.objects.filter(is_deleted=False)
    return render(request, 'post_list.html', {'posts': posts})



def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    print("Request method:", request.method)  # Debugging statement
    if request.method == 'POST':
        category.delete()
        print("Category deleted:", category.name)  # Debugging statement
        return redirect('category_list')
    return render(request, 'delete_category.html', {'category': category})


def dashboard(request):
    graph = BlogModel.objects.generate_post_activity_graph()
    return render(request, 'dashboard.html', {'graph': graph})

def add_post(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        image = request.FILES.get('image', '')
        title = request.POST.get('title')
        if form.is_valid():
            print('Valid')
            content = form.cleaned_data['content']
            form.save()
            return redirect('post_list')
    else:
        form = BlogForm()
    return render(request, 'add_post.html', {'form': form})



def admin(request):
    return render(request, 'admin.html')

    


def page_show(request):
    categories = Category.objects.all()
    category = get_object_or_404(Category, id=category_id)
    posts = category.post_set.all()
    
    # Your pagination logic here

    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'category_posts.html', context)
    



def edit_post(request, post_id):
    post = get_object_or_404(BlogModel, id=post_id)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = BlogForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})

def delete_post(request, post_id):
    post = get_object_or_404(BlogModel, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'delete_post.html', {'post': post})

def post_detail(request, slug):
    post = get_object_or_404(BlogModel, slug=slug)
    return render(request, 'post_detail.html', {'post': post})

def posts_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = BlogModel.objects.filter(category=category)
    return render(request, 'posts_by_category.html', {'category': category, 'posts': posts})

def front_page(request):
    categories = Category.objects.filter(page='front')
    posts = BlogModel.objects.filter(page='front')
    return render(request, 'front.html', {'categories': categories, 'posts': posts})

def back_page(request):
    categories = Category.objects.filter(page='back')
    posts = BlogModel.objects.filter(page='back')
    return render(request, 'back.html', {'categories': categories, 'posts': posts})

