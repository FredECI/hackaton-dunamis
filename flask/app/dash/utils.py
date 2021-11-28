from ..models import Usuario, Resposta
from .. import db


from typing import Dict, Union, List


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
        7
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
        u.nome: - (pior_pontuacao - u.pontos) for u in users
    }




