# Входные данные
import psycopg2
from abc import ABC, abstractmethod

from Trainee.Logic.DataBase import PostgreSQL_CFG


class DataBase(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def select_data(self):
        pass


class PostgresDB(DataBase):
    def connect(self):
        connection = psycopg2.connect(
            user=PostgreSQL_CFG.user,
            password=PostgreSQL_CFG.password,
            host=PostgreSQL_CFG.host,
            dbname=PostgreSQL_CFG.db_name
        )

        return connection

    def select_data(self, table_name):
        db_connection = self.connect()

        with db_connection.cursor() as cursor:
            cursor.execute(f'SELECT * from "{table_name}"')

            # fetchall возвращается список кортежей из одного элемента. Трансформируем в список
            return [i[0] for i in cursor.fetchall()]
