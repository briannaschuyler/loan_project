def eval_string(x):
  if type(x) == str:
    return eval(x)
  else:
    return []

def get_date(x):
  from datetime import datetime
  return datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ").date()

def set_to_string(input_set):
  # Takes a set as input and outputs a string with the elements of that set
  output = ''
  for s in input_set:
    if s is not None:
      output = output + s + ', '
  return output[:-2]
