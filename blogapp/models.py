from django.db import models
from django.db.models.signals import pre_save
from django.db.models import Count
from django.urls import reverse

from users.models import User
from .utils import unique_slug_generator

from taggit.managers import TaggableManager


class BlogQuerySet(models.query.QuerySet):
    """Personalized queryset created to improve model usability"""

    def get_5_popular_post(self):
        """Returns only the popular items as in the current queryset."""
        return self.order_by('-views')[:5]

    def get_popular_post(self):
        """Returns only the popular items as in the current queryset."""
        return self.filter(status="P").order_by('-views', '-timestamp')

    def get_counted_tags(self):
        tag_dict = {}
        query = self.annotate(
            tagged=Count('tags')).filter(tags__gt=0)
        for obj in query:
            for tag in obj.tags.names():
                if tag not in tag_dict:
                    tag_dict[tag] = 1

                else:  # pragma: no cover
                    tag_dict[tag] += 1

        return tag_dict.items()


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.title


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=80, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(null=True, blank=True)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='blog/', default='img/blog-1.jpg')
    tags = TaggableManager()
    objects = BlogQuerySet.as_manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blogapp:post', kwargs={'slug': self.slug})


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.blog.title


def blog_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(blog_pre_save_receiver, sender=Blog)


def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(category_pre_save_receiver, sender=Category)
