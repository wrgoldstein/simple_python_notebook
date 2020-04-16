import warnings
import pandas as pd

warnings.simplefilter('ignore')

import psycopg2

"""
hack! need to rewrite
basically, take a sql query and an id
bind the resulting dataframe to a
variable name generated from the id
and keep that name consistent for the id
"""

pgconfig = dict(
    prod='host=localhost port=20199',
    staging="host=localhost port=22199"
)

class varbinding:
  def __init__(self, name):
    self.name = name

  def _repr_json_(self):
    return dict(
      varbinding=self.name
    )

class rs:
    cells = []
    conn = None
    cur = None
    @classmethod
    def connect(cls, env):
        cls.conn = psycopg2.connect(pgconfig[env])
        cls.cur = cls.conn.cursor()

    @classmethod
    def get(cls, cell_id, query):
        try:
            cls.cur.execute(query)
            rows = cls.cur.fetchall()
            columns = [c.name for c in cls.cur.description]
            try:
              i = cls.cells.index(cell_id)
            except:
              i = len(cls.cells)
              cls.cells.append(cell_id)
            name = f'data{i}'
            data = pd.DataFrame(rows, columns=columns)
            display(varbinding(name))
            globals()[name] = data
            return data
        except (
            psycopg2.DatabaseError,
            psycopg2.ProgrammingError

        ) as e:
            cls.conn.rollback()
            raise(e)

rs.connect('prod')
