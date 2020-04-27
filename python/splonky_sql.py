import warnings
import pandas as pd
import time

warnings.simplefilter('ignore')

import psycopg2

"""
hack! TODO rewrite
basically, take a sql query and an id
bind the resulting dataframe to a
variable name generated from the id
and keep that name consistent for the id
"""

pgconfig = dict(
    prod='host=localhost port=20199',
    staging="host=localhost port=22199"
)

class SqlResult:
  def __init__(self, name, status, nrows, seconds, errormsg):
    self.name = name
    self.status = status
    self.errormsg = errormsg
    self.nrows = nrows
    self.seconds = seconds

  def _repr_json_(self):
    return dict(
      spl=True,
      kind='SqlResult',
      data=dict(
        name=self.name,
        status=self.status,
        nrows=self.nrows,
        seconds=self.seconds,
        errormsg=self.errormsg
      )
    )

  def __repr__(self):
    return f"""
      spl=True,
      kind='SqlResult',
      data=dict(
        name={self.name},
        status={self.status},
        nrows={self.nrows},
        seconds={self.seconds},
        errormsg={self.errormsg}
      )
    )
    """

class RS:
    conn = None
    cur = None
    @classmethod
    def connect(cls, env):
        cls.conn = psycopg2.connect(pgconfig[env])
        cls.cur = cls.conn.cursor()

    @classmethod
    def get(cls, i, query):
        try:
            t = time.time()
            cls.cur.execute(query)
            rows = cls.cur.fetchall()
            columns = [c.name for c in cls.cur.description]
            name = f'cell{i}'
            data = pd.DataFrame(rows, columns=columns)
            display(SqlResult(
              name,
              "OK", 
              len(data), 
              time.time() - t,
              None
            ))
            return (name, data)
        except (
            psycopg2.DatabaseError,
            psycopg2.ProgrammingError
        ) as e:
            display(SqlResult(
              name,
              "ERR", 
              None, 
              None,
              e.pgerror
            ))
            cls.conn.rollback()
            raise(e)

RS.connect('prod')
