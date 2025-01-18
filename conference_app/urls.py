from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistrationListView, ProfileView, StatisticView, UserProfileView, MyTokenObtainPairView, RegisterView, ConferenceListView, ConferenceDetailView, ConferenceCreateView, RegistrationCreateView, SessionCreateView, ConferenceUpdateDeleteView, SessionUpdateDeleteView, VerifyRegistrationView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register('profile', ProfileView, basename='profile')
router.register('user-profile', UserProfileView, basename='user-profile')
router.register('stats', StatisticView, basename='stats')

urlpatterns = [
    path('token/',MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
   
    path('conferences/', ConferenceListView.as_view(), name='conference_list'),
    path('conferences/<int:pk>/', ConferenceDetailView.as_view(), name='conference_detail'),
    path('registrations/', RegistrationListView.as_view(), name='registration_list'),
    path('conferences/create/', ConferenceCreateView.as_view(), name='conference_create'),
    path('register-conference/', RegistrationCreateView.as_view(), name='register_conference'),
    path('sessions/create/', SessionCreateView.as_view(), name='session_create'),
    path('conferences/<int:pk>/update/', ConferenceUpdateDeleteView.as_view(), name='conference-update-delete'),
    path('sessions/<int:pk>/update/', SessionUpdateDeleteView.as_view(), name='session-update-delete'),
    path('verify/<str:unique_code>/', VerifyRegistrationView.as_view(), name='verify_registration'),
]

urlpatterns += router.urls
