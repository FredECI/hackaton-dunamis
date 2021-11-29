from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, logout_user, current_user

from . import auth
from ..models import Usuario, encode_md5
from .. import db
# from .forms import RegisterForm, LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form)
        if request.json:
            form = request.json
        else:
            form: dict = request.form
        email: str = form.get('inputF')
        senha: str = form.get('senhaF')
        senha_hash: str = encode_md5(senha)
        if email is not None and senha is not None:
            u = Usuario.query.filter_by(email=email, senha=senha_hash).first()
            if u is not None:
                login_user(u)
                return redirect(url_for('dash.dashboard'))

        flash("Credenciais incorretas", "danger")

    flash("Teste")
    return render_template("auth/login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        print(request.form)
        form: dict = request.form
        nome: str = form.get('nome')
        genero: str = form.get('genderPicker')
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
                u.hora_inicio = 9
                u.hora_fim = 17
                u.genero = genero

                db.session.add(u)
                db.session.commit()

                login_user(u)
                return redirect(url_for('home.pesquisa'))

    return render_template('auth/register.html')


@auth.route("/logout", methods=["GET"])
def logout():
    if current_user.is_authenticated:
        logout_user()

    return redirect(url_for("home.index"))