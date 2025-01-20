from rest_framework import serializers
from .models import Profile, User, Session, Registration, Conference
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_superuser']
        
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = ['fullname', 'verified', 'bio', 'image', 'user', 'created_at']

class UserSerializerProfile(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True) 
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_superuser', 'profile']       

class MytokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['fullname'] = user.profile.fullname
        token['username'] = user.username
        token['email'] = user.email
        token['bio'] = user.profile.bio
        token['image'] = str(user.profile.image)  # Convertion chaîne, nécessaire be
        token['verified'] = user.profile.verified  
        token['is_superuser'] = user.is_superuser 
        token['is_staff'] = user.is_staff          
        
        return token

# register serializer    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model=User
        fields =  ['email', 'username', 'password', 'password2']    
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields does not match"}
            )    
        return attrs
        
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
            
        return user
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur existe déjà.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email existe déjà.")
        return value

class SessionSerializer(serializers.ModelSerializer):
    participants_count = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = ['id', 'title', 'speaker', 'profession', 'start_time', 'conference', 'participants_count']

    def validate(self, data):
        conference = data.get('conference')
        start_time = data.get('start_time')
        
        if conference and start_time:
            # Vérifier que la date de session est le même jour que la conférence
            if start_time.date() != conference.date:
                raise serializers.ValidationError(
                    "La date de la session doit être le même jour que la conférence"
                )
            
            # Vérifier que la date n'est pas dans le passé
            if start_time < timezone.now():
                raise serializers.ValidationError(
                    "La date de la session ne peut pas être dans le passé"
                )
        
        return data

    def get_participants_count(self, obj):
        return obj.registrations.count()

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['id', 'user', 'session', 'registered_at']

class ConferenceSerializer(serializers.ModelSerializer):
    sessions = SessionSerializer(many=True, read_only=True)
    total_participants = serializers.SerializerMethodField()    
    class Meta:
        model = Conference
        fields = ['id', 'title', 'description', 'image', 'date', 'lieu', 'price', 'category', 'created_at', 'sessions', 'total_participants']
    
    def get_total_participants(self, obj):
        return Registration.objects.filter(
            session__conference=obj
        ).values('user').distinct().count()

class ConferenceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conference
        fields = ['title', 'description', 'image', 'date', 'price', 'lieu', 'category']

    def validate_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("La date de la conférence ne peut pas être dans le passé.")
        return value

class RegistrationCreateSerializer(serializers.ModelSerializer):
    conference_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Registration
        fields = ['conference_id', 'session']
        read_only_fields = ['session']

    def validate_conference_id(self, value):
        try:
            conference = Conference.objects.get(id=value)
            # Vérifier si la conférence a des sessions
            if not conference.sessions.exists():
                raise serializers.ValidationError("Cette conférence n'a pas de sessions disponibles.")
            return value
        except Conference.DoesNotExist:
            raise serializers.ValidationError("Cette conférence n'existe pas.")

    def create(self, validated_data):
        user = self.context['request'].user
        conference_id = validated_data.pop('conference_id')
        
        # Récupérer la première session disponible de la conférence
        session = Session.objects.filter(
            conference_id=conference_id,
            start_time__gt=timezone.now()
        ).first()
        
        if not session:
            raise serializers.ValidationError("Aucune session disponible pour cette conférence.")
        
        if Registration.objects.filter(user=user, session=session).exists():
            raise serializers.ValidationError("Vous êtes déjà inscrit à cette session.")
        
        registration = Registration.objects.create(
            user=user,
            session=session
        )
        return registration


class StatisticSerializer(serializers.Serializer):
      conferences = serializers.IntegerField()  
      registrations = serializers.IntegerField()    
      users = serializers.IntegerField()
    