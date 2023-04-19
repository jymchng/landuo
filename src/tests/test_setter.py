import pytest
from src.landuo import cached_property
import time
from timeit import timeit


class PersonTwo:

    def __init__(self, name: str) -> None:
        self._name = name

    @cached_property
    def name(self):
        print("Sleeping for 2 seconds...")
        time.sleep(2)
        return self._name

    @name.setter
    def name(self, new_name):
        time.sleep(1)
        print("Sleeping for 1 seconds...")
        if not isinstance(new_name, str):
            raise ValueError
        self._name = new_name

@pytest.fixture
def person_two_james():
    return PersonTwo('James')

@pytest.fixture
def person_two_peter():
    return PersonTwo('Peter')

def test_first_call_takes_two_seconds(person_two_james):
    assert timeit(lambda: PersonTwo('James').name, number=1) >= 2

def test_second_calls_onwards_faster():
    james = PersonTwo('James')
    assert timeit(lambda: james.name, number=10) < 2.5

def test_output_printed(capfd):
    james = PersonTwo('James')
    _ = james.name
    out, err = capfd.readouterr()
    assert out == "Sleeping for 2 seconds...\n"

def test_name_property(person_two_james):
    assert person_two_james.name == "James"


def test___set__method_working(capfd):
    person_two_james = PersonTwo("James")
    print("*", person_two_james.__dict__)
    assert person_two_james.name == 'James'
    person_two_james.name = 'Thomas'
    person_two_james.name
    assert timeit(lambda: person_two_james.name, number=10) < 2.5
    assert person_two_james.name == 'Thomas'
    assert person_two_james.__dict__ == {'_name': 'Thomas' , 'name': 'Thomas'}
    

def test_james_peter_names_work(person_two_james, person_two_peter):
    assert person_two_james.name == 'James'
    assert person_two_peter.name == 'Peter'