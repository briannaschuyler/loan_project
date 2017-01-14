def eval_string(x):
    if type(x) == str:
         return eval(x)
    else:
        return []

def get_date(x):
    from datetime import datetime
    return datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ").date()
