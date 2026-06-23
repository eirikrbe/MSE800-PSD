
class Singleton:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
            
        return cls._instance


class MyClass(Singleton):

    def __init__(self, a):
         self.a = a

    def __str__(self):
         return f"a is {self.a}"


if __name__ == "__main__":

    a = Singleton()
    b = Singleton()

    print(id(a), id(b))

    class_a = MyClass(10)
    print(class_a)
    class_b = MyClass(20)
    print(class_b)
    print(f"class_a is {class_a}, class_b is {class_b}")
