from rest_framework import serializers
from .models import Question, Submitter, Choice, Answer


class SubmitterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submitter
        fields = ['name', 'date_of_birth', 'adress', 'nationality', 'answer']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question', 'choice', 'answer']




