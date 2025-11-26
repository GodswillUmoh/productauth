from django.shortcuts import render
from .models import BlogPost
from django.core.paginator import Paginator

def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/blog_list.html', {
        'posts': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages()
    })
