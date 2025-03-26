from rest_framework import serializers
from backend.models.manager_profil import UserExperience, UserEducation, UserLanguage, UserPortfolio, UserRealisation, UserRecommendation

class UserExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExperience
        fields = '__all__'

class UserEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEducation
        fields = '__all__'

class UserLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLanguage
        fields = '__all__'

class UserPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPortfolio
        fields = '__all__'

class UserRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRecommendation
        fields = '__all__'


class UserRealisationSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = UserRealisation
        fields = '__all__'
    
    
    def create(self, validated_data):
        try:
            realisation = super().create(validated_data)
            realisation.save()
            return realisation
        except Exception as e:
            return {"error": str(e)}