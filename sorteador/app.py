from flask import Flask, render_template, request, jsonify
from database import db, Nome, app
import random

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form.get('nome')
    if nome:
        novo_nome = Nome(nome=nome)
        db.session.add(novo_nome)
        db.session.commit()
        return jsonify({'mensagem': 'Nome adicionado!'})
    return jsonify({'erro': 'Nome inválido'}), 400

@app.route('/sortear', methods=['GET'])
def sortear():
    nome = Nome.query.filter_by(sorteado=False).order_by(db.func.random()).first()
    if nome:
        nome.sorteado = True
        db.session.commit()
        return jsonify({'nome': nome.nome})
    return jsonify({'mensagem': 'Todos os nomes já foram sorteados!'})

@app.route('/resetar', methods=['POST'])
def resetar():
    db.session.query(Nome).delete()  # Apaga todos os registros
    db.session.commit()
    return jsonify({'mensagem': 'Todos os nomes foram apagados!'})

@app.route('/listar', methods=['GET'])
def listar():
    nomes = Nome.query.filter_by(sorteado=False).all()  # Pega apenas os não sorteados
    nomes_lista = [nome.nome for nome in nomes]
    return jsonify(nomes_lista)


if __name__ == '__main__':
    app.run(debug=True)
