from dataclasses import dataclass, field


@dataclass()
class Foo():
    id: str
    name: str = field(init=False)

    def __post_init__(self):
        self.name = self.__get_name()

    def __get_name(self):
        return 'helo'


f = Foo('asas')
print(f.__dict__)
