from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from fourteen.models import Usuario
from flask_login import current_user

class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(message="Digite um nome de usuário válido")])
    email = StringField('E-mail', validators=[DataRequired(), Email(message="Digite um endereço de e-mail válido")])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6,28, message="A senha tem que ter entre 6 a 20 caracteres")])
    confirmacao = PasswordField('Confirme sua senha', validators=[DataRequired(), EqualTo('senha', message="Senha diferente da preenchida anteriomente")])
    botao_submit_criarconta = SubmitField('Criar conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro email ou faça login para continuar.')


class FormLongin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email(message="Digite um endereço de e-mail válido")])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6,28, message="Digit um valor para a senha de 6 a 20 caracteres")])
    lembrar_dados = BooleanField('Lembre-se')
    botao_submit_login = SubmitField('Fazer login')

class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(message="Digite um nome de usuário válido")])
    email = StringField('E-mail', validators=[DataRequired(), Email(message="Digite um endereço de e-mail válido")])
    foto_perfil = FileField('Atualizar foto de perfil',validators=[FileAllowed(['jpg', 'png'])])
    j_souls = BooleanField('Jogos Souls')
    j_sobrevivência = BooleanField('Sobrevivência')
    j_fps = BooleanField('FPS')
    j_acao = BooleanField('Ação')
    j_2d = BooleanField('2D')
    j_online = BooleanField('Jogos on-line')
    j_fantasia = BooleanField('Fantasia')
    j_rpg = BooleanField('RPG')
    j_terror = BooleanField('Terror')
    j_estratégia = BooleanField('Estratégia')
    j_esporte = BooleanField('Esporte')
    j_corrida = BooleanField('Corrida')
    j_simulação = BooleanField('Simulação')
    j_sandbox = BooleanField('Sandbox')
    botao_submit_editarperfil = SubmitField('Confirmar Edição')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuario com esse e-mail, Cadastre outro e-mail')

class FormCriarPost(FlaskForm):
    titulo = StringField('Titulo do Post', validators=[DataRequired(), Length(2, 140)])
    corpo =  TextAreaField('Teixe sua menssagem aqui!!!', validators=[DataRequired()])
    botao_submit =SubmitField('Criar Post')