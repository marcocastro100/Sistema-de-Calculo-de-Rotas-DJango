from django.http import HttpResponse, JsonResponse #return data response to the page
from .models import Applet #Import applet DB model
from .models import AppletForm, SearchForm #Import Applet form (all fields) and Search (context, language)
from .models import AppletSerializer #importing created serializer (convert a structure to a dictionary)

############################______G U I______##################################################################
from django.shortcuts import render #integrate the view to the html on templates
from django.shortcuts import redirect #redirect to other pages
import json #Work with json files

#===================================================
def LOM_serializer(applet): #Transforms a model applet in a dictionary in the IEEE LOM format
    serialized = {
        "Applet":{
            "id":applet.id,
            "title":applet.title,
            "description":applet.description,
            "url":applet.url,
            "area":applet.area,
        },
        "General":{
            "language":applet.language
        },
        "Life_cycle":{
            "status":applet.status,
            "contribute":applet.contribute
        },
        "Technical":{
            "location":applet.location
        },
        "Educational":{
            "interactivity_type":applet.interactivity_type,
            "interactivity_resourse":applet.interactivity_resourse,
            "interactivity_level":applet.interactivity_level,
            "context":applet.context,
            "difficulty":applet.difficulty
        },
        "Rights":{
            "cost":applet.cost,
            "copyright":applet.copyright
        }
    };
    return(serialized);
#==============================================================================
def applets_list(request): #Root /applets: list all Applets models instances
    json_list=[];
    instance = Applet.objects.all(); #Catch all instances in the database
    for ins in instance:
        json_list.append(LOM_serializer(ins));
    return(render(request,'Applets/templates/list.html',{'Applets':json_list})) #Handles how that json will be showed in the browser (iteration)

#=====================================================================
def applets_detail(request,id): #Active when a applet id (pk) is selected (an is in the url (pk [urls.py]))
    instance = Applet.objects.get(id=id); #get the specific applet by the primary key
    instance_dict = AppletSerializer(instance); #selected applet in serialized mode
    instance_json = json.dumps(instance_dict.data); #To json for correcly show in browser
    instance_form =  AppletForm(request.POST or None, instance=instance); #Creates a form with POST (change) data, where the default values showed are the current values of the instance
    if (request.method == 'POST'):
        instance_form.save(); #verify if is valid and saves it
    return(render(request,'Applets/templates/detail.html',{'Applet':json.loads(instance_json),'form':instance_form}))

#=====================================================================
def applets_create(request): #creates a new applet
    if(request.method == 'GET'):
        instance_form = AppletForm(); #Just entering the page, define the form as GET
    elif(request.method == 'POST'):
        instance_form = AppletForm(request.POST); #Case sending information to DB, defines form as POST
        instance_form.save();
    return(render(request,'Applets/templates/create.html',{'form':instance_form})) #sends to template to render it in html forms

#=====================================================================
def applets_delete(request,id):
    instance = Applet.objects.get(id=id); #get the deleting id
    instance.delete() #deletes from db
    return(redirect('../../')); #redirect to other page

#=====================================================================
import os #Controls the Operacional system (create a folder/file if not exists yet)
def applets_download(request,id):
    instance = Applet.objects.get(id=id);
    instance_dict = LOM_serializer(instance);
    instance_json = json.dumps(instance_dict,indent=3);
    return JsonResponse(instance_dict, json_dumps_params={'indent': 2})

#=====================================================================
def applets_search(request):
    if(request.method == 'GET'):
        instance_form = SearchForm(); #Form with only key search fields
        return(render(request,'Applets/templates/search.html',{'form':instance_form}))

    if(request.method == 'POST'):
        instances = Applet.objects.filter( #Take the instances in the BD with the informed keys
            title = request.POST['title'],
            description = request.POST['description'],
            url = request.POST['url'],
            area = request.POST['area'],
            language = request.POST['language'],
            status = request.POST['status'],
            contribute = request.POST['contribute'],
            location = request.POST['location'],
            interactivity_type = request.POST['interactivity_type'],
            interactivity_resourse = request.POST['interactivity_resourse'],
            interactivity_level = request.POST['interactivity_level'],
            context = request.POST['context'],
            difficulty = request.POST['difficulty'],
            cost = request.POST['cost'],
            copyright = request.POST['copyright']
        ); 
        instances_dict = [];
        for inst in instances:
            instances_dict.append(LOM_serializer(inst));
        instance_form = SearchForm(request.POST or None, instance=instances[0] if instances else None); #instances to continue with current search key values in the form
        return(render(request,'Applets/templates/search.html',{'form':instance_form,'instances':instances_dict}))

#=====================================================================


from rest_framework import viewsets
class AppletView(viewsets.ModelViewSet):

    queryset = Applet.objects.all()
    serializer_class = AppletSerializer 

    def get_queryset(self): #Função responsável pela busca via url
        queryset = Applet.objects.all() #Pega todos os objetos no banco de dados
        model_fields = Applet.return_fields() #Pega o nome de todos os campos do modelo
        search_param = []
        for field in model_fields: #Para cada field do modelo (cada potencial busca)
            filtro = self.request.query_params.get(field,None); #Pega objetos correspondentes no banco de dados
            if (filtro is not None and filtro != ''): #Caso tenho retornado um objeto exitente
                search_param.append(field) #registra que o field x foi informado como parametro de busca

        #Com queryset(todos objetos no db), ir filtrando o resultado a medida que filtros validos vão sendo contabilizados
        if('id' in search_param): queryset = queryset.filter(id=self.request.query_params.get('id',None));
        if('title' in search_param): queryset = queryset.filter(title=self.request.query_params.get('title',None));
        if('description' in search_param): queryset = queryset.filter(description=self.request.query_params.get('description',None));
        if('url' in search_param): queryset = queryset.filter(url=self.request.query_params.get('url',None));
        if('area' in search_param): queryset = queryset.filter(area=self.request.query_params.get('area',None));
        if('language' in search_param): queryset = queryset.filter(language=self.request.query_params.get('language',None));
        if('status' in search_param): queryset = queryset.filter(status=self.request.query_params.get('status',None));
        if('contribute' in search_param): queryset = queryset.filter(contribute=self.request.query_params.get('contribute',None));
        if('location' in search_param): queryset = queryset.filter(location=self.request.query_params.get('location',None));
        if('interactivity_type' in search_param): queryset = queryset.filter(interactivity_type=self.request.query_params.get('interactivity_type',None));
        if('interactivity_resourse' in search_param): queryset = queryset.filter(interactivity_resourse=self.request.query_params.get('interactivity_resourse',None));
        if('interactivity_level' in search_param): queryset = queryset.filter(interactivity_level=self.request.query_params.get('interactivity_level',None));
        if('context' in search_param): queryset = queryset.filter(context=self.request.query_params.get('context',None));
        if('difficulty' in search_param): queryset = queryset.filter(difficulty=self.request.query_params.get('difficulty',None));
        if('cost' in search_param): queryset = queryset.filter(cost=self.request.query_params.get('cost',None));
        if('copyright' in search_param): queryset = queryset.filter(copyright=self.request.query_params.get('copyright',None));
        
        return (queryset);

    def put(self, request, id): # using curl -X PUT http://localhost:8000/api/api/x/ --data 'field=newvalue' or adding more --datas we can update a object individualy (not usable with url for http forms can only handle GET e POST)
        instancia = Applet.objects.get(id) #Pega todos os objetos no banco de dados
        model_fields = Applet.return_fields() #Pega o nome de todos os campos do modelo
        search_param = []
        for field in model_fields: #Para cada field do modelo (cada potencial busca)
            filtro = self.request.query_params.get(field,None); #Pega objetos correspondentes no banco de dados
            if (filtro is not None and filtro != ''): #Caso tenho retornado um objeto exitente
                instancia.field = filtro;
                instancia.save();










#Na mão.....
# ############################______A P I______##################################################################
# from rest_framework.views import APIView #enables the use of class view (better looking and same as function)
# from rest_framework.response import Response #Smart response (json, api, error handling, etc)
# from rest_framework import status #status from response to avoid error page

# #=====================================================================
#     #Dealing with a external system requiring not specified applet in url
# class api_list(APIView): 

#         #Show all applets in json format
#     def get(self,request): #format=None: deal with extra url parameter (like .json)
#         instance = Applet.objects.all();
#         instance_dict = AppletSerializer(instance,many=True);
#         return(Response(instance_dict.data));

#         #Create a new applet (post=create)
#     def post(self,request):
#         new_instance = request.data;
#         new_instance_dict = AppletSerializer(data=new_instance);
#         if(new_instance_dict.is_valid()):
#             new_instance_dict.save();
#             return Response(new_instance_dict.data,status=201); #201 = Created
#         else: return(HttpResponse('Bad Data Input')) #400 = BadRequest

# #======================================================================================================
#         #External System requiring a specific applet
#     # from django.views.decorators.csrf import csrf_exempt
# class api_detail(APIView): 

#         #Gets the current instance of applet givened by url
#     def pick_instance(self,id):
#         current_instance = Applet.objects.get(id=id);
#         return(current_instance);

#         #Show the applet in json format    
#     def get(self,request,id):
#         instance = self.pick_instance(id);
#         instance_dict = AppletSerializer(instance);
#         return(Response(instance_dict.data));

#         #Delete the applet from the server        
#     def delete(self,request,id):
#         instance = self.pick_instance(id);
#         instance.delete()
#         return(Response(status=204)) #204 = No Content

#         #Modify the applet in the server database    
#     def put(self,request,id):
#         instance = self.pick_instance(id);
#         instance_dict = AppletSerializer(instance,data=request.data);
#         if(instance_dict.is_valid()):
#             instance.save();
#             return(Response(instance_dict.data));
#         else:
#             return(HttpResponse('Bad Data Input!'))
#         return(Response(status=200));

# #======================================================================================================
#     #Search for jsons returns by key search in the model
# class api_search(APIView): 
#     def get(self,request): #only generates the form for search
#         return(HttpResponse('Para buscar metadados, envie um method POST para este endereço com as keys do IEEE-LOM:'))

#     def post(self,request): #Makes a search for the entry data, returning the jsons maching the pattern
#         instances = Applet.objects.filter( #Take the instances in the BD with the informed keys
#             area = request.data['area'],
#             language = request.data['language'],
#             contribute = request.data['contribute'],
#             location = request.data['location'],
#             interactivity_type = request.data['interactivity_type'],
#             interactivity_resourse = request.data['interactivity_resourse'],
#             interactivity_level = request.data['interactivity_level'],
#             context = request.data['context'],
#             difficulty = request.data['difficulty'],
#             cost = request.data['cost'],
#             copyright = request.data['copyright']
#         ); 
#         instances_dict = [];
#         for inst in instances:
#             instances_dict.append(LOM_serializer(inst));
#         return(Response(instances_dict)); #sends the data in json format