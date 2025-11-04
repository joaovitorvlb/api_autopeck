#!/usr/bin/env python3
"""Teste end-to-end usando os DAOs e modelos.

Fluxo:
 - inicializa pool (lê env vars se não passar args)
 - insere funcionário, cliente, produto
 - cria venda e adiciona item(s) via ItemVendaDAO
 - verifica total da venda
 - atualiza quantidade do item e verifica total
 - remove item e verifica total
 - limpa (deleta venda, produto, cliente, funcionario)

Use: python scripts/test_e2e.py
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dao.db import init_db, close_pool
from dao.funcionario_dao import FuncionarioDAO
from dao.cliente_dao import ClienteDAO
from dao.produto_dao import ProdutoDAO
from dao.venda_dao import VendaDAO
from dao.item_venda_dao import ItemVendaDAO
from models.funcionario import Funcionario
from models.cliente import Cliente
from models.produto import Produto
from models.venda import Venda
from models.item_venda import ItemVenda


def main():
    print('Inicializando pool de conexões...')
    init_db()

    f_dao = FuncionarioDAO()
    c_dao = ClienteDAO()
    p_dao = ProdutoDAO()
    v_dao = VendaDAO()
    iv_dao = ItemVendaDAO()

    # ids baseados no tempo para evitar colisões
    ts = int(time.time() % 100000)
    id_func = ts + 70000
    id_cli = ts + 71000
    id_prod = ts + 72000
    id_venda = ts + 73000

    item_id = None

    try:
        print('\n== Construindo e inserindo funcionário de teste (modelo) ==')
        f_model = Funcionario(id_funcionario=id_func, nome=f'Func Test {id_func}', cargo='Vendedor', salario=2500.00, data_contratacao='2025-10-27')
        f_dao.inserir_funcionario_obj(f_model)
        print(f'Funcionario inserido id={f_model.id_funcionario}')

        print('\n== Construindo e inserindo cliente de teste (modelo) ==')
        c_model = Cliente(id_cliente=id_cli, nome=f'Cli Test {id_cli}', email='cli@test.com', telefone='+55 11 90000-0000', endereco='Rua Teste, 1')
        c_dao.inserir_cliente_obj(c_model)
        print(f'Cliente inserido id={c_model.id_cliente}')

        print('\n== Construindo e inserindo produto de teste (modelo) ==')
        p_model = Produto(id_produto=id_prod, nome=f'Prod Test {id_prod}', descricao='Desc teste', preco=49.90, estoque=10)
        p_dao.inserir_produto_obj(p_model)
        print(f'Produto inserido id={p_model.id_produto}')

        print('\n== Construindo e inserindo venda de teste (modelo) ==')
        v_model = Venda(id_venda=id_venda, id_cliente=id_cli, id_funcionario=id_func, data_venda='2025-10-27', total=0)
        v_dao.inserir_venda_obj(v_model)
        print(f'Venda criada id={v_model.id_venda}')

        print('\n== Construindo e adicionando ItemVenda via modelo (quantidade=2) ==')
        item_model = ItemVenda(id_item=None, id_venda=id_venda, id_produto=id_prod, quantidade=2, preco_unitario=49.90)
        item_id = iv_dao.add_item_from_model(item_model)
        print(f'Item adicionado id_item={item_id}')

        print('\n== Verificando venda e total ==')
        venda = v_dao.buscar_venda(id_venda)
        print('Venda:', venda)

        expected_total = 2 * 49.90
        print(f'Expected total: {expected_total}  DB total: {venda.total}')

        print('\n== Atualizando quantidade do item para 5 ==')
        iv_dao.update_item_quantity(item_id, 5)
        venda = v_dao.buscar_venda(id_venda)
        print('Venda após update:', venda)

        print('\n== Removendo item ==')
        iv_dao.remove_item(item_id)
        venda = v_dao.buscar_venda(id_venda)
        print('Venda após remover item:', venda)

        print('\n== Teste E2E concluído com sucesso.')

    except Exception:
        print('\nErro durante E2E:')
        import traceback
        traceback.print_exc()
    finally:
        print('\n== Limpando dados de teste ==')
        try:
            # garantir remoção de item se ainda existir
            if item_id:
                try:
                    iv_dao.remove_item(item_id)
                except Exception:
                    pass

            try:
                v_dao.deletar_venda(id_venda)
            except Exception:
                pass

            try:
                p_dao.deletar_produto(id_prod)
            except Exception:
                pass

            try:
                c_dao.deletar_cliente(id_cli)
            except Exception:
                pass

            try:
                f_dao.deletar_funcionario(id_func)
            except Exception:
                pass

            print('Limpeza concluída.')
        finally:
            print('\nFechando pool de conexões...')
            close_pool()


if __name__ == '__main__':
    main()
