from django.contrib import admin
from polls.models import Question, Choice

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_text"]
    inlines = [ChoiceInline]#Permite agregar las respuestas al momento de crear una pregunta
    list_display = ("question_text", "pub_date")#Permite visualizar diferentes campos en el admin 
    list_filter = ["pub_date"]#No permite filtrar por un campo especifico 
    search_fields = ["question_text"]


admin.site.register(Question, QuestionAdmin)
