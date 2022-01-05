d = {"ab":2, "bbb":5,"sadsd":1}
minval = min(d.values())
res = list(filter(lambda x: d[x]==minval, d))
print(res)