from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import PostForm
from webapp.models import Post


class PostsListView(ListView):
    model = Post
    template_name = "posts/posts_list.html"
    context_object_name = "posts"
    paginate_by = 3
    ordering = ("-created_at",)

    def get_queryset(self):
        posts = super().get_queryset()
        if self.request.user.is_authenticated:
            # posts = posts.filter(author__followers__contains=self.request.user.pk)
            posts = super().get_queryset().filter(author__in=self.request.user.following.all())
        return posts


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = "posts/post_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_update.html"

    def has_permission(self):
        return self.request.user == self.get_object().author


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = "posts/post_delete.html"

    def has_permission(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse("accounts:profile", kwargs={"pk": self.request.user.pk})


class PostDetailView(DetailView):
    queryset = Post.objects.all()
    template_name = "posts/post_view.html"


class FollowersView(LoginRequiredMixin, View):
    def get(self, request, *args, pk, **kwargs):
        user = get_object_or_404(get_user_model(), pk=pk)
        if user == request.user:
            return HttpResponseBadRequest()
        if request.user in user.followers.all():
            user.followers.remove(request.user)
        else:
            user.followers.add(request.user)
        return redirect("accounts:profile", pk=pk)


class LikePostView(LoginRequiredMixin, View):
    def get(self, request, *args, pk, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        if request.user in post.like_users.all():
            post.like_users.remove(request.user)
        else:
            post.like_users.add(request.user)
        return HttpResponseRedirect(self.request.GET.get("next"))
