#0
AREAS = [("Geometria","Geometria",),("Calculo","Cálculo"),("Estatistica","Estatística"),
("Aritimetica","Aritimética"),("Trigonometria","Trigonometria"),("Algebra","Álgebra"),
("Probabilidade","Probabilidade"),("Funcoes","Funções")]
#1
LANGUAGES = [("PT","Português"),("EN","Ingles")]
#2
STATUS = [("Draft","Draft"),("Final","Final"),("Unavailable","Unavailable")];
CONTRIBUTE = [("Author","Author"),("Unknown","Unknown"),("Editor","Editor")];
#4
LOCATION = [("Geogebra","Geogebra"),("Github","Github")];
#5
INTERACTIVITY_TYPE=[("Active","Active"),("Expositive","Expositive"),("Mixed","Mixed"),("Undefined","Undefined")];
INTERACTIVITY_RESOURSE=[("Simulation","Simulation"),("Exercise","Exercise"),("Experiment","Experiment")];
INTERACTIVITY_LEVEL=[("low","low"),("medium","medium"),("high","high")];
CONTEXT=[("Primary","Primary"),("Secondary","Secondary"),("Higher","Higher"),("University","University")];
DIFFICULTY=[("easy","easy"),("medium","medium"),("hard","hard")];
#6
COST=[("yes","yes"),("no","no")];
COPYRIGHT=[("yes","yes"),("no","no")];

######################________Models.py__________#################################################
from django.db import models
class Applet(models.Model):
####################APPLET
    id = models.AutoField                       (primary_key=True)
    title = models.CharField                    (default="none",max_length=20);
    description = models.CharField              (default="none",max_length=20);
    url = models.CharField                      (default="none",max_length=20);
    area = models.CharField                     (choices=AREAS,default="none",max_length=20)
#################IEEE LOM
    #1 General
    language = models.CharField                 (choices=LANGUAGES,default="none",max_length=20)
    #2 Life-Cycle
    status = models.CharField                   (choices=STATUS,default="none",max_length=20);
    contribute = models.CharField               (choices=CONTRIBUTE,default="none",max_length=20);
    #4 Technical
    location = models.CharField                 (choices=LOCATION,default="none",max_length=20);
    #5 Educational
    interactivity_type = models.CharField       (choices=INTERACTIVITY_TYPE,default="none",max_length=20)
    interactivity_resourse = models.CharField   (choices=INTERACTIVITY_RESOURSE,default="none",max_length=20);
    interactivity_level = models.CharField      (choices=INTERACTIVITY_LEVEL,default="none",max_length=20);
    context = models.CharField                  (choices=CONTEXT,default="none",max_length=20);
    difficulty = models.CharField               (choices=DIFFICULTY,default="none",max_length=20);
    #6 Rights
    cost = models.CharField                     (choices=COST,default="none",max_length=20);
    copyright = models.CharField                (choices=COPYRIGHT,default="none",max_length=20);

    def return_fields():
        return(['id','title','description','url','area','language','status','contribute',
        'location','interactivity_type','interactivity_resourse','interactivity_level','context',
        'difficulty','cost','copyright']);

######################________Forms.py__________######################################################
from django import forms #work with forms
class AppletForm(forms.ModelForm):
    class Meta:
        model = Applet; #my model
        fields = "__all__"

class SearchForm(forms.ModelForm):
    class Meta:
        model = Applet;
        fields = "__all__";
        # exclude = ['id','title','description','url'];

######################________Serializers.py__________##############################################
from rest_framework import serializers #import a serializer
class AppletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applet #define o modelo a ser serializado
        fields = "__all__" #todos os atributos devem ser serializados (inclusive id oculto)