from django.conf import settings

from django.shortcuts import render, redirect
from datetime import datetime
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)

from .filters import PostFilter
from .models import *
# from .filters import PostFilter
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from django.shortcuts import get_object_or_404

from django.core.cache import cache

from django.utils.translation import gettext as _

import pytz
from django.utils import timezone

from django.core.mail import send_mail

class PostList(ListView):
    model = Post
    ordering = '-create_time'
    template_name = 'post.html'
    context_object_name = 'post'
    paginate_by = 2

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones  # добавляем в контекст все доступные часовые пояса
        return context

    #
    # def post(self, request):
    #     request.session['django_timezone'] = request.POST['timezone']
    #     return redirect(request.META['HTTP_REFERER'])


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def post(self, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(self.request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = self.request.user
            comment.save()
            send_mail(
                subject=f'New Comment on"{comment.post.header}"',
                message=f'Был оставлен отклик {comment.comm_text} пользователем {self.request.user.username} на ваше объявление "{comment.post.header}"',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[comment.post.user.email]
            )
            return redirect('post_detail', pk=post.pk)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class PostSearch(ListView):
    model = Post
    ordering = '-create_time'
    template_name = 'post_search.html'
    context_object_name = 'post'
    paginate_by = 2

    #
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.filterset = PostFilter(self.request.GET, queryset=queryset)
    #     return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context



class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')


class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class AddPost(PermissionRequiredMixin, CreateView):
    permission_required = ('post.add_post', )


class ChangePost(PermissionRequiredMixin, UpdateView):
    permission_required = ('post.change_post', )
    # а дальше пишите код вашего представления


def accept(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if comment.status == 'pending':
        comment.status = 'accepted'
        comment.save()
        send_mail(
            subject=f'Оповещение',
            message=f'Ваш отклик "{comment}" был принят автором {comment.post.user.username}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[comment.user.email],
        )
    return redirect('profile')

#