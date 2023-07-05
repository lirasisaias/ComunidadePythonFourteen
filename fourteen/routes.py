from flask import render_template, redirect, url_for, flash, request, abort
from fourteen import app, database, bcrypt
from fourteen.forms import FormLongin, FormCriarConta, FormEditarPerfil, FormCriarPost
from fourteen.models import Usuario, Post
from fourteen.auxiliares import salvar_imagem, atualizar_jogos
from sqlalchemy import create_engine
from flask_login import login_user, logout_user, current_user, login_required

engine = create_engine("mysql+pymysql://user:pw@host/db", pool_pre_ping=True)

@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('Home.html', posts=posts)

@app.route('/contato')
def contato():
    return render_template('Contato.html')

@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('Usuarios.html', lista_usuarios=lista_usuarios)

@app.route('/login', methods=['GET','POST'])
def login():
    form_login = FormLongin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no email: {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no login, E-mail ou Senha incorretos', 'alert-danger')

    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada com sucesso no email: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('Login.html', form_login=form_login, form_criarconta=form_criarconta)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout feito com sucesso','alert-success')
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('Perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar', methods=['GET','POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post criado com SUCESSO', 'alert-success')
        return redirect(url_for('home'))
    return render_template('Criar Post.html',form=form)

@app.route('/perfil/editar', methods=['GET','POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.jogos_fav = atualizar_jogos(form)
        database.session.commit()
        flash("Perfil atualizado com Sucesso", 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username

    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)

@app.route('/post/<post_id>', methods=['GET','POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post atualizado com Sucesso','alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('Post.html', post=post, form=form)

@app.route('/post/<post_id>/excluir', methods=['GET','POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Excluido com Sucesso', 'alert-warning')
        return redirect(url_for('home'))
    else:
        abort(403)
