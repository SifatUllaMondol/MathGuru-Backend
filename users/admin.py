from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser,
    UploadedDocument,
    QA,
    Tag,
    StudentTagPerformance,
    Test,
    TestQuestion,
)

# Customizing the UserAdmin for CustomUser
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'username', 'email', 'type_accuracy', 'payment_date', 
        'age', 'student_class', 'chapter_completed', 'type', 'registration_date'
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('age', 'student_class', 'chapter_completed')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('age', 'student_class', 'chapter_completed')}),
    )
    search_fields = ('username', 'email', 'student_class')
    list_filter = ('student_class', 'chapter_completed', 'is_staff')


# Admin for UploadedDocument
class UploadedDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'uploaded_at', 'type')
    list_filter = ('uploaded_at', 'type')
    search_fields = ('file',)


@admin.register(QA)
class QAAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer', 'type', 'tags')
    search_fields = ('question', 'answer')
    list_filter = ('type',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(StudentTagPerformance)
class StudentTagPerformanceAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'student', 'tag',
        'total_questions', 'correct_answers', 'last_updated'
    )
    search_fields = ('student__username', 'tag__name')
    list_filter = ('tag', 'student')


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'created_at', 'completed')
    search_fields = ('student__username',)
    list_filter = ('completed', 'created_at')


@admin.register(TestQuestion)
class TestQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'test', 'question', 'is_correct')
    search_fields = ('test__student__username', 'question__question')
    list_filter = ('is_correct',)


# Register the CustomUser and UploadedDocument models with custom admin classes
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UploadedDocument, UploadedDocumentAdmin)
