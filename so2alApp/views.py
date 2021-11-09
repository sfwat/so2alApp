from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Submitter
from .serializer import SubmitterSerializer, QuestionSerializer
from .models import Question, Answer
# Create your views here.


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
        qs_id = Answer.objects.exclude(submitter=submitter_id).values_list("question").first()
        if not qs_id:
            return Response({"message": "Already submitted all questions"})
        question = Question.objects.get(pk=qs_id[0])
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    
class Answer(APIView):

    def post(self, request):
        submitter_id = request.GET.get("submitter_id")
        if not submitter_id:
            return Response({"message": "userId is missing"})
        qs_id = Answer.objects.exclude(submitter=submitter_id).values_list("question").first()
        if not qs_id:
            return Response({"message": "Already submitted all questions"})
        question = Question.objects.get(pk=qs_id[0])
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
