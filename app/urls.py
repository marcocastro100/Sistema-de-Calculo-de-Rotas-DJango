from django.urls import path, include #way to redirect web page to the project tree structure
from . import views

urlpatterns = [
    #GUI
    path('',views.main,name='main'),
    path('CadastroCliente',views.CadastroCliente,name='Clientes'),
    path('CadastroCidade',views.CadastroCidade,name='Cidades'),
    path('CadastroFuncionario',views.CadastroFuncionario,name='Funcionarios'),
    path('CalcularRota',views.CalcularRota,name='Rota'),
    path('AdicionarDestino/<int:id>/',views.AdicionarDestino,name='Destino'),
]