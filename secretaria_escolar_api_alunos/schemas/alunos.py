from pydantic import BaseModel
from typing import Optional, List
from model.alunos import Aluno



class AlunoSchema(BaseModel):
    """ Define como deve ser representado um aluno que será cadastrado.
    """
    matricula: str = "ALU001"
    nome: str = "João Pedro"
    cpf: str = "12345678900"
    telefone: str = "21999999999"
    endereco: str = "Av Pres Vargas, 42 - Centro"
    cidade: str = "Cordeiro"
    cep: str = "28540000"
    unidade_escolar: str = "Cordeiro"
    
    
class AtualizaAlunoSchema(BaseModel):
    """ Define como deve ser representado um aluno que será atualizado/alterado.
    """
    matricula: str = "ALU001"
    nome: str = "João Pedro"
    cpf: str = "12345678900"
    telefone: str = "21999999999"
    endereco: str = "Av Pres Vargas, 42 - Centro"
    cidade: str = "Cordeiro"
    cep: str = "28540000"
    unidade_escolar: str = "Cordeiro"
    

class BuscaAlunoSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca, que será
        feita apenas com base no número de matrícula do aluno.
    """
    matricula: str = "ALU001"


class ListagemAlunosSchema(BaseModel):
    """ Define como uma listagem de alunos cadastrados será retornada.
    """
    list_alunos:List[AlunoSchema]


def exibe_alunos(alunos: List[Aluno]):
    """ Retorna uma representação da listagem de alunos cadastrados seguindo o schema definido em
        AlunoViewSchema.
    """
    result = []
    for aluno in alunos:
        result.append({
            "matricula": aluno.matricula,
            "nome": aluno.nome,
            "cpf": aluno.cpf,
            "telefone": aluno.telefone,
            "endereco": aluno.endereco,
            "cidade": aluno.cidade,
            "cep": aluno.cep,
            "unidade_escolar": aluno.unidade_escolar
        })

    return {"alunos": result}


class AlunoViewSchema(BaseModel):
    """ Define como um aluno cadastrado será retornado.
    """
    id: int = 1
    matricula: str = "ALU001"
    nome: str = "João Pedro"
    cpf: str = "12345678900"
    telefone: str = "21999999999"
    endereco: str = "Av Pres Vargas, 42 - Centro"
    cidade: str = "Cordeiro"
    cep: str = "28540000"
    unidade_escolar: str = "Cordeiro"
    


class RemoveAlunoSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção de um aluno.
    """
    mensagem_remove_aluno: str
    nome_remove_aluno: str


def exibe_aluno(aluno: Aluno):
    """ Retorna uma representação do aluno seguindo o schema definido em
        AlunoViewSchema.
    """
    return {
        "matricula": aluno.matricula,
        "nome": aluno.nome,
        "cpf": aluno.cpf,
        "telefone": aluno.telefone,
        "endereco": aluno.endereco,
        "cidade": aluno.cidade,
        "cep": aluno.cep,
        "unidade_escolar": aluno.unidade_escolar
    }
