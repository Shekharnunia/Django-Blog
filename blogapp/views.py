from django.shortcuts import render, get_object_or_404
from django.views.generic import (CreateView, DeleteView, DetailView,
                                  ListView, UpdateView, FormView)
from django.db.models import Q
from django.urls import reverse

from .models import Blog, Category, Comment
from .forms import CommentForm


class BlogListView(ListView):
    model = Blog
    template_name = 'blog.html'
    context_object_name = "blogs"
    paginate_by = 10

    def get_queryset(self):
        if self.request.GET.get("query"):
            query = self.request.GET.get("query")
            return Blog.objects.filter(Q(title__icontains=query) |
                                       Q(tags__name=query) | Q(user__username=query) |
                                       Q(user__name=query)).distinct()
        else:
            blog = Blog.objects.all().order_by('-timestamp')
            return blog

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['popular_tags'] = Blog.objects.get_counted_tags()
        context['latest_blog'] = Blog.objects.order_by('-timestamp')[:3]
        context['categories'] = Category.objects.all()
        context['blogapp'] = Category.objects.all()
        context['post'] = Blog.objects.last()
        return context


def index(request):
    post = Blog.objects.last()
    return render(request, 'base.html', {'post': post})


def post(request, slug=None):
    blog = get_object_or_404(Blog, slug=slug)
    categories = Category.objects.all()
    latest_blog = Blog.objects.order_by('-timestamp')[:3]
    context = {
        'blog': blog,
        'categories': categories,
        'latest_blog': latest_blog,
        'post_nav': True,
    }
    return render(request, 'post.html', context)


class DetailBlogView(FormView, DetailView):
    """Basic DetailView implementation to call an individual blog."""
    model = Blog
    form_class = CommentForm
    template_name = 'post.html'
    context_object_name = 'blog'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all()
        context['form'] = CommentForm()
        context['latest_blog'] = Blog.objects.order_by('-timestamp')[:3]
        return context

    def get_success_url(self):
        blog = self.get_object()
        return reverse('blogapp:post',
                       kwargs={'slug': blog.slug})

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        blog = self.get_object()
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.blog_id = blog.id
            form.save()
        return FormView.post(self, request, *args, **kwargs)


# class CommentFormView(FormView):
#     form_class = CommentForm
#     # success_url = reverse('blogapp:post', )
