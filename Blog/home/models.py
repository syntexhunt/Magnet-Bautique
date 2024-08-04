# Create your models here.

import requests
import matplotlib.pyplot as plt
import seaborn as sns
from django.db import models
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from io import BytesIO
import base64
from django.conf import settings
from io import BytesIO

from froala_editor.fields import FroalaField
from django.contrib.auth.models import User
from .helpers import generate_slug

PAGE_CHOICES = [
    ('front', 'MANS'),
    ('back', 'KIDS'),
]

class BlogManager(models.Manager):
    def generate_post_activity_graph(self):
        daily_posts = self.annotate(date=TruncDay('created_at')).values('date').annotate(count=Count('id')).order_by('date')
        weekly_posts = self.annotate(date=TruncWeek('created_at')).values('date').annotate(count=Count('id')).order_by('date')
        monthly_posts = self.annotate(date=TruncMonth('created_at')).values('date').annotate(count=Count('id')).order_by('date')

        daily_dates = [entry['date'] for entry in daily_posts]
        daily_counts = [entry['count'] for entry in daily_posts]
        weekly_dates = [entry['date'] for entry in weekly_posts]
        weekly_counts = [entry['count'] for entry in weekly_posts]
        monthly_dates = [entry['date'] for entry in monthly_posts]
        monthly_counts = [entry['count'] for entry in monthly_posts]

        plt.figure(figsize=(14, 7))
        sns.lineplot(x=daily_dates, y=daily_counts, label='Daily Posts')
        sns.lineplot(x=weekly_dates, y=weekly_counts, label='Weekly Posts')
        sns.lineplot(x=monthly_dates, y=monthly_counts, label='Monthly Posts')
        plt.title('Post Activity Over Time')
        plt.xlabel('Date')
        plt.ylabel('Number of Posts')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graph = base64.b64encode(image_png)
        graph = graph.decode('utf-8')

        return graph

class Category(models.Model):
    name = models.CharField(max_length=100)
    page = models.CharField(max_length=10, choices=PAGE_CHOICES, default='MANS')

    def __str__(self):
        return self.name

class BlogModel(models.Model):
    title = models.CharField(max_length=1000)
    content = FroalaField()
    slug = models.SlugField(max_length=1000, null=True, blank=True)
    image = models.URLField(max_length=1000, blank=True, null=True)  # Keep for images
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    page = models.CharField(max_length=10, choices=PAGE_CHOICES, default='KIDS')
    objects = BlogManager()
    price = models.CharField(max_length=1000)
    is_deleted = models.BooleanField(default=False)  # Ensure this field exists


    def upload_image_to_github(self, image_file):
        repo_path = f"images/{upload_image.name}"
        url = f"https://api.github.com/repos/{settings.GITHUB_REPO_OWNER}/{settings.GITHUB_REPO_NAME}/contents/{image_file.name}"
        headers = {
            'Authorization': f'token {settings.GITHUB_ACCESS_TOKEN}',
            'Accept': 'application/vnd.github.v3+json',
        }
        data = {
            'message': f'Upload image {image_file.name}',
            'content': base64.b64encode(image_file.read()).decode('utf-8')
        }
        response = requests.put(url, json=data, headers=headers)
        if response.status_code == 201:
            return response.json()['content']['download_url']
        else:
            raise Exception('Failed to upload image to GitHub')



    def __str__(self):
        return self.title

    #def save(self, *args, **kwargs):
    #    if not self.slug:
    #        self.slug = generate_slug(self.title)
    #    super(BlogModel, self).save(*args, **kwargs)

    #def get_image(self):
    #    return self.image_url if self.image_url else self.image.url

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.title)
        if 'image' in kwargs:
            image_file = kwargs.pop('image')
            self.image = self.upload_image_to_github(image_file)
        super(BlogModel, self).save(*args, **kwargs)
        print(f"Image URL: {self.image}")  # Print the image URL
