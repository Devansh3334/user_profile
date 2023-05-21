from .models import User
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

import io
from rest_framework import serializers


class UserSerializear(serializers.ModelSerializer):
    username = serializers.CharField(min_length=3, max_length=50)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(min_length=3, max_length=50)
    last_name = serializers.CharField(min_length=3, max_length=50)
    password = serializers.CharField(min_length=8, max_length=255,
                                     write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(min_length=8, max_length=255,
                                             required=False, write_only=True)
    profile_image = serializers.ImageField()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', "confirm_password", "first_name", "last_name", "profile_image"
            , "phone_number", "designation", "date_of_birth"]

    def validate(self, validated_data):
        errors = {}
        # password validation
        if "password" in validated_data:
            try:
                validate_password(validated_data['password'])
                if validated_data['password'] != validated_data['confirm_password']:
                    errors.setdefault("confirm_password", []).append((
                        validated_data['confirm_password']))
            except Exception as err:
                errors.setdefault("password", []).append(err.args[0])

        if len(errors) > 0:
            raise ValidationError(errors)

        return validated_data

    def validate_username(self, username):
        user_obj = User.objects.filter(username=username)
        if user_obj:
            raise serializers.ValidationError({"username": "username already exits"})
        return username

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'].lower(),
            password=validated_data['password'],
            username=validated_data['username'],
            date_of_birth=validated_data['date_of_birth'],
        )
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.profile_image = validated_data['profile_image']
        user.phone_number = validated_data['phone_number']
        user.designation = validated_data['designation']
        user.set_password(validated_data['password'])
        user.save()
        return user

    def save(self, **kwargs):
        image_file = self.validated_data.get('profile_image')

        if image_file:
            # Open the image with Pillow
            image = Image.open(image_file)

            # Set the target file size in bytes (e.g., 1 MB = 1,000,000 bytes)
            target_size = 1000000

            # Set the initial quality value and resize the image dimensions
            quality = 95
            width, height = image.size
            aspect_ratio = width / height

            # Calculate the target width and height based on the aspect ratio and desired file size
            target_width = int((target_size * aspect_ratio) ** 0.5)
            target_height = int(target_width / aspect_ratio)

            # Resize the image to the target dimensions
            image = image.resize((target_width, target_height), Image.ANTIALIAS)

            # Create a BytesIO object to save the compressed image
            output_buffer = io.BytesIO()

            # Compress the image with the desired quality
            image.save(output_buffer, format='JPEG', optimize=True, quality=quality)

            # Check the size of the compressed image
            while output_buffer.tell() > target_size and quality > 5:
                # Decrease the quality and compress the image again
                quality -= 5
                output_buffer.truncate(0)
                output_buffer.seek(0)
                image.save(output_buffer, format='JPEG', optimize=True, quality=quality)

            # Create an InMemoryUploadedFile from the BytesIO buffer
            django_file = InMemoryUploadedFile(
                output_buffer,
                None,
                image_file.name,
                'image/jpeg',
                output_buffer.tell(),
                None
            )

            # Assign the Django File object to the image field
            self.validated_data['profile_image'] = django_file

        # Call the superclass save() method to save the model instance
        return super().save(**kwargs)


class UserUpdateSerializear(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', "first_name", "last_name", "phone_number", "designation", "profile_image"]

    def save(self, **kwargs):
        image_file = self.validated_data.get('profile_image')

        if image_file:
            # Open the image with Pillow
            image = Image.open(image_file)

            # Set the target file size in bytes (e.g., 1 MB = 1,000,000 bytes)
            target_size = 1000000

            # Set the initial quality value and resize the image dimensions
            quality = 95
            width, height = image.size
            aspect_ratio = width / height

            # Calculate the target width and height based on the aspect ratio and desired file size
            target_width = int((target_size * aspect_ratio) ** 0.5)
            target_height = int(target_width / aspect_ratio)

            # Resize the image to the target dimensions
            image = image.resize((target_width, target_height), Image.ANTIALIAS)

            # Create a BytesIO object to save the compressed image
            output_buffer = io.BytesIO()

            # Compress the image with the desired quality
            image.save(output_buffer, format='JPEG', optimize=True, quality=quality)

            # Check the size of the compressed image
            while output_buffer.tell() > target_size and quality > 5:
                # Decrease the quality and compress the image again
                quality -= 5
                output_buffer.truncate(0)
                output_buffer.seek(0)
                image.save(output_buffer, format='JPEG', optimize=True, quality=quality)

            # Create an InMemoryUploadedFile from the BytesIO buffer
            django_file = InMemoryUploadedFile(
                output_buffer,
                None,
                image_file.name,
                'image/jpeg',
                output_buffer.tell(),
                None
            )

            # Assign the Django File object to the image field
            self.validated_data['profile_image'] = django_file

        # Call the superclass save() method to save the model instance
        return super().save(**kwargs)
