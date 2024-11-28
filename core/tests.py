from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Colecao 

class ColecaoTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')  
    
    def test_criar_colecao_associada_usuario(self):
        url = '/colecoes/'  
        data = {
            'nome': 'Coleção Teste',
            'descricao': 'Descrição da Coleção',
        }

        response = self.client.post(url, data, format='json')

        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        colecao = Colecao.objects.get(id=response.data['id'])
        self.assertEqual(colecao.usuario.id, self.user.id)

    def test_editar_colecao_usuario_autenticado(self):
        colecao = Colecao.objects.create(nome='Coleção Teste', usuario=self.user)
        url = f'/colecoes/{colecao.id}/'  
        data = {
            'nome': 'Coleção Teste Atualizada',
        }

        
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        colecao.refresh_from_db()
        self.assertEqual(colecao.nome, 'Coleção Teste Atualizada')

    def test_editar_colecao_usuario_nao_autenticado(self):
        colecao = Colecao.objects.create(nome='Coleção Teste', usuario=self.user)
        self.client.logout()  # Deslogar o usuário
        url = f'/colecoes/{colecao.id}/'
        data = {
            'nome': 'Coleção Teste Atualizada',
        }

        # Tentar editar sem estar autenticado
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_deletar_colecao_usuario_autenticado(self):
        colecao = Colecao.objects.create(nome='Coleção Teste', usuario=self.user)
        url = f'/colecoes/{colecao.id}/'

        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Colecao.DoesNotExist):
            Colecao.objects.get(id=colecao.id)

    def test_deletar_colecao_usuario_nao_autenticado(self):
        colecao = Colecao.objects.create(nome='Coleção Teste', usuario=self.user)
        self.client.logout()  
        url = f'/colecoes/{colecao.id}/'

        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_deletar_colecao_outro_usuario(self):
        outro_usuario = User.objects.create_user(username='outro_usuario', password='password')
        colecao = Colecao.objects.create(nome='Coleção Teste', usuario=self.user)
        self.client.login(username='outro_usuario', password='password')
        url = f'/colecoes/{colecao.id}/'

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_listar_colecoes_usuario_autenticado(self):
        colecao1 = Colecao.objects.create(nome='Coleção Teste 1', usuario=self.user)
        colecao2 = Colecao.objects.create(nome='Coleção Teste 2', usuario=self.user)
        url = '/colecoes/' 
        response = self.client.get(url)

        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  
        colecoes_nomes = [colecao['nome'] for colecao in response.data]
        self.assertIn(colecao1.nome, colecoes_nomes)
        self.assertIn(colecao2.nome, colecoes_nomes)

    def test_listar_colecoes_usuario_nao_autenticado(self):
        colecao = Colecao.objects.create(nome='Coleção Teste', usuario=self.user)
        self.client.logout()  
        url = '/colecoes/'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

