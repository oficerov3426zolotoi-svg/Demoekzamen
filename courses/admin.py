from django.contrib import admin
from .models import Course, Application, Review, UserProfile


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_type', 'duration', 'price')
    list_filter = ('course_type',)
    search_fields = ('name', 'description')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'start_date', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'course')
    search_fields = ('user__username', 'course__name')
    actions = ['set_in_progress', 'set_completed']

    @admin.action(description='Идет обучение')
    def set_in_progress(self, request, queryset):
        queryset.update(status='in_progress')

    @admin.action(description='Обучение завершено')
    def set_completed(self, request, queryset):
        queryset.update(status='completed')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'application', 'created_at')
    list_filter = ('created_at',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'email')
    search_fields = ('full_name', 'user__username')