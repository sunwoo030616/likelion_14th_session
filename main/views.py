from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import *

# Create your views here.
def mainpage(request):

    return render(request, 'main/mainpage.html')

def new_blog(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    return render(request, 'main/new_blog.html')

def blogpage(request):
    blogs = Blog.objects.all()
    return render(request, 'main/blogpage.html',{'blogs': blogs})

def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    
    if request.method == 'POST' and request.user.is_authenticated:
        new_comment = Comment()
        
        new_comment.blog = blog
        new_comment.writer = request.user
        new_comment.content = request.POST['content']
        
        new_comment.save()  
        return redirect('main:detail', blog.id)
    
    comments = Comment.objects.filter(blog=blog)    
    return render(request, 'main/detail.html',{'blog': blog, 'comments': comments})

def create(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    new_blog = Blog()
    
    new_blog.title = request.POST['title']
    new_blog.writer = request.user
    new_blog.content = request.POST['content']
    new_blog.pub_date = request.POST['pub_date']
    
    new_blog.save()
    
    save_tags(new_blog)
    
    return redirect('main:detail', new_blog.id)

def edit(request, blog_id):
    
    edit_blog = get_object_or_404(Blog, pk=blog_id)
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    
    if edit_blog.writer != request.user:
        return redirect('accounts:login')
    
    return render(request, 'main/edit.html', {'blog': edit_blog})

def update(request, blog_id):
    
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    update_blog = get_object_or_404(Blog, pk=blog_id)
    
    if update_blog.writer != request.user:
        return redirect('main:detail', update_blog.id)
    
    update_blog.title = request.POST['title']
    update_blog.writer = request.user
    update_blog.content = request.POST['content']
    update_blog.pub_date = request.POST['pub_date']
    
    update_blog.save()
    
    save_tags(update_blog)
    
    return redirect('main:detail', update_blog.id)

def delete(request, blog_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    delete_blog = get_object_or_404(Blog, pk=blog_id)
    
    if delete_blog.writer != request.user:
        return redirect('main:detail', delete_blog.id)
    
    
    delete_blog = get_object_or_404(Blog, pk=blog_id)
    delete_blog.delete()
    
    return redirect('main:blogpage')

def save_tags(blog):
    words = blog.content.split()
    tag_list = []
    
    for w in words: 
        if len(w) > 0:
            if w[0] == '#':
                tag_list.append(w[1:])
                
    blog.tags.clear()
    
    for t in tag_list:
        tag, boolean = Tag.objects.get_or_create(name=t)
        blog.tags.add(tag)
    
    
def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'main/tag_list.html', {'tags': tags})

def tag_blog_list(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    blogs = tag.blogs.all()
    return render(request, 'main/tag_blog_list.html', {'tag': tag, 'blogs': blogs})
    