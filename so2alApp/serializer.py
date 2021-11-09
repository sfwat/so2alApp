from rest_framework import serializers
from .models import Question, Submitter, Choice, Answer


class SubmitterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submitter
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    choice = serializers.StringRelatedField(many=True)

    class Meta:
        model = Question
        fields = ['question', 'choice']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'




