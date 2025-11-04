#!/usr/bin/env python3
"""Script de teste simples para o ProdutoDAO.

Uso:
  - Configure variáveis de ambiente PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE ou passe via args.
  - Execute: python scripts/test_produto.py

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

from dao.db import init_db, close_pool
from dao.produto_dao import ProdutoDAO


def parse_args():
    p = argparse.ArgumentParser(description="Testador do ProdutoDAO")
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

    dao = ProdutoDAO()

    try:
        print('\n== Lista inicial de produtos ==')
        produtos = dao.listar_produtos()
        print(produtos)

        test_id = int(time.time() % 100000) + 90000
        print(f"\n== Inserindo produto de teste id={test_id} ==")
        dao.inserir_produto(
            test_id,
            f'Produto Teste {test_id}',
            'Descrição de teste',
            99.99,
            42
        )

        print('\n== Após insert: listar ==')
        produtos = dao.listar_produtos()
        print(produtos)

        print(f"\n== Buscar produto id={test_id} ==")
        p = dao.buscar_produto(test_id)
        print(p)

        print(f"\n== Atualizar produto id={test_id} ==")
        dao.atualizar_produto(test_id, f'Produto Teste {test_id} Atualizado', 'Descrição atualizada', 123.45, 99)

        print(f"\n== Buscar após update id={test_id} ==")
        p = dao.buscar_produto(test_id)
        print(p)

        print(f"\n== Deletar produto id={test_id} ==")
        dao.deletar_produto(test_id)

        print('\n== Lista final de produtos ==')
        produtos = dao.listar_produtos()
        print(produtos)

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
