from rest_framework import serializers
from .models import Question, Submitter, Choice, Answer


class SubmitterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submitter
        fields = ['id', 'name', 'gender', 'answer']


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ('id', 'choice_text')


class QuestionSerializer(serializers.ModelSerializer):

    choice = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['question', 'choice']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'




