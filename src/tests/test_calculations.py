import pytest
from src.landuo import cached_property
import time
from timeit import timeit

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
    
    @name.setter
    def name(self, new):
        if not isinstance(new, str):
            raise ValueError("`new` must be of type `str`.")
        self._name = new
        
    @cached_property
    def height(self):
        print("Sleep 2 seconds.")
        time.sleep(2)
        return self._height
    
    @height.setter
    def height(self, new):
        if not isinstance(new, float):
            raise ValueError("`new` must be of type `str`.")
        self._height = new
    
    @cached_property
    def weight(self):
        print("Sleep 2 seconds.")
        time.sleep(2)
        return self._weight
    
    @weight.setter
    def weight(self, new):
        if not isinstance(new, int):
            raise ValueError("`new` must be of type `str`.")
        self._weight = new
        
    @cached_property
    def bmi(self):
        return self.height + self.weight