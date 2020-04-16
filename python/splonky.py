import inspect

def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]

"""
This code allows us to rerun python cells
and not update certain special varialbes
that should be controlled by a input widget
"""

class spl_:
  pass

class spltype(type):
  def __getattr__(cls, key):
    if hasattr(cls._, key):
      return (key, getattr(cls._, key))
  def __setattr__(cls, key, value):
    if key == "lock":
      super(spltype, cls).__setattr__(key, value)
    elif cls.lock:
      # Don't update if locked
      return (getattr(cls, key))
    else:
      setattr(cls._, key, value)

class spl(metaclass=spltype):
  _ = spl_
  lock = True

"""
> import splonky as spl
> spl.x = 5
> x
5
> spl.lock = True
> x = 8
> x  # still 5!
5 
"""

# Input Widgets
class Slider:
  """
  Takes a pandas dataframe and generates json interpreted
  by the splonky client as svelte component data

  Usage
  --------
  import splonky as spl

  spl.x = 5
  spl.Slider(x, 0, 100)
  """
  def __init__(self, var, min, max):
    self.value = var
    self.varname = retrieve_name(var)
    self.min = min
    self.max = max

  def data(self):
    return {
      "varname": self.varname,
      "min": self.min,
      "max": self.max,
      "value": self.value
    }
  
  def _repr_json_(self):
    repr_ = {
      "kind": "Slider",
      "data": self.data()
    }
    return repr_ 


# Graphics
class Chart:
  """
  Takes a pandas dataframe and generates json interpreted
  by the splonky client as svelte component data

  Parameters
  -----------
  df: pandas.DataFrame
  kind: one of 'Bar', 'Line'
  title: title for the chart

  """
  def __init__(self, df, kind, title=None):
    self.df = df
    self.kind = kind
    self.title = title

  def data(self):
    self.df

    return {
      "labels": self.x if self.x else list(self.df.index),
      "datasets": [ {"label": c, "data": list(v.values)} 
        for c,v in self.df.items()]
    }
  
  def _repr_json_(self):
    repr_ = {
      "kind": self.kind,
      "data": self.data()
    }
    if self.title: repr_['title'] = self.title
    return repr_

def chart(dataframe, kind, title=None):
  """
  Return an object which can be displayed
  as a svg chart
  """
  return Chart(dataframe, kind)


