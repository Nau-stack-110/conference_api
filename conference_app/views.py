from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.generics import ListAPIView
from rest_framework import viewsets, permissions
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import MytokenObtainPairSerializer, RegisterSerializer, SessionSerializerList, StatisticSerializer, UserSerializerProfile, ProfileSerializer, ConferenceSerializer, RegistrationSerializer, ConferenceCreateSerializer, RegistrationCreateSerializer, SessionSerializer
from .models import Profile, Session, User, Conference, Registration
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.utils import timezone
from rest_framework import serializers
from django.conf import settings

class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class UserProfileView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializerProfile
  
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MytokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class RegisterView2(APIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConferenceListView(generics.ListAPIView):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer

class ConferenceDetailView(generics.RetrieveAPIView):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer

    def get_queryset(self):
        return Conference.objects.prefetch_related('sessions', 'sessions__registrations')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        
        total_participants = Registration.objects.filter(
            session__conference=instance
        ).values('user').distinct().count()
        
        data['total_participants'] = total_participants
        return Response(data)

class RegistrationListView(generics.ListAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        conference_id = self.request.query_params.get('conference_id')
        if conference_id:
            return Registration.objects.filter(session__conference_id=conference_id)
        return Registration.objects.all()

class ConferenceCreateView2(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def post(self, request):
        serializer = ConferenceCreateSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ConferenceCreateView(generics.CreateAPIView):
    queryset = Conference.objects.all()
    serializer_class = ConferenceCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  

class RegistrationCreateView(generics.CreateAPIView):
    serializer_class = RegistrationCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            registration = serializer.save()
            
            # Générer le ticket
            from .ticket_generator import TicketGenerator
            ticket_generator = TicketGenerator(registration)
            ticket_path = ticket_generator.generate_ticket()
            
            return Response({
                'message': 'Inscription réussie',
                'conference': registration.session.conference.title,
                'session': registration.session.title,
                'date': registration.session.start_time,
                'ticket_url': request.build_absolute_uri(settings.MEDIA_URL + ticket_path)
            }, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class StatisticView(viewsets.ModelViewSet):
    queryset = Conference.objects.all()
    serializer_class = StatisticSerializer
    http_method_names = ['get']
    def list(self, request, *args, **kwargs ):
        stats = {
            "conferences":Conference.objects.count(),
            "registrations":Registration.objects.count(),
            "users":User.objects.count(),
        }
        serializer = self.get_serializer(stats)
        return JsonResponse(serializer.data)  

class SessionCreateView2(generics.CreateAPIView):
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class SessionCreateView(generics.CreateAPIView):
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Les données doivent être une liste."}, status=status.HTTP_400_BAD_REQUEST)

class ConferenceUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Conference.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ConferenceCreateSerializer
        return ConferenceSerializer
    
    def perform_destroy(self, instance):
        # Vérifier s'il y a des inscriptions
        if Registration.objects.filter(session__conference=instance).exists():
            raise serializers.ValidationError(
                "Impossible de supprimer une conférence qui a des participants inscrits"
            )
        instance.delete()

class SessionUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def perform_destroy(self, instance):
        # Vérifier s'il y a des inscriptions
        if instance.registrations.exists():
            raise serializers.ValidationError(
                "Impossible de supprimer une session qui a des participants inscrits"
            )
        instance.delete()
    
    def perform_update(self, serializer):
        session = self.get_object()
        if session.registrations.exists():
            new_start_time = serializer.validated_data.get('start_time')
            if new_start_time and abs((new_start_time - session.start_time).days) > 0:
                raise serializers.ValidationError(
                    "Impossible de changer la date d'une session qui a des participants inscrits"
                )
        serializer.save()

class VerifyRegistrationView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, unique_code):
        try:
            registration = Registration.objects.get(unique_code=unique_code)
            return Response({
                'message': 'Inscription vérifiée',
                'conference': registration.session.conference.title,
                'session': registration.session.title,
                'date': registration.session.start_time,
                'participant': registration.user.username
            })
        except Registration.DoesNotExist:
            return Response({'error': 'Inscription non trouvée'}, status=404)


class SessionViewList(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializerList
  