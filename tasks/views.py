from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from tasks.mixins import UserIsOwnerMixin

from .forms import TaskFilterForm, TaskForm
from .models import Task


class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        queryset = Task.objects.all()

        if self.request.user.is_authenticated:
            queryset = queryset.filter(creator=self.request.user)

        form = TaskFilterForm(self.request.GET)
        if form.is_valid():
            status = form.cleaned_data.get("status")
            priority = form.cleaned_data.get("priority")
            due_date = form.cleaned_data.get("due_date")

            if status:
                queryset = queryset.filter(status=status)
            if priority:
                queryset = queryset.filter(priority=priority)
            if due_date:
                queryset = queryset.filter(due_date=due_date)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TaskFilterForm(self.request.GET)
        return context


class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:task_list")

    def form_valid(self, form):
        form.instance.creator = self.request.user   
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:task_list")


class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks:task_list")


class RegisterView(CreateView):
    template_name = "registration/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("tasks:task_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
