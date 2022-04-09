from django.shortcuts import render
from .models import Post
from .forms import PostForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import datetime
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})


class NewPostCreateView(CreateView):
    model = Post
    fields = ["title", "text"]
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        

# def new_post(request):
#     if request.method == "POST":
#         form = PostForm(request.POST)
        # if form.is_valid():
        #     post = form.save(commit=False)
        #     post.author = User.objects.all()[0]
        #     post.published_date = datetime.datetime.now()
        #     post.save()
        #     return redirect('post_detail', post_id=post.id)
#     else:
#         form = PostForm()
#     return render(request, 'blog/post_form.html', {'form': form, 'type_of_request': 'New'})


def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = User.objects.all()[0]
            post.published_date = datetime.datetime.now()
            post.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'type_of_request': 'Edit'})

def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('post_list')