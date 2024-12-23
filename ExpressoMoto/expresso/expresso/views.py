from django.shortcuts import render 
import pyrebase  
from django.http import JsonResponse, HttpResponseRedirect 
from firebase_admin import firestore 
from django.views.decorators.csrf import csrf_exempt 
import json, random
from datetime import datetime
from django.urls import reverse
from django.contrib import messages


  
config={ 
    "apiKey": "AIzaSyD4w3SZYFKMu37cD9npKZADoTyIFXU2nog", 
    "authDomain": "express-c6178.firebaseapp.com", 
    "databaseURL": "https://express-c6178-default-rtdb.firebaseio.com", 
    "projectId": "express-c6178", 
    "storageBucket": "express-c6178.firebasestorage.app", 
    "messagingSenderId": "Use Your messagingSenderId Here", 
    "appId": "1:427820307117:web:067f65abd80af149556c24"
} 
firebase=pyrebase.initialize_app(config) 
authe = firebase.auth() 
database=firebase.database()
db = firestore.client()



def mostrar_dados(request):
    colecao_ref = db.collection('nome_da_colecao')
    docs = colecao_ref.stream()

    dados = []
    for doc in docs:
        dados.append(doc.to_dict())

    return render(request, 'pagina_com_dados.html', {'dados': dados})
  
def home(request): 
    day = database.child('Data').child('Day').get().val() 
    id = database.child('Data').child('Id').get().val() 
    projectname = database.child('Data').child('Projectname').get().val() 
    return render(request,"Home.html",{"day":day,"id":id,"projectname":projectname })



@csrf_exempt
def adicionar_documento(request):
    if request.method == 'POST':
        id = str(random.getrandbits(48))
        nome = request.POST['nome']
        retirada = request.POST['retirada']
        entrega = request.POST['entrega']
        obs = request.POST['obs']
        data_lancamento= str(datetime.now())
        nm_forma_pgto = request.POST['selecao']
        id_motoboy= str('0')
        nm_motoboy= str('Não informado')
        celular = str('8400002022')
        valor = request.POST['valor']
        nm_atendente = str('nome do atendnete')
        status = 0


        db = firestore.client()
        doc_ref = db.collection('entregas').document(id)
        doc_ref.set({
            'id': id,
            'nm_cliente': nome,
            'celular':celular,
            'end_retirada': retirada,
            'end_entrega': entrega,
            'observacao': obs,
            'data_lancamento': data_lancamento,
            'nm_forma_pgto': nm_forma_pgto,
            'id_motoboy':id_motoboy,
            'nm_motoboy':nm_motoboy,
            'valor' : valor,
            'nm_atendente' : nm_atendente,
            'status': status
        })

        colecao_ref = db.collection('entregas') 
       
        documentos = colecao_ref.where('status', '==', 0).stream()
        lista_documentos = []
        for doc in documentos:
            lista_documentos.append(doc.to_dict())
        messages.success(request, "Entrega adicionada com sucesso!")
        return HttpResponseRedirect(reverse('listar_documentos'))
    return JsonResponse({'status': 'Método não permitido'}, status=405)

# Listar documentos sem filtro
def listar_documentos(request):
    db = firestore.client()
    colecao_ref = db.collection('usuarios')
    documentos = colecao_ref.stream()

    lista_documentos = []
    for doc in documentos:
        lista_documentos.append(doc.to_dict())

    return render(request, 'entregas.html', {'documentos': lista_documentos})



# Função para remover entrega

@csrf_exempt
def remover_documento(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        
        if not id:
            messages.error(request, "Nome do documento não fornecido.")
            return HttpResponseRedirect(reverse('sua_url_para_a_lista_de_documentos'))  # Redireciona para a página de lista

        # Conexão com o Firestore para remover o documento
        db = firestore.client()
        doc_ref = db.collection('entregas').document(id)

        # Verifica se o documento existe
        if doc_ref.get().exists:
            doc_ref.delete()
            messages.success(request, "Documento removido com sucesso!")
        else:
            messages.error(request, "Documento não encontrado.")
        
        return HttpResponseRedirect(reverse('listar_documentos'))  # Redireciona após a exclusão
    else:
        return HttpResponseRedirect(reverse('sua_url_para_a_lista_de_documentos'))  # Caso o método não seja POST


# Função para filtrar entrega

def filtrar_documentos(request):
    db = firestore.client()
    colecao_ref = db.collection('entregas')

    # Exemplos de filtros:
    # Filtrar por idade maior que 25
    documentos_filtrados = colecao_ref.where('status', '==', 0).stream()
    
    # Filtrar por cidade específica
    # documentos_filtrados = colecao_ref.where('cidade', '==', 'São Paulo').stream()

    lista_documentos_filtrados = []
    for doc in documentos_filtrados:
        lista_documentos_filtrados.append(doc.to_dict())

    return render(request, 'entregas.html', {'documentos': lista_documentos_filtrados})



def home(request):
    return render(request, 'home.html')

def entregas(request):
    return render(request, 'entregas.html')

# def about(request):
#     return render(request, 'about.html')

# def contact(request):
#     return render(request, 'contact.html')
