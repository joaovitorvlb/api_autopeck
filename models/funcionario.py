from datetime import date
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass
class Funcionario:
    id_funcionario: int
    nome: str
    cargo: Optional[str] = None
    salario: Optional[Decimal] = None
    data_contratacao: Optional[date] = None

    @staticmethod
    def from_dict(data: dict) -> 'Funcionario':
        """
        Cria uma instância de Funcionário a partir de um dicionário
        """
        # Converte o salário para Decimal se existir
        if 'salario' in data and data['salario'] is not None:
            data['salario'] = Decimal(str(data['salario']))
        
        # Converte a data de contratação para date se existir
        if 'data_contratacao' in data and data['data_contratacao'] is not None:
            if isinstance(data['data_contratacao'], str):
                data['data_contratacao'] = date.fromisoformat(data['data_contratacao'])

        return Funcionario(
            id_funcionario=data['id_funcionario'],
            nome=data['nome'],
            cargo=data.get('cargo'),
            salario=data.get('salario'),
            data_contratacao=data.get('data_contratacao')
        )

    def to_dict(self) -> dict:
        """
        Converte a instância de Funcionário para um dicionário
        """
        return {
            'id_funcionario': self.id_funcionario,
            'nome': self.nome,
            'cargo': self.cargo,
            'salario': float(self.salario) if self.salario is not None else None,
            'data_contratacao': self.data_contratacao.isoformat() if self.data_contratacao is not None else None
        }