from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Aluno(Base):
    __tablename__ = 'tbl_alunos'

    id = Column("pk_aluno", Integer, primary_key = True)
    matricula = Column(String(6), unique = True)
    nome = Column(String(100))
    cpf = Column(String(11))
    telefone = Column(String(11))
    endereco = Column(String(100))
    cidade = Column(String(30))
    cep = Column(String(8))
    unidade_escolar = Column(String(30))
    data_insercao = Column(DateTime, default = datetime.now())

    def __init__(self, matricula: str, nome: str, cpf: str, telefone: str, endereco: str,
                 cidade: str, unidade_escolar: str, cep: str, data_insercao:Union[DateTime, None] = None):
        """
        Cria um registro para um aluno com os seguintes argumentos:
            matricula: número da matrícula do aluno.
            nome: nome do aluno.
            cpf: cpf do aluno.
            telefone: telefone do aluno.
            endereco: endereco do aluno.
            cidade: cidade onde o aluno reside.
            cep: cep do endereço do aluno.
            unidade_escolar: unidade onde o aluno está/será matriculado.
            data_insercao: data na qual o aluno foi cadastrado.
        """
        self.matricula = matricula
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.endereco = endereco
        self.cidade = cidade
        self.cep = cep
        self.unidade_escolar = unidade_escolar
        
        # se não for informada, será a data do cadastro do aluno
        if data_insercao:
            self.data_insercao = data_insercao