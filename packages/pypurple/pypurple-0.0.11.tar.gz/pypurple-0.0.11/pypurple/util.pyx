def unicode_to_c(py_po):
    po = {}
    for (k, v) in py_po.items():
        po[k.encode()] = v.encode() if type(v) is str else v
    return po
