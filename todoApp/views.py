from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .models import *



class TasksView(View):
    def get(self, request):
        if request.user.is_authenticated:
            tasks = Task.objects.filter(user=request.user).order_by('-id')
            context = {
                'tasks': tasks,
                'user': request.user,
                'status_choices': Task.STATUS_CHOICES,
            }
            return render(request, 'index.html', context)
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            print(request.POST.get('deadline'))
            task = Task.objects.create(
                title=request.POST.get('title', None),
                description=request.POST.get('description', None),
                deadline=request.POST.get('deadline', None),
                status=request.POST.get('status', 'new'),
                user=request.user
            )
            if task.deadline == "2000-01-01":
                task.deadline = None
                task.save()
            return redirect('index')
        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is not None:
            login(request, user)
            return redirect('index')
        return redirect('login')



class LogaoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class DeleteTaskView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            task = get_object_or_404(Task, id=pk)
            if task.user == request.user:
                task.delete()
                return redirect('index')
            return redirect('logaout')
        return redirect('login')

class UpdateTaskView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            task = get_object_or_404(Task, id=pk)
            if task.user != request.user:
                return redirect('index')
            context = {
                'task': task,
                'status_choise': Task.STATUS_CHOICES
            }
            return render(request, 'edit.html', context)
        return redirect('login')

    def post(self, request, pk):
        if request.user.is_authenticated:
            task = get_object_or_404(Task, id=pk)
            if task.user == request.user:
                task.title = request.POST.get('title', None)
                task.description = request.POST.get('description', None)
                task.status = request.POST.get('status', 'complate')
                task.save()
            return redirect('index')
        return redirect('login')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        try:
            User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
            )
        except:
            return redirect('register')
        return redirect('login')



