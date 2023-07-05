from fourteen import app
from PIL import Image
import secrets
import os
def salvar_imagem(imagem):
    #Colocando o codigo no nome do arquivo para garantiri que não ira se repetir
    cod = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_full = nome + cod + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_full)
    #reduzir o tamanho da imagem para nosso BD
    tamanho = (300, 300)
    imagem_red = Image.open(imagem)
    imagem_red.thumbnail(tamanho)
    #Salvarndo a imagem
    imagem_red.save(caminho_completo)
    return nome_full

def atualizar_jogos(form):
    lista_jogos = []
    for campo in form:
        if 'j_' in campo.name:
            if campo.data:
                lista_jogos.append(campo.label.text)
    return ';'.join(lista_jogos)