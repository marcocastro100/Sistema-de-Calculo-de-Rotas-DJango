from django.db import models #Use models objects
from django import forms #use already ready forms for each model

#Models
class Cidade(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    latitude = models.FloatField()
    new = models.FloatField()
    longitude = models.FloatField()
    def __str__(self):
        return(self.name)

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    cidade = models.ForeignKey(Cidade,on_delete=models.CASCADE,null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    def __str__(self):
        return(self.name)

class Funcionario(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    idade = models.IntegerField()
    def __str__(self):
        return(self.name)

class Rota(models.Model):
    id = models.AutoField(primary_key=True)
    clientes = models.ForeignKey(Cliente,on_delete=models.CASCADE,null=True)
    cidade = models.ForeignKey(Cidade,on_delete=models.CASCADE,null=True)
    funcionario = models.ForeignKey(Funcionario,on_delete=models.CASCADE,null=True)
    

#Forms
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"

class CidadeForm(forms.ModelForm):
    class Meta:
        model = Cidade
        fields = "__all__"

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = "__all__"

class RotaForm(forms.ModelForm):
    class Meta:
        model = Rota
        fields = ["cidade","funcionario"]
