class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]


@Singleton
class Cls2(object):
    def __init__(self):
        pass


if __name__ == '__main__':
    cls1 = Cls2()
    cls2 = Cls2()
    print(id(cls1) == id(cls2))
