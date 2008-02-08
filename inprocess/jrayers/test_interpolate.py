class interp(object):
    def do_interp(self, first, last, steps):
        diff = last - first
        inc = diff/steps
        lst = []
        lst.append(first)
        for i in range(0,steps):
            x = lst[i] + inc
            lst.append(x)
        lst.pop()
        lst.append(last)
        return lst
            