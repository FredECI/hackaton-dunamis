from .models import Usuario, Resposta
from . import db
from os import path
from json import load
from random import choice

from typing import Dict, Union, List

PATH_MENSAGEM = path.join(path.dirname(__file__), 'mensagem.json')
PATH_FRASES = path.join(path.dirname(__file__), 'frases.json')


def get_mensagens():
    with open(PATH_MENSAGEM, 'r', encoding='utf-8') as f:
        lista = load(f)
    return choice(lista)


def get_frases(user: Usuario):
    r = get_doencas(user)
    maior = max(r.keys(), key=lambda x: r[x])

    with open(PATH_FRASES, 'r', encoding='utf-8') as f:
        dict_frases = load(f)

    if maior in dict_frases:
        return choice(dict_frases[maior])
    else:
        return get_mensagens()


def get_doencas(user=None) -> Dict:
    res = {
        # "Alcoolismo": 0,
        "Cancer de Mama": 0,
        "Obesidade": 0,
        "Cardiaco": 0,
        "Hipertensão": 0,
        "Diabetes": 0,
        "Cancer de Pulmão": 0,
    }

    if user is None:
        lista: List[Resposta] = Resposta.query.all()
    else:
        lista: List[Resposta] = Resposta.query.filter_by(token_pessoa=user.token).all()

    for r in lista:
        x = int(r.id_pergunta)
        if x == 1 or x == 3 or x == 5:
            pass
            # res["Alcoolismo"] += 1

        elif x == 9:
            res["Cancer de Mama"] += 1

        elif x == 10 or x == 11:
            res["Obesidade"] += 1

        elif r.id_pergunta == 20:
            res["Cardiaco"] += 1
            res["Obesidade"] += 1
            res["Hipertensão"] += 1
            res["Diabetes"] += 1

        elif r.id_pergunta == 21:
            res["Cancer de Pulmão"] += 1

    return res


def get_status(token_ou_object: Union[Usuario, str]):
    """
    Esses são os problemas ou vantagens relativos ao banco de perguntas a seguir:

    1,  Você consome bebida alcóolica?,                                             alcoolismo
    2,  Alguma vez o(a) senhor(a) sentiu que deveria diminuir ou parar de beber?,   alcoolismo
    3,  As pessoas o aborrecem porque criticam seu modo de beber?,                  alcoolismo
    4,  O(A) senhor(a) se sente culpado pela maneira como costuma beber?,           alcoolismo
    5,  O(A) senhor(a) costuma beber pela manhã para diminuir o nervosismo e a ressaca?,alcoolismo
    6,  O seu sexo biológico é masculino?,                                          gender
    7,  A senhora já teve filhos?,                                                  filho
    8,  A senhor amamentou o(s) seu(s) filho(s) até os seis meses?,                 filho
    9,  Você toma bebida alcólica mais que 4 vezes na semana?,                      Xalcoolismo
    10, "O seu <a href=""https://www.tuasaude.com/calculadora/imc/"" target=""_blank"">IMC</a> está acima de 30?",  imc
    11, "O seu <a href=""https://www.tuasaude.com/calculadora/imc/"" target=""_blank"">IMC</a> está acima de 25?",  imc
    20, Você faz atividade física mais que 6h semanais?,    fisica
    21, Você é fumante?,                                    fumo
    22, Você possui uma alimentação balancedada?,           alimento
    23, Você tem alguma doença crônica ou comorbidade?,     cronica
    """

    res = []

    if isinstance(token_ou_object, Usuario):
        token = token_ou_object.token
        genero = token_ou_object.genero
    else:
        user: Usuario = Usuario.query.filter_by(token=token_ou_object).first()
        if user is None:
            return []
        token = token_ou_object
        genero = user.genero

    respostas: List[Resposta] = Resposta.query.filter_by(token_pessoa=token).all()
    respostas_id_set: set = {x.id_pergunta for x in respostas}

    # analisando CAGE
    CAGE = False
    if 1 in respostas_id_set and len(respostas_id_set.intersection({2, 3, 4, 5})) > 2:
        CAGE = True
        res.append("Alcoolismo preocupante, CAGE positivo")

    # analisando feminino
    if genero == 'f':
        if {7, 8} in respostas_id_set:
            res.append('-7% no risco de cancer de mama')

        if CAGE or 9 in respostas_id_set:
            res.append("RR de 1.4 para cancer de mama")

        if 20 not in respostas_id_set:
            res.append("Sedentarismo: Fator de risco para doenças do sist. Circulatório, obesidade, hipertensão, diabates...")

    if 11 in respostas_id_set:
        res.append("Risco de doença crônica ou comorbidade")
    elif 10 in respostas_id_set:
        res.append("Grande risco de doença crônica ou comorbidade")

    if 23 in respostas_id_set:
        res.append("Maior risco para desenvolver outra doença crônica ou comorbidade")

    if 21 in respostas_id_set:
        res.append("Maior risco para cancer de pulmão, doença de sistema circulatório...")

    if 22 not in respostas_id_set:
        res.append("Maior risco para DCNT")

    return res


def get_scoreboard() -> Dict[str, int]:
    users = db.session.query(
        Usuario.nome,
        Usuario.pontos
    ).order_by(
        Usuario.pontos.desc()
    ).limit(
        5
    ).all()

    pior: Usuario = db.session.query(
        Usuario.pontos
    ).order_by(
        Usuario.pontos.asc()
    ).first()

    if pior is None:
        pior_pontuacao = -500
    else:
        pior_pontuacao = pior.pontos

    return {
        str(u.nome).capitalize(): - (pior_pontuacao - u.pontos) for u in users
    }


def get_empregados() -> int:
    return Usuario.query.filter_by(gestor=0).count()


def get_gestores() -> int:
    return Usuario.query.filter_by(gestor=1).count()




