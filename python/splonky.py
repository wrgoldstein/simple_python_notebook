import shortuuid

SplRegistry = {}

# Input Widgets
class Slider:
  global SplRegistry

  lookup = {}
  """
  Takes a pandas dataframe and generates json interpreted
  by the splonky client as svelte component data

  Usage
  --------
  import splonky as spl

  spl.Slider(0, 100, 50, lambda x: print(x))
  """
  def __init__(self, min, max, value, f):
    """
    Generates an interactive Slider.

    Params
    =========
    min: The minimum value of the slider
    max: The maximum value of the slider
    value: The default value of the slider
    f: A one parameter function that is called
    with the output of the slider.

    """
    self.min = min
    self.max = max
    self.value = value
    self.f = f
    self._id = shortuuid.uuid()

    # SplRegistry is instantiated by the client.
    # Probably should just used a global variable here
    SplRegistry[self._id] = f

  def data(self) -> dict:
    return {
      "min": self.min,
      "max": self.max,
      "value": self.value,
      "id": self._id
    }
  
  def _repr_json_(self) -> dict:
    return {
      "id": self._id,
      "spl": True,
      "kind": "Slider",
      "data": self.data()
    }

class Dropdown:
  global SplRegistry

  lookup = {}
  """
  Takes a pandas dataframe and generates json interpreted
  by the splonky client as svelte component data

  Usage
  --------
  import splonky as spl

  spl.Slider(0, 100, 50, lambda x: print(x))
  """
  def __init__(self, options, value, f):
    """
    Generates an interactive Slider.

    Params
    =========
    options: A list of strings for the dropdown menu
    value: The default value of the dropdown
    f: A one parameter function that is called
    with the output of the dropdown selection.

    """
    self.options = options
    self.value = value
    self.f = f
    self._id = shortuuid.uuid()

    # SplRegistry is instantiated by the client.
    # Probably should just used a global variable here
    SplRegistry[self._id] = f

  def data(self) -> dict:
    return {
      "options": self.options,
      "value": self.value,
      "id": self._id
    }
  
  def _repr_json_(self) -> dict:
    return {
      "id": self._id,
      "spl": True,
      "kind": "Dropdown",
      "data": self.data()
    }


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
      "labels": list(self.df.index),
      "datasets": [ {"label": c, "data": list(v.values)} 
        for c,v in self.df.items()]
    }
  
  def _repr_json_(self):
    repr_ = {
      "spl": True,
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


