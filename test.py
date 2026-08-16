import ipaddress
cnip = []
with open(r'china_ip_list.txt','r') as r:
    for line in r:
        line = line.strip()
        if not line:
            continue
        ip = ipaddress.ip_network(line)
        cnip.append(ip)
result = list(ipaddress.collapse_addresses(cnip))

print("原始数量:", len(cnip))
print("合并后数量:", len(result))

class Node :
    def __init__(self,ip):
        self.ip = ip
        self.left = None
        self.right = None
        self.is_cn = False
    def split(self):
        subnet = list(
            self.ip.subnets(prefixlen_diff=1)
        )
        self.left = Node(subnet[0])
        self.right = Node(subnet[1])
def insert_cn(node,cn)
    if node.network == cn:
        node.is_cn = True
        return
    if not node.network.overlaps(cn):
        return
    if not node.left is None:
        node.split()
    insert_cn(node.left,cn)
    insert_cn(node.right,cn)

def dump_non_cn(node, result):
    if node.is_cn:
        return
    if node.left is None:
        result.append(node.network)
        return
    dump_non_cn(node.left, result)
    dump_non_cn(node.right, result)


