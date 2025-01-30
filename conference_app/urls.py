from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConferenceCreateView2, RegisterView2, RegistrationListView, ProfileView, SessionCreateView2, SessionViewList, StatisticView, UserProfileView, MyTokenObtainPairView, RegisterView, ConferenceListView, ConferenceDetailView, ConferenceCreateView, RegistrationCreateView, SessionCreateView, ConferenceUpdateDeleteView, SessionUpdateDeleteView, VerifyRegistrationView, MyTicketsView, ConferenceDateRangeView, AdminAddParticipantView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register('profile', ProfileView, basename='profile')
router.register('user-profile', UserProfileView, basename='user-profile')
router.register('stats', StatisticView, basename='stats')
router.register('sessions', SessionViewList, basename='sessions')

urlpatterns = [
    path('token/',MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register_betsaka/', RegisterView2.as_view(), name='register_betsaka'),
    
    path('conferences/', ConferenceListView.as_view(), name='conference_list'),
    path('conferences/<int:pk>/', ConferenceDetailView.as_view(), name='conference_detail'),
    path('registrations/', RegistrationListView.as_view(), name='registration_list'),
    path('conferences/create_betsaka/', ConferenceCreateView2.as_view(), name='conference_create_betsaka'),
    path('conferences/create/', ConferenceCreateView.as_view(), name='conference_create'),
    path('register-conference/', RegistrationCreateView.as_view(), name='register_conference'),
    path('sessions/create/', SessionCreateView2.as_view(), name='session_create'),
    path('sessions/create_betsaka/', SessionCreateView.as_view(), name='session_create_betsaka'),
    path('conferences/<int:pk>/update/', ConferenceUpdateDeleteView.as_view(), name='conference-update-delete'),
    path('sessions/<int:pk>/update/', SessionUpdateDeleteView.as_view(), name='session-update-delete'),
    path('verify/<str:unique_code>/', VerifyRegistrationView.as_view(), name='verify_registration'),
    path('my-tickets/', MyTicketsView.as_view(), name='my-tickets'),
    path('conferences/date-range/', ConferenceDateRangeView.as_view(), name='conference-date-range'),
    path('admin/add-participant/', AdminAddParticipantView.as_view(), name='admin-add-participant'),
]

urlpatterns += router.urls
