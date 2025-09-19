from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import UploadedDocument, QA
from rest_framework import status
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status, permissions
from django.shortcuts import render, redirect
import random
from django.views import View
from django.contrib import messages
from django.contrib.auth import get_user_model


User = get_user_model()

# Registration API and Page
class RegisterUser(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def RegisterPage(request):
    if request.user.is_authenticated:
        return redirect('okk') 
    if request.method == 'POST':
        username = request.POST.get('username')
        age = request.POST.get('age')
        student_class = request.POST.get('student_class')
        chapter_completed = request.POST.get('chapter_completed')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')

        if password != re_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        # Create the user
        user = User.objects.create_user(username=username, password=password, age=age, student_class=student_class, chapter_completed=chapter_completed)
        # You can extend this to save age, class, etc., in a custom model if needed

        messages.success(request, "Registration successful. Please login.")
        return redirect('login_page')  # name of your login URL

    return render(request, 'registration.html')
    
# Login API and Page
class LoginUser(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['username'],
                                password=serializer.validated_data['password'])
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "token": token.key,
                    "message": "Login successful"
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('okk') 
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('okk')
        return render(request, 'login.html', {'error': 'Invalid credentials'})

# logout API and Page
class LogoutUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()  # Delete the user's token
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

class LogoutPage(View):
    def post(self, request):
        logout(request)
        return redirect('login_page')

# Document upload Page
def upload_document_page(request):
    return render(request, 'upload_document.html')


from .utils import extract_text_from_file, parse_questions

def upload_document(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        type_value = request.POST.get('type', None)

        # Validate file presence
        if not file:
            messages.error(request, "No file provided.")
            return render(request, 'upload_document.html')

        # Save the document
        try:
            document = UploadedDocument.objects.create(
                file=file,
                type=int(type_value) if type_value else None
            )
            messages.success(request, "File uploaded successfully!")

            # Extract questions from document
            if document:
                text = extract_text_from_file(document.file.path)
                qas = parse_questions(text)

                 # list the Q&A and tags that are avaiable in the pdf
                tags = set()
                for question, tag, answer in qas:
                    
                    tags.update(tag)

                    # if not QA.objects.filter(question=question.strip()).exists():
                    QA.objects.create(question=question.strip(), answer=answer.strip(), tags=tag, doc_type_num=document, type=document.type)

            return redirect('upload_page')
        except ValueError:
            messages.error(request, "Invalid type value. Please enter a valid number.")
            return render(request, 'upload_document.html')

        
    return render(request, 'upload_document.html')


# Rendering q&a from QA model///

from django.contrib.auth.decorators import login_required
from .models import  Tag, StudentTagPerformance
import ast
@login_required
def view_document(request):
    if request.method == 'POST':
        # Get the previously selected question IDs from session
        question_ids = request.session.get('selected_question_ids', [])
        questions = QA.objects.filter(id__in=question_ids)
        results = []

        # Process answers and update tag performance
        for q in questions:
            user_answer = request.POST.get(f'answer_{q.id}', '').strip().lower()
            correct = user_answer == q.answer.strip().lower()
            results.append((q.question, q.answer, user_answer, correct))

            # Safely convert tags string to list
            try:
                tags_list = ast.literal_eval(q.tags) if isinstance(q.tags, str) else q.tags
            except Exception as e:
                tags_list = []
                print(f"Error parsing tags for question {q.id}: {e}")

            # Update StudentTagPerformance
            for tag_name in tags_list:
                # Ensure Tag instance exists
                tag_obj, _ = Tag.objects.get_or_create(name=tag_name)

                # Update or create StudentTagPerformance for this tag
                performance, created = StudentTagPerformance.objects.get_or_create(
                    student=request.user,
                    tag=tag_obj,
                    defaults={'total_questions': 0, 'correct_answers': 0}
                )
                performance.total_questions += 1
                if correct:
                    performance.correct_answers += 1
                performance.save()

        # Clean up session
        request.session.pop('selected_question_ids', None)

        return render(request, 'quiz_result.html', {'results': results})

    else:
        # Select questions for the test
        question_type = 2  # Clculate TYPE.........................................
        
        ques = list(QA.objects.filter(type=question_type))

        # Select 5 random questions
        selected_questions = random.sample(ques, min(5, len(ques)))

        # Store selected question IDs in session
        request.session['selected_question_ids'] = [q.id for q in selected_questions]

        return render(request, "view_data.html", {'questions': selected_questions})



# User profile

def profile_view(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html', {'user': request.user})

def okk(request):
    return render(request, 'okk.html')