import tempfile

import paginator as paginator
from django.contrib.auth.models import User
from mediablog.forms import *
from django.core.paginator import Paginator
from django.contrib.sites import requests
from django.core import files
from django.shortcuts import render, get_object_or_404,redirect
from mediablog.models import MediaBlog, Comment, Reaction
from django.template.loader import render_to_string
from django.http import JsonResponse
from mediablog.forms import MediaForm
# Create your views here.
def MediaView(request):
    posts = MediaBlog.objects.all().order_by('-id')
    comment =Comment.objects.all()
    paginator =Paginator(posts,8)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'mediablog.html', {'posts':posts,'comment':comment})
def DetailPost(request,id):
    posts =MediaBlog.objects.all()
    post = get_object_or_404(MediaBlog,id=id)
    video_id = post.link.split('v=')[+1]
    comments = Comment.objects.filter(post=post,reply=None).order_by('-id')
    if request.method=="POST":
        comment_form =CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = comment_form.cleaned_data.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(post=post,user=request.user,content=content,reply=comment_qs)
            comment.save()
            # return redirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()
    context={
        'comments':comments,
        'post':post,
        'posts':posts,
        'video_id':video_id,
        'total_like': post.liked_count_r(),
        'comment_form':comment_form,
    }
    if request.is_ajax():
        html = render_to_string('media/comment_section.html',context,request=request)
        return JsonResponse({'form':html})
    return render(request,'mediadetails.html',context)

def like_post(request):
    post = get_object_or_404(MediaBlog,id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        return {"status":"success","action":"increase"}
    total=get_object_or_404(MediaBlog,id=request.POST.get('post_id'))
    context={
        'post':post,
        'total_like':total.likes.count(),
    }
    if request.is_ajax():
        html =render_to_string('media/reaction_section.html',context,request=request)
        return JsonResponse({'form':html})

def love_post(request):
    post = get_object_or_404(MediaBlog,id=request.POST.get('post_id'))
    if post.love.filter(id=request.user.id).exists():
        post.love.remove(request.user)
    else:
        post.love.add(request.user)
    return redirect(post.get_absolute_url())
# def reaction_post(request):
#     post =get_object_or_404(MediaBlog,id=request.POST.get('post_id'))
#     user = request.user
#     if request.method=="POST":
#         if 'like_id' in request.POST:
#             if post.likes.filter(id=request.user.id).exists():
#                 post.likes.remove(user)
#             else:
#                 post.likes.add(user)
#                 if post.love.filter(id=request.user.id).exists():
#                     post.love.remove(user)
#
#
#         if 'love_id' in request.POST:
#            pass
#         if 'angry_id' in request.POST:
#            pass
#         if 'hahaha_id' in request.POST:
#            pass
#         if 'sad_id' in request.POST:
#             pass
#     context={
#         'post':post,
#
#     }
#     if request.is_ajax():
#         html = render_to_string('media/reaction_section.html',context,request=request)
#         return JsonResponse({'form': html})
def CreateMedia(user,title,link,des):
    video_id = link.split('v=')[+1]
    thumbnail_url = f"http://img.youtube.com/vi/{video_id}/sddefault.jpg"
    request = requests.get(thumbnail_url,stream=True)

    lf = tempfile.NamedTemporaryFile()
    for block in request.iter_content(1024*8):
        if not block:
            break
        lf.write(block)
    media = MediaBlog(author=user)
    media.title=title
    media.link=link
    media.description=des
    media.thumbnail.save("thumbnail.jpg",files.File(lf))

