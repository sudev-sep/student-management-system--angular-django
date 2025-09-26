from rest_framework import serializers
from .models import User, Teacher, Student


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'email', 'usertype',
            'address', 'phone_number', 'first_name', 'last_name'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
            usertype=validated_data['usertype'],
            address=validated_data['address'],
            phone_number=validated_data['phone_number'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class TeacherSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(source='teacher_id')

    class Meta:
        model = Teacher
        fields = ['id', 'teacher', 'salary', 'experience', 'teacher_pic', 'is_approved']

    def create(self, validated_data):
        user_data = validated_data.pop('teacher_id')
        users = UserSerializer().create(user_data)
        teacher = Teacher.objects.create(teacher_id=users, **validated_data)
        return teacher

    def update(self, instance, validated_data):
        user_data = validated_data.pop('teacher_id', None)
        instance.salary = validated_data.get('salary', instance.salary)
        instance.experience = validated_data.get('experience', instance.experience)
        instance.teacher_pic = validated_data.get('teacher_pic', instance.teacher_pic)
        instance.is_approved = validated_data.get('is_approved', instance.is_approved)
        instance.save()

        if user_data:
            user = instance.teacher_id
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.username = user_data.get('username', user.username)
            user.email = user_data.get('email', user.email)
            user.phone_number = user_data.get('phone_number', user.phone_number)
            user.address = user_data.get('address', user.address)
            user_data.pop('username', None)
            user.save()
        return instance


class StudentSerializer(serializers.ModelSerializer):
    student = UserSerializer(source='student_id')

    class Meta:
        model = Student
        fields = ['id', 'student', 'guardian', 'is_approved']

    def create(self, validated_data):
        user_data = validated_data.pop('student_id')
        user = UserSerializer().create(user_data)
        student = Student.objects.create(student_id=user, **validated_data)
        return student

    def update(self, instance, validated_data):
        user_data = validated_data.pop('student_id', None)
        instance.guardian = validated_data.get('guardian', instance.guardian)
        instance.is_approved = validated_data.get('is_approved', instance.is_approved)
        instance.save()

        if user_data:
            user = instance.student_id
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.username = user_data.get('username', user.username)
            user.email = user_data.get('email', user.email)
            user.phone_number = user_data.get('phone_number', user.phone_number)
            user.address = user_data.get('address', user.address)
            user_data.pop('username', None)
            user.save()
        return instance