import pytest
from src.landuo import cached_property
import time
from timeit import timeit
from src.landuo.exceptions import SetterUnimplemented


class Person:

    def __init__(self, name: str, height: float, weight: int) -> None:
        self._name = name
        self._weight = weight
        self._height = height

    @cached_property
    def name(self):
        print("Sleep 2 seconds.")
        time.sleep(2)
        return self._name

    @cached_property
    def height(self):
        print("Sleep 2 seconds.")
        time.sleep(2)
        return self._height

    @cached_property
    def weight(self):
        print("Sleep 2 seconds.")
        time.sleep(2)
        return self._weight

    @cached_property
    def bmi(self):
        return self.height + self.weight


def factory():
    james = Person(name='James', height=1.5, weight=1)
    peter = Person(name='Peter', height=1.5, weight=2)
    mary = Person(name='Mary', height=1.5, weight=3)
    return james, peter, mary


def test_first_call_takes_two_seconds(capfd):
    james, peter, mary = factory()
    assert timeit(lambda: james.name, number=1) >= 2
    out, err = capfd.readouterr()
    assert out == "Sleep 2 seconds.\n"
    assert james.name == "James"
    


def test_second_calls_onwards_faster():
    james, peter, mary = factory()
    assert timeit(lambda: james.name, number=10) < 2.5


def test___set__method_raises():
    with pytest.raises(SetterUnimplemented):
        james, peter, mary = factory()
        james.name = 'Thomas'
        assert james.name == 'Thomas'


def test_james_peter_names_work():
    james, peter, mary = factory()
    assert peter.name == 'Peter'
    assert james.name == 'James'
    assert mary.name == 'Mary'
