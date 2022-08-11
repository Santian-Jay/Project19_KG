
def run(r):
    mask = (r>0)*1.0
    return mask

a = [-1, 0, 1, 2]
for i in a:
    print(run(i))