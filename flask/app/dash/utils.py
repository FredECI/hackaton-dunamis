from ..models import Usuario, Pergunta, Resposta
from .. import db


from typing import Dict, Union, List


def get_problemas(token_ou_object: Union[Usuario, str]):
    """
    Esses são os problemas relativos ao banco de perguntas a seguir:

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

    doencas = []

    if isinstance(token_ou_object, Usuario):
        token = token_ou_object.token
    else:
        token = token_ou_object

    respostas: List[Resposta] = Resposta.query.filter_by(token_pessoa=token).all()
    respostas_id_set:set = {x.id_pergunta for x in respostas}

    # analisando CAGE
    if 1 in respostas_id_set and len(respostas_id_set.intersection({2, 3, 4, 5})) > 2:
        doencas.append("Alcoolismo preocupante, CAGE positivo")





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




