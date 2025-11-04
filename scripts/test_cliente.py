#!/usr/bin/env python3
"""Script de teste simples para o ClienteDAO.

Uso:
  - Configure variáveis de ambiente PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE ou passe via args.
  - Execute: python scripts/test_cliente.py

O script fará: listar, inserir, buscar, atualizar, deletar e listar novamente.
"""
import argparse
import os
import sys
import time
from pathlib import Path

# Garante que o root do projeto esteja no sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dao_sqlite.db import init_db, close_pool
from dao_sqlite.cliente_dao import ClienteDAO


def parse_args():
    p = argparse.ArgumentParser(description="Testador do ClienteDAO")
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

    print('Inicializando pool de conexões...')
    init_db(db_config=cfg)

    dao = ClienteDAO()

    try:
        print('\n== Lista inicial de clientes ==')
        clientes = dao.listar_clientes()
        print(clientes)

        test_id = int(time.time() % 100000) + 90000
        print(f"\n== Inserindo cliente de teste id={test_id} ==")
        dao.inserir_cliente(
            test_id,
            f'Teste {test_id}',
            'teste@example.com',
            '+55 99 99999-9999',
            'Rua Teste, 123, Testelandia'
        )

        print('\n== Após insert: listar ==')
        clientes = dao.listar_clientes()
        print(clientes)

        print(f"\n== Buscar cliente id={test_id} ==")
        c = dao.buscar_cliente(test_id)
        print(c)

        print(f"\n== Atualizar cliente id={test_id} ==")
        dao.atualizar_cliente(test_id, f'Teste {test_id} Atualizado', 'atualizado@example.com', '+55 99 98888-8888', 'Rua Nova, 456, Testelandia')

        print(f"\n== Buscar após update id={test_id} ==")
        c = dao.buscar_cliente(test_id)
        print(c)

        print(f"\n== Deletar cliente id={test_id} ==")
        dao.deletar_cliente(test_id)

        print('\n== Lista final de clientes ==')
        clientes = dao.listar_clientes()
        print(clientes)

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
