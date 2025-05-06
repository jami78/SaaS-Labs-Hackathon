from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver
import os

DATABASE_URL = os.getenv('DATABASE_URL')


connection_kwargs = {
    "autocommit": True,
    "prepare_threshold": 0,
}


pool = ConnectionPool(
    conninfo=DATABASE_URL,
    max_size=20,
    kwargs=connection_kwargs,
)

checkpointer = PostgresSaver(pool)
    



