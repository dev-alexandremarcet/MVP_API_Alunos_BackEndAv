from flask_openapi3 import OpenAPI, Info, Tag
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from flask import redirect
from urllib.parse import unquote

from model import Session, Aluno
from schemas import *


info = Info(title = "API Secretaria Escolar - Cadastro de Alunos", version = "1.1.0")
app = OpenAPI(__name__, info = info)
CORS(app)


# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
aluno_tag = Tag(name="Secretaria Escolar - Cadastro de Alunos", description="Adição, visualização e remoção de alunos à base de dados")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/cadastra_aluno', tags=[aluno_tag],
          responses={"200": AlunoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def insere_aluno(form: AlunoSchema):
    """Cadastra um novo aluno à base de dados

    Retorna uma representação do aluno.
    """
    aluno = Aluno(
        matricula = form.matricula,
        nome = form.nome,
        cpf = form.cpf,
        telefone = form.telefone,
        endereco = form.endereco,
        cidade = form.cidade,
        cep = form.cep,
        unidade_escolar = form.unidade_escolar
        )

    try:
        # criando conexão com a base de dados
        session = Session()
        # adicionando um novo aluno à base de dados
        session.add(aluno)
        # efetivando o comando de adição de novo aluno na tabela
        session.commit()
        return exibe_aluno(aluno), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Aluno com a mesma matrícula existente na base de dados:/"
        return {"mensagem de erro de integridade": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível cadastrar um novo aluno :/"
        return {"mensagem de erro": error_msg}, 400

@app.put('/atualiza_aluno', tags=[aluno_tag],
            responses={"200": AlunoViewSchema, "400": ErrorSchema})
def atualiza_aluno(form: AtualizaAlunoSchema):
    """Atualiza um aluno existente na base de dados

    Retorna uma representação do aluno.
    """
    try:
        #aluno_num_matricula = form.num_matricula
        matricula_aluno = form.matricula
        # criando conexão com a base de dados
        session = Session()
        # fazendo a busca
        aluno = session.query(Aluno).filter(Aluno.matricula == matricula_aluno).first()
        if not aluno:
        # se o aluno não foi encontrado
            error_msg = "Aluno não encontrado na base de dados:/"
            return {"mensagem de erro": error_msg}, 404

        if form.nome:
            aluno.nome = form.nome

        if form.cpf:
            aluno.cpf = form.cpf

        if form.telefone:
            aluno.telefone = form.telefone

        if form.endereco:
            aluno.endereco = form.endereco

        if form.cidade:
            aluno.cidade = form.cidade

        if form.cep:
            aluno.cep = form.cep

        if form.unidade_escolar:
            aluno.unidade_escolar = form.unidade_escolar
            
        # adicionando um novo aluno à base de dados
        session.add(aluno)
        # efetivando o comando de adição de novo aluno na tabela
        session.commit()
        return exibe_aluno(aluno), 200

    except Exception as e:
    # caso um erro fora do previsto
        error_msg = "Não foi possível atualizar o aluno :/"
        return {"mensagem de erro": error_msg}, 400


@app.get('/listagem_alunos', tags=[aluno_tag],
         responses={"200": ListagemAlunosSchema, "404": ErrorSchema})
def busca_alunos():
    """Faz a busca por todos os alunos cadastrados na base de dados

    Retorna uma representação da listagem de alunos.
    """
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    alunos = session.query(Aluno).all()
    
    if not alunos:
        # se não há alunos cadastrados
        return {"alunos": []}, 200
    else:
        # retorna a representação da listagem de alunos
        return exibe_alunos(alunos), 200


@app.get('/busca_aluno', tags=[aluno_tag],
         responses={"200": AlunoViewSchema, "404": ErrorSchema})
def busca_aluno(query: BuscaAlunoSchema):
    """Faz a busca por um aluno a partir do número de matrícula do aluno.

    Retorna uma representação do aluno.
    """
    #aluno_num_matricula = query.num_matricula
    matricula_aluno = query.matricula
    # criando conexão com a base de dados
    session = Session()
    # fazendo a busca
    aluno = session.query(Aluno).filter(Aluno.matricula == matricula_aluno).first()
    
    if not aluno:
        # se o aluno não foi encontrado
        error_msg = "Aluno não encontrado na base de dados:/"
        return {"mensagem de erro": error_msg}, 404
    else:
        # retorna a representação de aluno
        return exibe_aluno(aluno), 200


@app.delete('/remove_aluno', tags=[aluno_tag],
            responses={"200": RemoveAlunoSchema, "404": ErrorSchema})
def remove_aluno(query: BuscaAlunoSchema):
    """Remove um aluno a partir do número de matrícula informado

    Retorna uma mensagem de confirmação da remoção do aluno.
    """
    
    #aluno_num_matricula = query.num_matricula
    matricula_aluno = query.matricula
    # criando conexão com a base de dados
    session = Session()
    # fazendo a remoção do aluno da base de dados
    contador = session.query(Aluno).filter(Aluno.matricula == matricula_aluno).delete()
    session.commit()
    
    if contador:
        # se o aluno foi removido da base de dados
        return {"mensagem": "Aluno removido", "Número de matrícula": matricula_aluno}
    else:
        # se o aluno não foi encontrado na base de dados
        error_msg = "Aluno não encontrado na base de dados:/"
        return {"mensagem": error_msg}, 404
