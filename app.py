from flask import Flask, render_template, request,  redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "1234"  # Chave secreta para proteger sessões e cookies

# Corrigido: banco de dados na mesma pasta do app
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///C:/Users/Gebruiker/PycharmProjects/GestordeTarefas1/database/tarefas.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Tarefa(db.Model):
    __tablename__ = "tarefas"
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(200), nullable=False)
    feita = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()
    db.session.commit()

@app.route('/')
def home():
    todas_as_tarefas = Tarefa.query.all()
    return render_template("index.html", lista_de_tarefas=todas_as_tarefas)

@app.route('/criar-tarefa', methods=['POST'])
def criar():
    try:
        conteudo_tarefa = request.form['conteudo_tarefa']
    except KeyError:
        return "Erro: chave 'conteudo_tarefa' não encontrada no formulário.", 400

    tarefa = Tarefa(conteudo=conteudo_tarefa, feita=False)
    db.session.add(tarefa)
    db.session.commit()
    return redirect(url_for('home')) # Redireciona-nos à função home()
@app.route('/eliminar-tarefa/<id>')
def eliminar(id):
    tarefa = Tarefa.query.filter_by(id=int(id)).delete() # Pesquisa-se dentro da base de dados, aquele registro cujo id coincida com o proporcionado peloparâmetro da rota. Quando se encontrar elimina-se
    db.session.commit() # Executar a operação pendente da base de dados
    return redirect(url_for('home'))
@app.route('/tarefa-feita/<id>')
def tarefa_feita(id):
    tarefa = Tarefa.query.filter_by(id=int(id)).first()
    tarefa.feita = not(tarefa.feita)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
