# Parte web

## Setup

### Flask

1. Confira se python 3.7 - 3.9 está instalado com ```python --version```.
2. Crie um ambiente virtual, ou utilize algo como o [conda](https://docs.conda.io/en/latest/). 
    A seguir estão os passos para instalar um ambiente virtual sem o conda:
```bash
# cria um ambiente virtual na pasta .venv
python -m venv venv

# inicia o ambiente virtual
venv\Scripts\activate (windows)
source venv/Scripts/activate

# fecha o ambiente virtual
deactivate
```

3. No ambiente virtual, instale os requerimentos para o Flask com ```pip install -r flask/requirements.txt```

4. Exporte as variáveis de ambiente necessárias:
```bash
cd flask
set MYSQL_ORI=mysql://admin:agFYuFEeYrsvBjc4Nymf@dev.cjsnzeyi5n0a.us-east-1.rds.amazonaws.com:3306/dev
set FLASK_APP=run.py
set FLASK_ENV=production    (ou development)
set FLASK_DEBUG=0           (ou 1)
...
```

5. Para subir o flask:

```bash
# development
flask run

# production
python3 run_gunicorn.py


```