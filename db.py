# db.py
import os
import logging
import sqlite3
from flask import g  # <-- add import

logger = logging.getLogger(__name__)

try:
    import psycopg2  # type: ignore
    HAS_PSYCOPG2 = True
except Exception:
    HAS_PSYCOPG2 = False


def _get_db_url() -> str:
    """
    Возвращает URL базы. По умолчанию — локальный SQLite файл.
    Примеры:
      - postgres://user:pass@host:port/dbname
      - postgresql://user:pass@host:port/dbname
      - sqlite:///app.db
    """
    return os.getenv("DATABASE_URL", "sqlite:///app.db")


def _connect():
    """
    Возвращает (conn, backend), где backend in {"postgres", "sqlite"}.
    """
    url = _get_db_url()
    url_lower = url.lower()

    if url_lower.startswith("postgres://") or url_lower.startswith("postgresql://"):
        if not HAS_PSYCOPG2:
            raise RuntimeError(
                "Для подключения к Postgres требуется пакет psycopg2, который не установлен. "
                "Либо установите psycopg2, либо используйте DATABASE_URL вида sqlite:///app.db"
            )
        conn = psycopg2.connect(url)
        return conn, "postgres"

    # SQLite
    if not url_lower.startswith("sqlite:///"):
        db_path = "app.db"
    else:
        db_path = url.split("sqlite:///", 1)[1] or "app.db"

    conn = sqlite3.connect(db_path, isolation_level=None)  # autocommit
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn, "sqlite"


def _normalize_sql_for_backend(sql: str, backend: str) -> str:
    """
    Делает SQL совместимым с выбранным движком.
    """
    if backend == "postgres":
        return sql

    adapted = sql
    replacements = {
        "SERIAL PRIMARY KEY": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "BIGINT": "INTEGER",
        "JSONB": "TEXT",
        "TIMESTAMPTZ": "TEXT",
        "BOOLEAN": "INTEGER",
        "VARCHAR(40)": "TEXT",
    }
    for src, dst in replacements.items():
        adapted = adapted.replace(src, dst)

    adapted = adapted.replace("DEFAULT NOW()", "DEFAULT (datetime('now'))")
    adapted = adapted.replace("DEFAULT now()", "DEFAULT (datetime('now'))")
    adapted = adapted.replace("DEFAULT TRUE", "DEFAULT 1")
    adapted = adapted.replace("DEFAULT FALSE", "DEFAULT 0")

    return adapted


def init_db_schema():
    """
    Проверяет и создает все необходимые таблицы в базе данных, если они отсутствуют.
    """
    conn, backend = _connect()
    cur = conn.cursor()

    logger.info("Проверка и инициализация схемы базы данных (%s)...", backend)

    ddl_statements = [
        """
        CREATE TABLE IF NOT EXISTS appeals (
            case_id INTEGER PRIMARY KEY,
            applicant_chat_id BIGINT,
            decision_text TEXT,
            applicant_arguments TEXT,
            applicant_answers JSONB,
            council_answers JSONB,
            total_voters INTEGER,
            status TEXT,
            expected_responses INTEGER,
            timer_expires_at TIMESTAMPTZ,
            ai_verdict TEXT,
            message_thread_id INTEGER,
            is_reviewed BOOLEAN DEFAULT FALSE,
            review_data JSONB,
            commit_hash VARCHAR(40),
            verdict_log_id INTEGER,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS user_states (
            user_id TEXT PRIMARY KEY,
            state TEXT,
            data JSONB,
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS editors (
            user_id BIGINT PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            is_inactive BOOLEAN DEFAULT FALSE,
            added_at TIMESTAMPTZ DEFAULT NOW()
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS interaction_logs (
            log_id SERIAL PRIMARY KEY,
            user_id BIGINT,
            case_id INTEGER,
            action TEXT,
            details TEXT,
            timestamp TIMESTAMPTZ DEFAULT NOW()
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS ai_chat_history (
            message_id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            sender TEXT NOT NULL CHECK (sender IN ('user', 'ai')),
            message_text TEXT NOT NULL,
            timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        """
    ]

    try:
        for sql in ddl_statements:
            cur.execute(_normalize_sql_for_backend(sql, backend))
        if backend == "postgres":
            conn.commit()
        logger.info("Инициализация схемы базы данных завершена.")
    except Exception as e:
        logger.exception("Не удалось инициализировать схему БД: %s", e)
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


def get_db():
    """
    Открывает новое соединение с БД, если его еще нет для текущего запроса.
    """
    if 'db' not in g:
        conn, _backend = _connect()
        g.db = conn
    return g.db

def close_db(e=None):
    """
    Закрывает соединение с БД, если оно было установлено.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    """
    Регистрирует функции управления БД в приложении Flask.
    """
    app.teardown_appcontext(close_db)