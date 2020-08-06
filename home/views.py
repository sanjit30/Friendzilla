from django.views import generic
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
import datetime
from .forms import *
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.template.loader import render_to_string

# class IndexView(generic.TemplateView):
#     # print(datetime.datetime.now())
#
#     template_name = 'index.html'
@login_required
def feed(request):
    if request.user.is_authenticated:
        profile,created = UserProfile.objects.get_or_create(user = request.user)
    friends = request.user.profile.friends.all()
    print("friedns--")
    print(friends)
    users = [];
    for friend in friends:
        users.append(friend.user)

    print(users)
    Posts = Post.objects.filter(Q(created_by= request.user)|Q(created_by__in = users)).order_by('-updated_at')

    return render(request,'home/feed.html',{'Posts':Posts})

@login_required
def new_post(request):

    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
            return redirect('home:feed')
    else:
        form = PostForm()
        return render(request, 'home/new_post.html', {'form': form})

# @login_required
# def edit_reply_topic(request,pk,topic_pk,post_pk):
#     post = get_object_or_404(Post,pk=post_pk)
#     if request.method == 'POST':
#         form = PostForm(request.POST,instance=post)
#         if form.is_valid():
#             post.save()
#             return redirect('forum:topic_posts',pk=pk,topic_pk=topic_pk)
#
#     else:
#         form = PostForm(instance=post)
#     return render(request,'forum/edit_reply.html',{'topic':topic,'form':form})


@login_required
def comment_form(request,post_pk):
    print('in comment')
    post =  get_object_or_404(Post,pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
    else:
        form = CommentForm()
    return save_comment_form(request,post,form, 'home/comment.html')


def save_comment_form(request,post,form, template_name):
    data = {
    "form_is_valid":False,
    }
    if request.method == 'POST':
        if form.is_valid():
            print('valid')

            comment= form.save(commit=False)
            comment.created_by = request.user
            comment.post = post
            data = {
            "form_is_valid":True,
            }
            comment.save();
        else:
            data ={
            "form_is_valid":False,
            }
    context = {'form': form,'post':post}
    print('here1')
    data['html_form'] = render_to_string(template_name, context, request=request)
    a = data["form_is_valid"]
    print(a);
    print('here2')
    return JsonResponse(data)

@login_required
def modify_like(request):
    if request.method=='GET' and request.is_ajax():
        print(request.GET.get('post_pk'))
        post_pk = int(request.GET.get('post_pk',None))
        print('correct here')
        print(post_pk)
        print(type(post_pk))
        post = get_object_or_404(Post, pk = post_pk)
        print('yeah')
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            message = 'You disliked this'
        else:
            print('yeah')
            post.likes.add(request.user)
            message = 'You liked this'
        data = {
            'success':True
        }
        return JsonResponse(data)
