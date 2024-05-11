from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired
import pandas as pd
from werkzeug.utils import secure_filename
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUA_SENHA_SUPER_SECRETA'  

# Armazenamento em memória
datasets = {}

# Dicionário de recomendações
recomendações = {
    'Electronics': ["Apple Iphone 15", "Samsung Smart TV 8K", "Sony", "LG", "Dell"],
    'Clothing': ["Nike T-shirt", "Adidas Tênis", "Zara", "H&M", "Uniqlo"],
    'Books': ["Amazon Kindle", "Barnes & Noble Nook", "Kobo", "Apple Books"],
    'Gardening': ["Home Depot", "Lowe's", "Walmart Garden Center", "Amazon Plants"],
    'Food': ["Whole Foods Market", "Trader Joe's", "Instacart", "Uber Eats"]
}

# Formulário
class NomeUsuarioForm(FlaskForm):
    nome_usuario = StringField("Nome do Usuário:", validators=[DataRequired()])
    dataset = FileField("Upload Dataset")
    submit = SubmitField("Gerar Recomendações")

# Rota da página inicial
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NomeUsuarioForm()
    if form.validate_on_submit():
        nome_usuario = form.nome_usuario.data
        file = form.dataset.data
        filename = secure_filename(file.filename)
        df = pd.read_csv(io.StringIO(file.read().decode('UTF8')), sep=',')
        datasets[filename] = df
        return redirect(url_for('recomendar', nome_usuario=nome_usuario))
    return render_template('index.html', form=form)

# Rota para recomendações
@app.route('/recomendar/<nome_usuario>')
def recomendar(nome_usuario):
    try:
        df = next(iter(datasets.values()))  # Use o primeiro dataset carregado
        categoria_usuario = df.loc[df['nome_usuario'].str.lower() == nome_usuario.lower(), 'categoria_produto'].iloc[0]
        lista_recomendacoes = recomendações[categoria_usuario]
        return jsonify({'recomendacoes': lista_recomendacoes, 'categoria': categoria_usuario})
    except IndexError:
        return jsonify({'erro': f'Usuário {nome_usuario} não encontrado.'})

if __name__ == '__main__':
    app.run(debug=True)
