from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Application, Course, Review, UserProfile
from .forms import RegisterForm, LoginForm, ApplicationForm, ReviewForm


def index(request):
    return render(request, 'courses/index.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('cabinet')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            full_name = form.cleaned_data['full_name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']

            user = User.objects.create_user(username=username, password=password)
            UserProfile.objects.create(user=user, full_name=full_name, phone=phone, email=email)
            login(request, user)
            return redirect('cabinet')
    else:
        form = RegisterForm()

    return render(request, 'courses/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('cabinet')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('cabinet')
            else:
                messages.error(request, 'Неправильный логин или пароль')
    else:
        form = LoginForm()

    return render(request, 'courses/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def cabinet(request):
    applications = Application.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'courses/cabinet.html', {'applications': applications})


@login_required
def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, 'Заявка успешно создана!')
            return redirect('cabinet')
    else:
        form = ApplicationForm()

    return render(request, 'courses/create_application.html', {'form': form})


@login_required
def add_review(request, application_id):
    application = Application.objects.get(id=application_id, user=request.user)
    if application.status != 'completed':
        messages.error(request, 'Отзыв можно оставить только после завершения обучения')
        return redirect('cabinet')

    if Review.objects.filter(application=application).exists():
        messages.error(request, 'Вы уже оставили отзыв на эту заявку')
        return redirect('cabinet')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.application = application
            review.save()
            messages.success(request, 'Отзыв успешно добавлен!')
            return redirect('cabinet')
    else:
        form = ReviewForm()

    return render(request, 'courses/add_review.html', {'form': form})


def admin_panel(request):
    if not request.user.is_authenticated or request.user.username != 'Admin26':
        return redirect('login')

    admin_password = 'Demo20'
    if request.method == 'POST':
        if request.POST.get('password') == admin_password:
            return redirect('admin_applications')
        else:
            messages.error(request, 'Неправильный пароль администратора')

    return render(request, 'courses/admin_login.html')


@login_required
def admin_applications(request):
    if not request.user.is_authenticated or request.user.username != 'Admin26':
        return redirect('login')

    applications = Application.objects.all()

    status_filter = request.GET.get('status', '')
    course_filter = request.GET.get('course', '')
    sort_by = request.GET.get('sort', '-created_at')

    if status_filter:
        applications = applications.filter(status=status_filter)

    if course_filter:
        applications = applications.filter(course_id=course_filter)

    if sort_by:
        applications = applications.order_by(sort_by)

    courses = Course.objects.all()
    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'courses/admin_panel.html', {
        'page_obj': page_obj,
        'courses': courses,
        'status_filter': status_filter,
        'course_filter': course_filter,
        'sort_by': sort_by,
    })


@login_required
def change_status(request, application_id):
    if not request.user.is_authenticated or request.user.username != 'Admin26':
        return redirect('login')

    application = Application.objects.get(id=application_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['new', 'in_progress', 'completed']:
            application.status = new_status
            application.save()
            messages.success(request, 'Статус заявки обновлен')

    return redirect('admin_applications')