from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import User, Arquivos
from datetime import datetime

import pandas as pd
import os
from django.conf import settings

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    return redirect('login')

@login_required
def change_password(request):

    if request.method == 'POST':
        if request.POST['password'] != request.POST['confirm_password']:
            return render(request, 'registration/change_password.html', {'error': 'As senhas não coincidem.'})
        else:
            password = request.POST['password']
            request.user.set_password(password)
            request.user.first_login = False
            request.user.save()
            return redirect('table')

    return render(request, 'registration/change_password.html')

@login_required
def create_user(request):
    if request.method == 'POST':
        l = request.user.groups.values_list('name',flat = True) # QuerySet Object
        l_as_list = list(l)                              

        if request.user.is_superuser or 'Gerenciador de Contas' in l_as_list:
            if request.POST['password'] != request.POST['confirm_password']:
                return render(request, 'registration/create_user.html', {'error': 'As senhas não coincidem.'})
            else:
                username = request.POST['username']
                password = request.POST['password']
                entidade = request.POST['entidade']
                uf = request.POST['uf']

                user = User.objects.create_user(username=username, password=password, entidade=entidade, uf=uf)
                user.save()
                return render(request, 'registration/create_user.html')

    return render(request, 'registration/create_user.html')

@login_required
def table(request):
    # O código de conexão precisa ser alterado aqui.
    # Onde ele está pegando e salvando o arquivo
    path = os.path.join(settings.BASE_DIR, 'justificativas.xlsx')
    
    #permissão de leitura
    assert os.path.isfile(path)
    #lendo o arquivo
    df = pd.read_excel(path)

    #adicionando uma coluna id
    df['id'] = df.index

    if request.method == 'POST':

        id = request.POST['id']
        justificativa = request.POST['justificativa']
        data_justificativa = datetime.now()
        usuario = request.user.username
        arquivo = request.FILES.get('arquivo')

        if arquivo:
            folder = os.path.join('documentos', str(id))
            os.makedirs(folder, exist_ok=True)
            file_path = os.path.join(folder, arquivo.name)
            with open(file_path, 'wb+') as destination:
                for chunk in arquivo.chunks():
                    destination.write(chunk)

            arquivo = Arquivos(id_arquivo=id, arquivo=file_path, nome=arquivo.name)
            arquivo.save()

        df.loc[df['id'] == int(id), 'JUSTIFICATIVAS'] = justificativa
        df.loc[df['id'] == int(id), 'DATA_CARGA'] = data_justificativa
        df.loc[df['id'] == int(id), 'NOME'] = usuario

        df.to_excel(path, index=False)
        
        return redirect('table')

    if request.method == 'GET':

        if request.user.first_login:
            return redirect('change_password')

        groups = request.user.groups.all()
        #drop the columns Unnamed: 0
        df = df.drop(columns=['Unnamed: 0'])

        page = request.GET.get('page', 1)
        paginator = Paginator(df, 25)

        try:
            dataframe = paginator.page(page)
        except PageNotAnInteger:
            dataframe = paginator.page(1)
        except EmptyPage:
            dataframe = paginator.page(paginator.num_pages)

        return render(request, 'api_rest/table.html', {'data': df.to_dict('records'), 'files': Arquivos.objects.all(), 'groups': groups, 'page_obj': dataframe})