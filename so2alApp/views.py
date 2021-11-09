from django.http import Http404
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Submitter
from .serializer import SubmitterSerializer, QuestionSerializer, AnswerSerializer
from .models import Question, Answer


class SubmitterCreate(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = SubmitterSerializer

    def post(self, request):
        return self.create(request)


class SubmitterRetrieve(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = Submitter.objects.all()
    serializer_class = SubmitterSerializer

    def get(self, request, pk):
        return self.retrieve(request)

    def put(self, request, pk):
        return self.update(request)


class QuestionRetrieve(APIView):

    def get(self, request):
        submitter_id = request.GET.get("submitter_id")
        if not submitter_id:
            return Response({"message": "userId is missing"})
        qs_id = Answer.objects.filter(submitter=submitter_id).values_list("question")
        question = Question.get_question(qs_id)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)


class AnswerSubmit(APIView):

    def post(self, request):

        serializer = AnswerSerializer(data = request.data)
        if serializer.is_valid():
            question = serializer.validated_data.get("question")
            if question.already_submitted(serializer.validated_data.get("submitter").id):
                return Response({"message": "user already submitted this question"}, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status.HTTP_400_BAD_REQUEST)


class QuestionStats(APIView):
    def get(self, request, pk):
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404
        stats = question.choice_percent()
        return Response({"stats": stats}, status.HTTP_200_OK)

