relation_head = {}
relation_tail = {}

data = open("../subgraph_v1/train2id.txt", "r")

total = int(data.readline())

for i in range(total):
    content = data.readline()
    head, tail, relation = content.strip().split()
    if (relation, head) not in relation_head:
        relation_head[relation, head] = []
    if (relation, tail) not in relation_tail:
        relation_tail[relation, tail] = []

print(len(relation_head))
print(len(relation_tail))

print(relation_head)
print(relation_tail)