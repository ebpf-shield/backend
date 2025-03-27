import logging
from typing import Annotated
from fastapi import Depends
from asyncpg import Connection, connect

from app.core.config import settings


logger = logging.getLogger(__name__)


class PostgresClientManager:
    _conn: Connection | None = None

    @property
    def conn(self) -> Connection:
        if self.conn is None:
            raise Exception("PostgreSQL client is not initialized.")
        return self._conn

    async def connect(self):
        try:
            self._conn = await connect(
                dsn=settings.CONNECTION_STRING, database=settings.DB_NAME
            )

            logger.info("Connected to postgreSQL")

        except Exception as _e:
            logger.error("Unable to connect to postgreSQL")
            print("Error")

    async def close(self):
        if self._conn is None:
            raise Exception("PostgreSQL client is not initialized.")

        try:
            self._conn.close()
            logger.info("Closed connection to PostgreSQL")
        except Exception as _e:
            logger.error("Unable to close connection to PostgreSQL")
            raise _e


posgtes_client_manager = PostgresClientManager()
CommonPostgresClient = Annotated[
    Connection,
    Depends(posgtes_client_manager.conn, use_cache=True),
]
