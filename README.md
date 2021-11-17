# Projeto


## Setup

### Flask (sem docker)

1. Confira se python 3.9 está instalado com ```python --version```.
2. Crie um ambiente virtual, ou utilize algo como o [conda](https://docs.conda.io/en/latest/). 
    A seguir estão os passos para instalar um ambiente virtual sem o conda:
```bash
# cria um ambiente virtual na pasta .venv
python -m venv venv

# inicia o ambiente virtual
venv\Scripts\activate (windows)

# fecha o ambiente virtual
deactivate
```

3. No ambiente virtual, instale os requerimentos para o Flask com ```pip install -r flask-app/requirements.txt```

4. Exporte as variáveis de ambiente necessárias:
```bash
set XXXX=XXXXX
...
```

5. Execute ```flask run``` para iniciar o flask.