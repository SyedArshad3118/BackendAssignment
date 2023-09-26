from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import User, UserProfile, Post
from .serializers import UserSerializer, UserProfileSerializer, PostSerializer
from .forms import UserRegistrationForm
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt


@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
class ProtectedView(APIView):
    def get(self, request):
        user = request.user  # Access the authenticated user
        return Response({"message": f"Hello, {user.username}! This is a protected view."})
    
@csrf_exempt
@authentication_classes([JSONWebTokenAuthentication])  # Use JWT authentication
@permission_classes([IsAuthenticated])  # Require authentication to access the view
def my_protected_view(request):
    user = request.user

    response_data = {
        'message': 'This is a protected view.',
        'user_id': user.id,
        'username': user.username,
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration_form.html', {'form': form})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request, username):
    # Get the user profile based on the username
    user = get_object_or_404(User, username=username)
    profile = user.profile

    # Serialize user profile data
    profile_serializer = UserProfileSerializer(profile)

    # Serialize user's posts
    posts = Post.objects.filter(author=user)
    post_serializer = PostSerializer(posts, many=True)

    # Serialize user's followers and following
    followers_serializer = UserSerializer(user.followers.all(), many=True)
    following_serializer = UserSerializer(user.following.all(), many=True)

    data = {
        'user_profile': profile_serializer.data,
        'user_posts': post_serializer.data,
        'followers': followers_serializer.data,
        'following': following_serializer.data,
    }

    return Response(data, status=status.HTTP_200_OK)



@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            return Response({'access_token': str(access_token)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user is None or not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        return Response({'access_token': str(access_token)}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
