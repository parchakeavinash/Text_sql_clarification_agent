from sqlalchemy import create_engine,text

from config.env_variable import settings


engine = create_engine(
    settings.DATABASE_URL
)


def execute_query(sql:str):
    with engine.connect() as connection:
        result = connection.execute(text(sql))

        columns = result.keys()

        return [

            dict(zip(columns,row))
            for row in result.fetchall()
        ]