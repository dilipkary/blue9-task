from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, BLOB
from config.database import meta, engine


Upload_Data = Table(
    'files', meta,
    Column('id', Integer, primary_key=True),
    Column('userid', String(255)),
    Column('filename', String(255))

)
# meta.create_all(engine)
