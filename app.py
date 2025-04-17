from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # Servidor web Flask

# Caminho correto do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tarefas.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # Inicializa a conexão com o banco de dados

# Definição do modelo da tabela de tarefas
# Cada tarefa tem um ID, conteúdo e status de concluída
class Tarefa(db.Model):
    __tablename__ = "tarefas"

    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(200), nullable=False)
    feita = db.Column(db.Boolean, default=False)


with app.app_context():
    db.create_all()
    db.session.commit()

# Página principal
@app.route('/')
def home():
    return render_template("index.html")

# Rota para criar tarefa
@app.route('/criar', methods=['POST'])
def criar():
    conteudo = request.form.get('conteudo_tarefa')
    if not conteudo:
        return 'Conteúdo inválido', 400

    nova_tarefa = Tarefa(conteudo=conteudo, feita=False)
    db.session.add(nova_tarefa)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
