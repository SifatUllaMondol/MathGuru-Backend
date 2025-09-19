from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField()
    student_class = models.CharField(null=True)
    chapter_completed = models.PositiveIntegerField(null=True)
    type = models.IntegerField(null=True)
    type_accuracy = models.IntegerField(null=True)
    payment_date = models.DateTimeField(null=True)
    registration_date = models.DateTimeField(auto_now_add=True) 

    

class UploadedDocument(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField(null=True)

class QA(models.Model):
    doc_type_num = models.ForeignKey(UploadedDocument, on_delete=models.CASCADE)
    type = models.IntegerField()
    question = models.TextField()
    answer = models.TextField()
    tags = models.TextField(null=True)

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class StudentTagPerformance(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'tag')

class Test(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

class TestQuestion(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(QA, on_delete=models.CASCADE)
    student_answer = models.TextField(blank=True, null=True)
    is_correct = models.BooleanField(default=False) 