import datetime
from venv import create

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse 


from .models import Question

# Normalmente se testean Modelos y Vistas
# Testeo del modelo Question
class QuestionModelTest(TestCase): #clase de modulo test de django que permite definir una bateria de test(conjunto de test que se corresponde a un aspecto particular de la app)

    def test_was_publish_recently_whit_future_question(self):
        """"This method return False for question whose pub_date is in the future """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="¿Quien es el mejor Course Direct de platzi", pub_date=time)
        self.assertIs(future_question.was_publish_recently(), False)
    
    def test_was_publish_recently_whit_past_question(self):
        """This method return False for question whose pub_date is in the past > 2 days """
        time = timezone.now() - datetime.timedelta(days=2)
        past_question = Question(question_text="¿Quien es el mejor Course Direct de platzi", pub_date=time)
        self.assertIs(past_question.was_publish_recently(), False)
    
    def test_was_publish_recently_whit_now_question(self):
        """"This method return False for question whose pub_date is now """
        time = timezone.now() 
        future_question = Question(question_text="¿Quien es el mejor Course Direct de platzi", pub_date=time)
        self.assertIs(future_question.was_publish_recently(), True)

def create_question(question_text, days):
    """Create a question with the given question_text and published the given number of days offset to now(negative for questions published in the past and positive for question that have yet to be published"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        """If no question exist, an appropiate message is displayed"""
        response = self.client.get(reverse("polls:index"))#Reverse nos permite no hardcodear una url y ponerla de manera dinamica y self.client.get() hace una peticion http sobre esa vista (polls:index) 
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])
    
    def test_future_question(self):
        "If exist a future question, the view doesn't show that"
        future_question = create_question("¿Mejor CD platzi?", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertNotContains(response,future_question)
    
    def test_past_question(self):
        """Question with a publ_date in the past are displayed on the index page"""
        question = create_question("Past question", -10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[question])
    
    def test_future_question_and_past_question(self):
        """Even if both past and future question exist, only pas question are displayed"""
        past_question = create_question("Paste question", -30)
        future_question = create_question("Paste question", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question]
        )
        
    def test_two_past_question(self):
        """The question index page may display multiple questions"""
        past_question1 = create_question("Paste question1", -30)
        past_question2 = create_question("Paste question2", -40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question1, past_question2]
        )
    
    def test_two_future_question(self):
        """The question index page shoud not display multiple questions"""
        future_question1 = create_question("Paste question1", 30)
        future_question2 = create_question("Paste question2", 40)
        response = self.client.get(reverse("polls:index"))
        self.assertNotEquals(response.context["latest_question_list"], [future_question1, future_question2])

class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """The detail view of a question with pub_date in the future returns a 404 error not found"""
        future_question = create_question("Paste question1", 30)
        url = reverse("polls:detail", args=(future_question.id,))#Trae la url del detalle de la pregunta y se le pasa los paramaetros con args
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past display de question test"""
        past_question = create_question("Paste question1", -30)
        url = reverse("polls:detail", args=(past_question.id,))#Trae la url del detalle de la pregunta y se le pasa los paramaetros con args
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)