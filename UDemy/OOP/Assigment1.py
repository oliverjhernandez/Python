#/usr/bin/env python


class MaxSizeList(object):
    """docstring for MaxSizeList."""
    def __init__(self, size):
        self.size = size
        self.mylist = []

    def push(self, value):
        self.mylist.append(value)
        if len(self.mylist) > self.size:
            self.mylist.pop(0)

    def get_list(self):
        return self.mylist

a = MaxSizeList(3)
b = MaxSizeList(1)

a.push("hey")
a.push("hi")
a.push("let's")
a.push("go")

b.push("hey")
b.push("hi")
b.push("let's")
b.push("go")

print(a.get_list())
print(b.get_list())
