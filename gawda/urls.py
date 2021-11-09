from django.contrib import admin
from django.urls import path
from so2alApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('so2al/submitter/', views.SubmitterCreate.as_view()),
    path('so2al/submitter/<int:pk>', views.SubmitterRetrieve.as_view()),
    # path('so2al/answer/', views.AnswerAdd.as_view()),
    path('so2al/question/', views.QuestionRetrieve.as_view())
]
