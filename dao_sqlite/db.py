import os
import sqlite3
import threading
from contextlib import contextmanager

# Configuração global
_db_path = None
_db_lock = threading.Lock()


def init_db(db_config: dict = None, minconn: int = 1, maxconn: int = 5):
    """Inicializa o caminho do banco SQLite.
    
    db_config: dict com chave 'database' (caminho do arquivo SQLite).
      Exemplo: {'database': 'app_sqlite.db'}
    Se db_config for None, usa variável de ambiente SQLITE_DB ou padrão 'banco_api.sqlite'.
    
    Os parâmetros minconn e maxconn são ignorados (compatibilidade com interface PostgreSQL).
    """
    global _db_path
    if _db_path is not None:
        return
    
    if db_config is None:
        _db_path = os.getenv('SQLITE_DB', 'banco_api.sqlite')
    else:
        _db_path = db_config.get('database', 'banco_api.sqlite')


@contextmanager
def get_cursor(commit: bool = True):
    """Context manager que fornece um cursor SQLite e executa commit/rollback automaticamente.
    
    Uso:
      from dao_sqlite.db import get_cursor
      with get_cursor() as cur:
          cur.execute("SELECT ...")
          rows = cur.fetchall()
    
    O commit é executado automaticamente se nenhum erro for lançado.
    """
    if _db_path is None:
        raise RuntimeError("Database path não inicializado. Chame init_db(...) primeiro.")
    
    # Remover lock global para melhorar performance
    # SQLite lida com concorrência internamente
    conn = sqlite3.connect(_db_path, timeout=30.0)  # Timeout de 30 segundos
    conn.row_factory = sqlite3.Row
    
    # Configurações para melhor performance
    conn.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging
    conn.execute("PRAGMA synchronous=NORMAL")  # Sincronização mais rápida
    conn.execute("PRAGMA cache_size=10000")  # Cache maior
    conn.execute("PRAGMA temp_store=memory")  # Temporários em memória
    
    cur = conn.cursor()
    try:
        yield cur
        if commit:
            conn.commit()
    except Exception:
        try:
            conn.rollback()
        except Exception:
            pass
        raise
    finally:
        try:
            cur.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass


def close_pool():
    """Fecha o pool (compatibilidade com interface PostgreSQL).
    Para SQLite, apenas reseta o caminho do banco.
    """
    global _db_path
    _db_path = None

