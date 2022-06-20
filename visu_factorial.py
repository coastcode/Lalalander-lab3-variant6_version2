from typing import Any


class Lambda(object):
    def __init__(self) -> None:
        self.node = Node()
        self.node.label = "start"
        self.node.children = []

    def FACT(self, n: int) -> Any:
        cur = self.node
        while cur.next is not None:
            cur = cur.next
        node_new = Node()
        cur.next = node_new     # 14
        if cur is None:
            cur = cur.next        # 15
        cur.label = "FACT"
        while cur.next is not None:
            cur = cur.next
        fact = (lambda a: lambda v: a(a, v))(
            lambda s, x: 1 if x == 0 else x * s(s, x - 1))
        a = fact(n)
        while n > 1:
            cur.addkid(f'{n}')
            n -= 1
        cur.addkid('1')
        cur.addkid(f'{a}')
        return a

    def visualize(self) -> str:
        cur = self.node
        res = []
        res.append("digraph G {")
        res.append(" rankdir=LR;")
        res.append('    start')
        while cur is not None:
            if cur.label == "start":
                cur = cur.next   # 37
            elif cur.label == "FACT":
                print(cur.label)
                for n in range(0, len(cur.children) - 2):
                    print(f'((λf.λx.n=0?1:n*f(n-1))(Y M)){cur.children[n]}')
                    print(f'=>(λn.n=0?1:n * ((Y M)(n - 1)))){cur.children[n]}')
                    print(f'=>{cur.children[n]}*((Y M)({cur.children[n]}- 1))')
                    print(f'=>{cur.children[n]}*((Y M){cur.children[n + 1]})')
                for i in range(0, len(cur.children) - 2):
                    res.append(f'{cur.children[i]}*')
                res.append('1')
                res.append(f'{cur.children[i + 2]}')
                cur = cur.next       # 49
        res.append("}")
        # print(res)
        return "\n".join(res)


class Node:
    def __init__(self, label: Any = None, children: Any = None) -> None:
        self.label = label
        self.children = children if children is not None else list()
        self.next = None

    def addkid(self, n: str) -> Any:
        self.children.append(n)
        return self
