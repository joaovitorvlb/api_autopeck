#!/usr/bin/env python3
"""Script de teste simples para o FuncionarioDAO.

Uso:
  - Configure variáveis de ambiente PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE ou passe via args.
  - Execute: python scripts/test_funcionario.py

O script fará: listar, inserir, buscar, atualizar, deletar e listar novamente.
"""
import argparse
import os
import sys
import time
from pathlib import Path

# Garantir que o root do projeto (pai de scripts/) esteja no sys.path quando
# o script for executado diretamente: python scripts/test_funcionario.py
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dao.db import init_db, close_pool
from dao.funcionario_dao import FuncionarioDAO


def parse_args():
    p = argparse.ArgumentParser(description="Testador do FuncionarioDAO")
    p.add_argument('--host', help='DB host')
    p.add_argument('--port', type=int, help='DB port')
    p.add_argument('--user', help='DB user')
    p.add_argument('--password', help='DB password')
    p.add_argument('--database', help='DB name')
    return p.parse_args()


def build_config_from_args(args):
    cfg = {}
    if args.host:
        cfg['host'] = args.host
    if args.port:
        cfg['port'] = args.port
    if args.user:
        cfg['user'] = args.user
    if args.password is not None:
        cfg['password'] = args.password
    if args.database:
        cfg['database'] = args.database
    return cfg or None


def main():
    args = parse_args()
    cfg = build_config_from_args(args)

    # Se cfg for None, init_db vai ler das variáveis de ambiente
    print('Inicializando pool de conexões...')
    init_db(db_config=cfg)

    dao = FuncionarioDAO()

    try:
        print('\n== Lista inicial de funcionários ==')
        funcionarios = dao.listar_funcionarios()
        print(funcionarios)

        # usar um id temporário pouco provável de conflito
        test_id = int(time.time() % 100000) + 90000
        print(f"\n== Inserindo funcionário de teste id={test_id} ==")
        dao.inserir_funcionario(
            test_id,
            f'Teste {test_id}',
            'Desenvolvedor',
            1234.56,
            '2025-10-26'
        )

        print('\n== Após insert: listar ==')
        funcionarios = dao.listar_funcionarios()
        print(funcionarios)

        print(f"\n== Buscar funcionário id={test_id} ==")
        f = dao.buscar_funcionario(test_id)
        print(f)

        print(f"\n== Atualizar funcionário id={test_id} ==")
        dao.atualizar_funcionario(test_id, f'Teste {test_id} Atualizado', 'Analista', 2345.67, '2025-10-26')

        print(f"\n== Buscar após update id={test_id} ==")
        f = dao.buscar_funcionario(test_id)
        print(f)

        print(f"\n== Deletar funcionário id={test_id} ==")
        dao.deletar_funcionario(test_id)

        print('\n== Lista final de funcionários ==')
        funcionarios = dao.listar_funcionarios()
        print(funcionarios)

        print('\nTeste concluído com sucesso (ou sem exceções levantadas).')

    except Exception as e:
        print('\nOcorreu um erro durante os testes:')
        import traceback
        traceback.print_exc()
    finally:
        print('\nFechando pool de conexões...')
        close_pool()


if __name__ == '__main__':
    main()
