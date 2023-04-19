import pytest
from src.landuo import cached_property
import time
from timeit import timeit


class PersonThree:

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

    @name.deleter
    def name(self):
        print("Deleting `self.name`...")


@pytest.fixture
def person_james():
    return PersonThree('James')


@pytest.fixture
def person_peter():
    return PersonThree('Peter')

def test_first_call_takes_two_seconds(person_james):
    assert timeit(lambda: person_james.name, number=1) >= 2

def test_second_calls_onwards_faster():
    james = PersonThree('James')
    assert timeit(lambda: james.name, number=10) < 2.5

def test_output_printed(person_james, capfd):
    person_james.name
    out, err = capfd.readouterr()
    assert out == "Sleeping for 2 seconds...\n"

def test_name_property(person_james):
    assert person_james.name == "James"


def test___set__method_working(capfd):
    person_james = PersonThree('James')
    print("*", person_james.__dict__)
    assert person_james.name == 'James'
    person_james.name = 'Thomas'
    print("**", person_james.__dict__)
    assert person_james.name == 'Thomas'
    out, err = capfd.readouterr()
    # caches immediately
    assert timeit(lambda: person_james.name, number=10) < 2.5
    assert "Sleeping for 1 seconds...\n" in out
    
    assert person_james.__dict__ == {'_name': 'Thomas', 'name': 'Thomas'}
    print(out, err)
    
def test_james_peter_names_work(person_james, person_peter):
    assert person_james.name == 'James'
    assert person_peter.name == 'Peter'
    
def test_invalidating_cache(capfd):
    person_james = PersonThree('James')
    assert person_james.name == 'James'
    person_james.name = 'Thomas'
    
    person_james.name
    assert timeit(lambda: person_james.name, number=10) < 2.5
    
    assert person_james.name == 'Thomas'
    del person_james.name
    assert not hasattr(person_james, '_name')
    assert not hasattr(person_james, 'name')
    
        

