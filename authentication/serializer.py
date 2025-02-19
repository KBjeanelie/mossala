from authentication.models import User, UserStatus
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['tel',  'password', 'status']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        tel = validated_data['tel']
        status = validated_data['status']
        if User.objects.filter(tel=tel).exists():
            raise serializers.ValidationError('Un utilisateur avec ce numéro de téléphone existe déjà.')

        user = User.objects.create_user(
            tel=tel,
            password=validated_data['password']
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    tel = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        tel = attrs.get('tel')
        password = attrs.get('password')

        if tel and password:
            try:
                user = User.objects.get(tel=tel)
            except User.DoesNotExist:
                raise serializers.ValidationError('Aucun utilisateur avec ce numéro de téléphone.')
            
            if not user.check_password(password):
                raise serializers.ValidationError('Mot de passe incorrect.')

            if not user.is_active:
                raise serializers.ValidationError('Utilisateur inactif.')

            refresh = self.get_token(user)

            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }
        else:
            raise serializers.ValidationError('Numéro de téléphone et mot de passe requis.')

        return super().validate(attrs)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'status': {'many': True},
        }
        
    def create(self, validated_data):
        status_data = validated_data.pop('status', [])
        user = User.objects.create(**validated_data)
        for status in status_data:
            user.status.add(UserStatus.objects.get(status=status['status']))
        return user

    def update(self, instance, validated_data):
        status_data = validated_data.pop('status', [])
        instance.username = validated_data.get('username', instance.username)
        instance.tel = validated_data.get('tel', instance.tel)
        instance.email = validated_data.get('email', instance.email)
        instance.email_verified = validated_data.get('email_verified', instance.email_verified)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        instance.save()

        if status_data:
            instance.status.clear()
            for status in status_data:
                instance.status.add(UserStatus.objects.get(status=status['status']))

        return instance
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Un utilisateur avec cet email existe déjà.')
        return value
    
    def validate_tel(self, value):
        if User.objects.filter(tel=value).exists():
            raise serializers.ValidationError('Un utilisateur avec ce numéro de téléphone existe déjà.')
        return value
    
    def validate_roles(self, value):
        for role in value:
            if not UserStatus.objects.filter(name=role).exists():
                raise serializers.ValidationError(f"Le rôle '{role}' n'existe pas.")
        return value