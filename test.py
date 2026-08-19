import ipaddress

private_ip = [
    ipaddress.IPv4Network('0.0.0.0/8'),
    ipaddress.IPv4Network('10.0.0.0/8'),
    ipaddress.IPv4Network('127.0.0.0/8'),
    ipaddress.IPv4Network('169.254.0.0/16'),
    ipaddress.IPv4Network('172.16.0.0/13'),
    ipaddress.IPv4Network('192.0.0.0/29'),
    ipaddress.IPv4Network('192.0.0.170/31'),
    ipaddress.IPv4Network('192.0.2.0/24'),
    ipaddress.IPv4Network('192.168.0.0/16'),
    ipaddress.IPv4Network('198.18.0.0/15'),
    ipaddress.IPv4Network('198.51.100.0/24'),
    ipaddress.IPv4Network('203.0.113.0/24'),
    ipaddress.IPv4Network('240.0.0.0/4'),
    ipaddress.IPv4Network('255.255.255.255/32'),
    ipaddress.IPv4Network('169.254.0.0/16'),
    ipaddress.IPv4Network('127.0.0.0/8'),
    ipaddress.IPv4Network('224.0.0.0/4'),
    ipaddress.IPv4Network('100.64.0.0/10'),
]

class Node:
    def __init__(self, ip):
        self.ip = ipaddress.ip_network(ip)
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
    cn_list.extend(private_ip)
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