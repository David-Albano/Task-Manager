from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # Na app encontra-se o nosso servidor web de Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/tarefas.db'
db = SQLAlchemy(app) # Cursor para a base de dados SQLite

class Tarefa(db.Model):
    __tablename__ = "tarefas"
    id = db.Column(db.Integer, primary_key=True)
    conteúdo = db.Column(db.String(200))
    feita = db.Column(db.Boolean)

with app.app_context():
    db.create_all()
    db.session.commit()

@app.route('/')
def home():
    todas_as_tarefas = Tarefa.query.all()# Consultamos e armazenamos todas as tarefas da base de dados
# Agora na variável todas_as_tarefas estão armazenadas todas as tarefas. Vamos entregar esta variável ao template index.html
    return render_template("index.html", lista_de_tarefas=todas_as_tarefas)
    # Carrega-se o template index.html

@app.route('/criar-tarefa', methods=['POST'])
def criar():
    tarefa = Tarefa(conteúdo=request.form["conteúdo_tarefa"], feita=False)
    # id não é necessário atribuí-lo manualmente, porque a primary key gera-se automaticamente

    db.session.add(tarefa)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/eliminar-tarefa/<id>')
def eliminar(id):
    tarefa = Tarefa.query.filter_by(id=int(id)).delete() # Pesquisa-se dentro da base de dados, aquele registro cujo id coincida com o proporcionado pelo parâmetro da rota. Quando se encontrar elimina-se
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/tarefa-feita/<id>')
def feita(id):
    tarefa = Tarefa.query.filter_by(id=int(id)).first()
    tarefa.feita = not(tarefa.feita)  # Guardar na variável booleana da tarefa, o seu contrário
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)