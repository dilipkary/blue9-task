from email.policy import default
from pymysql import STRING
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from config.database import meta, engine

users = Table(
    'users', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('email', String(255)),
    Column('password', String(255)),
    Column('type', String(255)),
    Column('is_active', Boolean, default=False),
    Column('confirmation', String(255))


)
# meta.create_all(engine)
