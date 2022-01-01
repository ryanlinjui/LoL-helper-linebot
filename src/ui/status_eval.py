from . import req_keys
from .graph import export_graph
def user_perf_pic(user_perf:dict, filename:str):
    # key required in user performance
    data = []
    for k in req_keys:
        if k not in req_keys:
            raise ValueError(f"require key {k}")
        data.append(user_perf[k])
    export_graph(data, filename)