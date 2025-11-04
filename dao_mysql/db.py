import os
from contextlib import contextmanager
import mysql.connector
from mysql.connector import pooling

_pool = None


def init_db(db_config: dict = None, minconn: int = 1, maxconn: int = 5):
    """Inicializa o pool de conexões MySQL. Se db_config não for fornecido, lê das variáveis de ambiente:
    MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

    db_config: dict com chaves compatíveis com mysql.connector.connect, por exemplo:
      {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '123456',
        'database': 'e_comerce_flask'
      }
    """
    global _pool
    if _pool is not None:
        return

    if db_config is None:
        db_config = {
            'host': os.getenv('MYSQL_HOST', 'localhost'),
            'port': int(os.getenv('MYSQL_PORT', 3306)),
            'user': os.getenv('MYSQL_USER', 'root'),
            'password': os.getenv('MYSQL_PASSWORD', '123456'),
            'database': os.getenv('MYSQL_DATABASE', 'e_comerce_flask'),
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
            'autocommit': False
        }

    _pool = pooling.MySQLConnectionPool(
        pool_name="mysql_pool",
        pool_size=maxconn,
        pool_reset_session=True,
        **db_config
    )


@contextmanager
def get_cursor(commit: bool = True):
    """Context manager que fornece um cursor MySQL e devolve a conexão ao pool ao sair.

    Uso:
      from dao_mysql.db import get_cursor
      with get_cursor() as cur:
          cur.execute("SELECT ...")
          rows = cur.fetchall()

    O commit é executado automaticamente se nenhum erro for lançado.
    """
    if _pool is None:
        raise RuntimeError("Connection pool não inicializado. Chame init_db(...) primeiro.")

    conn = _pool.get_connection()
    cur = conn.cursor(dictionary=True)  # Retorna resultados como dicionários
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
        try:
            conn.close()
        except Exception:
            pass


def close_pool():
    """Fecha o pool de conexões"""
    global _pool
    if _pool is not None:
        _pool._remove_connections()
        _pool = None