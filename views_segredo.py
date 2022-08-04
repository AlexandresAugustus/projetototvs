from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from segredo import app, db
from models import Segredo
from helpers import recupera_imagem, deleta_arquivo, Formulariosegredo
import time


@app.route('/')
def index():
    lista = Segredo.query.order_by(Segredo.id)
    return render_template('lista.html', titulo='Segredo', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = Formulariosegredo()
    return render_template('novo.html', titulo='SENHA', form=form)

@app.route('/criar', methods=['POST',])
def criar():
    form = Formulariosegredo(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data


    segredo = Segredo.query.filter_by(nome=nome).first()

    if segredo:
        flash('já existente!')
        return redirect(url_for('index'))

    novo_jogo = Segredo(nome=nome)
    db.session.add(novo_jogo)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{novo_jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    jogo = Segredo.query.filter_by(id=id).first()
    form = Formulariosegredo()
    form.nome.data = jogo.nome
    capa_jogo = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Mensagem', id=id, capa_jogo=capa_jogo, form=form)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = Formulariosegredo(request.form)

    if form.validate_on_submit():
        jogo = Segredo.query.filter_by(id=request.form['id']).first()
        jogo.nome = form.nome.data


        db.session.add(jogo)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(id)
        arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Segredo.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Deletado com sucesso!')

    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)