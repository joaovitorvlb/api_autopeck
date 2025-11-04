#!/usr/bin/env python3
"""Script de teste simples para o VendaDAO.

Uso:
  - Configure variáveis de ambiente PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE ou passe via args.
  - Execute: python scripts/test_venda.py

O script fará: listar, inserir, buscar, atualizar, deletar e listar novamente.

Observação: para inserir uma venda de teste usamos `id_cliente=1` e `id_funcionario=1` (já presentes no banco de exemplo). Ajuste se necessário.
"""
import argparse
import os
import sys
import time
from pathlib import Path

# Garante que o root do projeto esteja no sys.path quando executado diretamente
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dao.db import init_db, close_pool
from dao.venda_dao import VendaDAO


def parse_args():
    p = argparse.ArgumentParser(description="Testador do VendaDAO")
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

    dao = VendaDAO()

    try:
        print('\n== Lista inicial de vendas ==')
        vendas = dao.listar_vendas()
        print(vendas)

        # id de venda temporário (pouco provável de conflito)
        test_id = int(time.time() % 100000) + 90000
        print(f"\n== Inserindo venda de teste id={test_id} ==")
        # Usa cliente e funcionário existentes (1,1). Ajuste se necessário.
        dao.inserir_venda(test_id, 1, 1, '2025-10-27', 150.00)

        print('\n== Após insert: listar ==')
        vendas = dao.listar_vendas()
        print(vendas)

        print(f"\n== Buscar venda id={test_id} ==")
        v = dao.buscar_venda(test_id)
        print(v)

        print(f"\n== Atualizar venda id={test_id} ==")
        dao.atualizar_venda(test_id, 1, 1, '2025-10-27', 180.50)

        print(f"\n== Buscar após update id={test_id} ==")
        v = dao.buscar_venda(test_id)
        print(v)

        print(f"\n== Deletar venda id={test_id} ==")
        dao.deletar_venda(test_id)

        print('\n== Lista final de vendas ==')
        vendas = dao.listar_vendas()
        print(vendas)

        print('\nTeste concluído com sucesso (ou sem exceções levantadas).')

    except Exception:
        print('\nOcorreu um erro durante os testes:')
        import traceback
        traceback.print_exc()
    finally:
        print('\nFechando pool de conexões...')
        close_pool()


if __name__ == '__main__':
    main()


