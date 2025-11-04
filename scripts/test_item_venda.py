#!/usr/bin/env python3
"""Script de teste para ItemVendaDAO.

Fluxo do teste:
 - inicializa pool
 - cria uma venda de teste (usando VendaDAO)
 - adiciona item(s) à venda via ItemVendaDAO
 - atualiza quantidade
 - remove item
 - deleta venda de teste

Observação: usa Cliente=1, Funcionario=1 e Produto=1 (existentes no DB de exemplo). Ajuste se necessário.
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dao.db import init_db, close_pool
from dao.venda_dao import VendaDAO
from dao.item_venda_dao import ItemVendaDAO


def main():
    # lê configuração via env ou usa default
    print('Inicializando pool de conexões...')
    init_db()

    venda_dao = VendaDAO()
    item_dao = ItemVendaDAO()

    try:
        print('\n== Criando venda de teste ==')
        test_venda_id = int(time.time() % 100000) + 91000
        venda_dao.inserir_venda(test_venda_id, 1, 1, '2025-10-27', 0)
        print(f'Venda criada id={test_venda_id}')

        print('\n== Lista inicial de items (deve estar vazia) ==')
        items = item_dao.listar_items_por_venda(test_venda_id)
        print(items)

        print('\n== Adicionando item à venda ==')
        id_item = item_dao.add_item_to_venda(test_venda_id, 1, 2, 29.90)
        print(f'item adicionado id_item={id_item}')

        print('\n== Lista após insert ==')
        items = item_dao.listar_items_por_venda(test_venda_id)
        print(items)

        print('\n== Atualizando quantidade do item ==')
        item_dao.update_item_quantity(id_item, 5)
        print('quantidade atualizada para 5')

        print('\n== Item após update ==')
        item = item_dao.buscar_item(id_item)
        print(item)

        print('\n== Removendo item ==')
        item_dao.remove_item(id_item)
        print('item removido')

        print('\n== Lista final de items ==')
        items = item_dao.listar_items_por_venda(test_venda_id)
        print(items)

        print('\n== Deletando venda de teste ==')
        venda_dao.deletar_venda(test_venda_id)
        print('venda deletada')

        print('\nTeste de ItemVenda concluído com sucesso.')

    except Exception as e:
        print('\nErro durante teste:')
        import traceback
        traceback.print_exc()
    finally:
        print('\nFechando pool...')
        close_pool()


if __name__ == '__main__':
    main()
