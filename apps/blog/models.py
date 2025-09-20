import uuid

from django.db import models
from django.utils import timezone


def blog_thumbnail_directory(instance, filename):
    return "blog/{0}/{1}".format(instance.title, filename)

def category_thumbnail_directory(instance, filename):
    return "blog_categories/{0}/{1}".format(instance.title, filename)

class Category(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey("self", related_name="children", on_delete=models.CASCADE, blank=True, null=True)
    
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to=category_thumbnail_directory)
    slug = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    

class Post(models.Model):
    
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')
            
    
    status_options = (
        ("draft", "Draft"),
        ("published", "Published")
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    content = models.TextField()
    thumbnail = models.ImageField(upload_to=blog_thumbnail_directory)

    keywords = models.CharField(max_length=128)
    slug = models.CharField(max_length=128)
    
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    status = models.CharField(max_length=10, choices=status_options, default='draft')
    
    objects = models.Manager()    # default manager
    postobjects = PostObjects()   # custom manager
    
    class Meta:
        ordering = ("-published")
        
    def __str__(self):
        return self.title
    