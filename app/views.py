from django.http import HttpResponse, JsonResponse, HttpRequest #return data response to the page
from django.shortcuts import render, redirect #render = html + django

from .models import Cliente,Cidade,Funcionario,Rota
from .models import ClienteForm,CidadeForm,FuncionarioForm,RotaForm


# Create your views here.
def main(request):
    return(render(request,'app/templates/base.html'))

def CadastroCliente(request):
    instance_form = ClienteForm()

    if(request.method == 'POST'):
        instance_form = ClienteForm(request.POST); #Case sending information to DB, defines form as POST
        instance_form.save();

    ClientesList = []
    Clientes = Cliente.objects.all() #Get all object in the DB and stores in a array to list in the html page
    for cli in Clientes:
        ClientesList.append(cli)

    return(render(request,'app/templates/CadastroCliente.html',{'form':instance_form,'Clientes':ClientesList})) #Go to the client Page

def CadastroCidade(request):
    instance_form = CidadeForm()

    if(request.method == 'POST'):
        instance_form = CidadeForm(request.POST); #Case sending information to DB, defines form as POST
        instance_form.save();

    CidadesList = []
    Cidades = Cidade.objects.all() #Get all object in the DB and stores in a array to list in the html page
    for cit in Cidades:
        CidadesList.append(cit)

    return(render(request,'app/templates/CadastroCidade.html',{'form':instance_form,'Cidades':CidadesList}))

def CadastroFuncionario(request):
    instance_form = FuncionarioForm()

    if(request.method == 'POST'):
        instance_form = FuncionarioForm(request.POST); #Case sending information to DB, defines form as POST
        instance_form.save();

    FuncionariosList = []
    Funcionarios = Funcionario.objects.all() #Get all object in the DB and stores in a array to list in the html page
    for func in Funcionarios:
        FuncionariosList.append(func)

    return(render(request,'app/templates/CadastroFuncionario.html',{'form':instance_form,'Funcionarios':FuncionariosList}))

#origem = str(Cidade.objects.get(name="Teste").latitude) +'%2C'+ str(Cidade.objects.get(name="Teste").longitude) #Lat,Long from diamantina as origin point
destinos = []

import requests #Make requests to external urls
import json
def CalcularRota(request):
    result = [] #holds the final matrix
    if(request.method == 'POST'): #Calcular rota clicked
        string_api= "http://www.mapquestapi.com/directions/v2/routematrix?key=gAQQ0DBuAZAjvg02l6sU4N7cWBvNuW7o&ambiguities=ignore&doReverseGeocode=false&outFormat=json&routeType=fastest&unit=k&allToAll=true&manyToOne=false&from=-18.2381,-43.611" #FROM DIAMANTINA
        for dest in destinos:
            string_api += "&to="+str(dest.latitude)+","+str(dest.longitude) #Get all the lat/long from the clients adress and combine in the url
        result = requests.get(string_api) #Get the json with the distance matrix (result.content)
        json_result = json.loads(result.content)
        result = json_result['distance']

    instance_form = RotaForm()
    Clientes_obj = Cliente.objects.all();
    return(render(request,'app/templates/CalcularRota.html',{'form':instance_form,'Clientes':Clientes_obj,'Destinos':destinos,'Result':result}))

def AdicionarDestino(request,id):
    destino = Cliente.objects.get(id=id)
    destinos.append(destino) #Add new dest in the global array
    return(redirect('Rota'));


#API to return a matrix of distances between coordinates, will be used in the gurobi or like tool 
#https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=40.6655101,-73.89188969999998&destinations=40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.659569%2C-73.933783%7C40.729029%2C-73.851524%7C40.6860072%2C-73.6334271%7C40.598566%2C-73.7527626%7C40.659569%2C-73.933783%7C40.729029%2C-73.851524%7C40.6860072%2C-73.6334271%7C40.598566%2C-73.7527626&key=AIzaSyCA9cWof-bJvsqWfarRG5VMkJ5akQR_m70
