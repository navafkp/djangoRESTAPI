
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import CustomUserSerializer
from .models import CustomUser, UserImage
import jwt, datetime
from rest_framework.exceptions import ValidationError
from rest_framework import status

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        phone = data.get('phone')
        if CustomUser.objects.filter(email=email).exists():
            print('Email already exists')
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(phone=phone).exists():
            print('Phone number already exists')
            return Response({'error': 'Phone number already exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomUserSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
       
        print(email)
        print(password)
        if not (email and password):
            return Response({
                'error': 'Email and Password is required'
            })
       
        user = CustomUser.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed({
                'error':'User is not found'
            })
        
        if not user.check_password(password):
            raise AuthenticationFailed({'error':'Incorrrect Password'})
        
        payload = {
            'id':user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm="HS256")
        response = Response()
    
        response.data = {
            'jwt': token
        }
    
        return response
    

class UserView(APIView):
    def get(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or 'Bearer ' not in auth_header:
            raise AuthenticationFailed("Not authorized")

        token = auth_header.split('Bearer ')[1]
        try:
            payload = jwt.decode(token, 'secret', algorithms=["HS256"])
            user = CustomUser.objects.filter(id=payload['id']).first()
            serializer = CustomUserSerializer(user)
            return Response(serializer.data)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Not authorized")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

    
 
from .serializers import ImageSerializer  # Import the serializer

class UserImageView(APIView):
    def post(self, request):
        user_firstname = request.data.get('user_firstname')
        print(user_firstname)
        try:
            user_obj = CustomUser.objects.filter(first_name=user_firstname).first()
            print(user_obj)
            user_image, created = UserImage.objects.get_or_create(user=user_obj)
            print(user_image)

            # Access the image data from request.FILES
            if 'image' in request.FILES:
                image_file = request.FILES['image']
                print(image_file)
                user_image.image.save(image_file.name, image_file, save=True)
                user_image.save()
                
                # Serialize the data
                serializer = ImageSerializer(user_image)
                serialized_data = serializer.data

                # Print the serialized data
                print(f"Serialized Data: {serialized_data}")

                return Response(status=200)
            else:
                return Response({'error': 'No image file found'}, status=400)
        except CustomUser.DoesNotExist as e:
            return Response({'error': 'User not found'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)



class UserLogout(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        
        return response

        
       
        