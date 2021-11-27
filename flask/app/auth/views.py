from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user

from . import auth
from ..models import Usuario, encode_md5
from .. import db
# from .forms import RegisterForm, LoginForm


@auth.route('/teste', methods=['GET', 'POST'])
def teste():
    usuario = request.args.get('usuario')
    return jsonify({"usuario": usuario})


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.json:
            form = request.json
        else:
            form: dict = request.form
        email: str = form.get('email')
        senha: str = form.get('senha')
        senha_hash: str = encode_md5(senha)
        if email is not None and senha is not None:
            u = Usuario.query.filter_by(email=email, senha=senha_hash).first()
            if u is not None:
                login_user(u)
                return redirect(url_for('home.dashboard'))

        flash("Credenciais incorretas", "danger")

    return render_template("auth/login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        form: dict = request.form
        nome: str = form.get('nome')
        email: str = form.get('email')
        senha: str = form.get('senha')
        if nome is not None and email is not None and senha is not None:
            # validando se o email ja existe
            if Usuario.query.filter_by(email=email).first() is not None:
                flash("Email já cadastrado.")
            else:
                u = Usuario()
                u.email = email
                u.nome = nome
                u.senha = encode_md5(senha)
                u.admin = 0
                u.gestor = 0
                u.tempo = 5

                db.session.add(u)
                db.session.commit()

                login_user(u)

    return render_template('auth/register.html')
