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
    Nome.query.update({'sorteado': False})
    db.session.commit()
    return jsonify({'mensagem': 'Sorteio reiniciado!'})

if __name__ == '__main__':
    app.run(debug=True)
