import os
from contextlib import contextmanager
from psycopg2 import pool

_pool = None


def init_db(db_config: dict = None, minconn: int = 1, maxconn: int = 5):
    """Inicializa o pool de conexões. Se db_config não for fornecido, lê das variáveis de ambiente:
    PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE

    db_config: dict com chaves compatíveis com psycopg2.connect, por exemplo:
      {
        'host': '127.0.0.1',
        'port': 5432,
        'user': 'postgres',
        'password': '123456',
        'database': 'e_comerce_flask'
      }
    """
    global _pool
    if _pool is not None:
        return

    if db_config is None:
        db_config = {
            'host': os.getenv('PGHOST', 'localhost'),
            'port': int(os.getenv('PGPORT', 5432)),
            'user': os.getenv('PGUSER', 'postgres'),
            'password': os.getenv('PGPASSWORD', '123456'),
            'database': os.getenv('PGDATABASE', 'e_comerce_flask'),
        }

    _pool = pool.SimpleConnectionPool(minconn, maxconn, **db_config)


@contextmanager
def get_cursor(commit: bool = True):
    """Context manager que fornece um cursor e devolve a conexão ao pool ao sair.

    Uso:
      from dao.db import get_cursor
      with get_cursor() as cur:
          cur.execute("SELECT ...")
          rows = cur.fetchall()

    O commit é executado automaticamente se nenhum erro for lançado.
    """
    if _pool is None:
        raise RuntimeError("Connection pool não inicializado. Chame init_db(...) primeiro.")

    conn = _pool.getconn()
    cur = conn.cursor()
    try:
        yield cur
        if commit:
            conn.commit()
    except Exception:
        # rollback on error and re-raise
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
        _pool.putconn(conn)


def close_pool():
    global _pool
    if _pool is not None:
        _pool.closeall()
        _pool = None
