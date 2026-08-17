import ipaddress

class Node:
    def __init__(self, ip):
        self.ip = ipaddress.ip_network(ip) if isinstance(ip, str) else ip
        self.left = None
        self.right = None
        self.is_cn = False

    def split(self):
        subnets = list(self.ip.subnets(prefixlen_diff=1))
        self.left = Node(subnets[0])
        self.right = Node(subnets[1])

def insert_cn(node, cn):
    if node.ip == cn:
        node.is_cn = True
        return
    if not node.ip.overlaps(cn):
        return
    if node.left is None:
        node.split()
    insert_cn(node.left, cn)
    insert_cn(node.right, cn)

def dump_non_cn(node, result):
    if node.is_cn:
        return
    if node.left is None:
        result.append(node.ip)
        return
    dump_non_cn(node.left, result)
    dump_non_cn(node.right, result)

def load_file(filename):
    cn_list = []
    with open(filename, 'r') as r:
        for line in r:
            line = line.strip()
            if not line:
                continue
            ip = ipaddress.ip_network(line)
            cn_list.append(ip)
    return cn_list

def main():
    cn_list = load_file('china_ip_list.txt')
    root = Node('0.0.0.0/0')
    for cn in cn_list:
        insert_cn(root, cn)

    result = []
    dump_non_cn(root, result)
    print(len(result))
    with open(r'non-cn.txt', 'w') as f:
        for network in result:
            f.write(str(network) + '\n')
    print('完成')

if __name__ == '__main__':
    main()