from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myapp.models import Student, User,Teacher
from .serializers import StudentSerializer, UserSerializer, TeacherSerializer
from django.contrib.auth import authenticate, login 
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated



class StudentRegisterView(APIView):
    authentication_classes=[]
    permission_classes=[AllowAny]

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'student registered successfully'})
        return Response(serializer.errors)
    
from rest_framework.parsers import MultiPartParser, FormParser
class TeacherRegisterView(APIView):
    authentication_classes=[]
    permission_classes=[AllowAny]
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request):
        print("request.data:", request.data)
        serializer = TeacherSerializer(data=request.data)
        print(serializer,"???????///")
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'teacher registered successfully'})
        print("serializer.errors:", serializer.errors)
        return Response(serializer.errors)

class alllogin(APIView):
    authentication_classes=[]
    permission_classes=[AllowAny]
    print("inclass")
    def post(self, request):
        print("in function")
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        print(user,username,password)
        if user :
            print(user,"////////////////")
            if user.usertype == 'teacher':
                print("here")
                try:
                    teacher = Teacher.objects.get(teacher_id=user)
                    print(teacher)
                    if not teacher.is_approved:
                        print(teacher.is_approved)
                        return Response({'error': 'Teacher not approved'},status=403)
                except :
                  return Response({'error': ' teacher not found '}, status=403)
        
            token, _ = Token.objects.get_or_create(user=user)
            print(token, "token")

            return Response({
                "token": token.key,
                "usertype": user.usertype,
                "is_superuser": user.is_superuser
                                   })
        return Response({"error": "Invalid credentials"}, status=401)


class TeacherListview(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
      if not request.user.is_superuser:
         return Response({'detail': 'Only admins can view this.'}, status=403)

      print(request.data,"//////////")
      teachers = Teacher.objects.all()
      print(teachers)
      serializer = TeacherSerializer(teachers, many=True)
      print(serializer.data,"\\\\\\\\\\\\\./")
      return Response(serializer.data)
    
class StudentListview(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_superuser:
            return Response({'detail': 'Only admins can view this.'}, status=403)

        print(request.data, "//////////")
        students = Student.objects.all()
        print(students)
        serializer = StudentSerializer(students, many=True)
        print(serializer.data, "\\\\\\\\\\\\\\./")
        return Response(serializer.data)


class approveTeacherview(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request,pk):
      try:
         teacher = Teacher.objects.get(pk=pk)
         user=teacher.teacher_id
         teacher.is_approved = True
         teacher.save()
         user.is_staff=True
         user.save()
         return Response("teacher approved")
      except Teacher.DoesNotExist:
          return Response({"error":"Teacher does not exist"})


class approveStudentview(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request,pk):
      try:
         student = Student.objects.get(pk=pk)
        #  user=student.student_id
         student.is_approved = True
         student.save()
       
         return Response("student approved")
      except Student.DoesNotExist:
          return Response({"error":"student does not exist"})     
      



class deleteTeachertview(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request,pk):
      try:
         teacher = Teacher.objects.get(pk=pk)
         teacher.teacher_id.delete()
         teacher.delete()
         return Response("teacher deleted")
      except Teacher.DoesNotExist:
          return Response({"error":"Teacher does not exist"})
      


class deleteStudentview(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request,pk):
      try:
         student = Student.objects.get(pk=pk)
         student.student_id.delete()
         student.delete()
         return Response("student deleted")
      except Student.DoesNotExist:
          return Response({"error":"student does not exist"})
      


class TeacherProfileview(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
      print("in teacher profile ")
      try:
         teacher = Teacher.objects.get(teacher_id=request.user)
         print(teacher)
         serializer=TeacherSerializer(teacher)
         print(serializer.data)
         teacher.save()
         return Response(serializer.data)
      except Teacher.DoesNotExist:
          return Response({"error":"teacher does not found"})



class StudentTeachListview(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        students = Student.objects.all()
        print(students)
        serializer = StudentSerializer(students, many=True)
        print(serializer.data, "\\\\\\\\\\\\\\./")
        return Response(serializer.data)
    

class TeacherProfileUpdateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request):
        try:
            teacher = Teacher.objects.get(teacher_id=request.user)
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher not found"})

        serializer = TeacherSerializer(teacher, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class StudentProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            student = Student.objects.get(student_id=request.user)
            print(request.user)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"})


class ALLTeachersListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        teachers = Teacher.objects.filter(is_approved=True)
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)


class StudentProfileUpdateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            student = Student.objects.get(student_id=request.user)
        except Student.DoesNotExist:
            return Response({"error": "student not found"})

        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:   
            print(serializer.errors)
            return Response(serializer.errors)
        