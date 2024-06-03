from abc import ABC, abstractmethod
import numpy as np
from anahiepro.pairwise import PairwiseComparisonMatrix

class Node(ABC):    
    def __init__(self, name, parents=None, children=None, id=0):
        self._id = id
        self.name = name
        self.parents = parents if parents is not None else []
        self.children = children if children is not None else []
        self.pcm = None
    
    def get_name(self):
        return self.name
    
    def get_parents(self):
        return self.parents
    
    def get_children(self):
        return self.children
    
    @abstractmethod
    def add_child(self, child):
        pass
    
    def _add_parent(self, parent):
        if self._can_add(parent):
            self.parents.append(parent)
    
    def _can_add(self, item):
        return isinstance(item, Node)
    
    def show(self, depth=0): 
        graph = '-' * depth + self.__str__()
        for child in self.children:
            graph += child.show(depth + 1)
        return graph
    
    def compare(self, key :tuple):
        if len(key) != 2:
            return False
        
        return self.name == key[0] and self._id == key[1]
    
    def create_pcm(self):
        self.pcm = PairwiseComparisonMatrix(len(self.children))
    
    def set_matrix(self, matrix):
        if self.pcm:
            self.pcm.set_matrix(matrix)
    
    def set_comparison(self, i, j, value):
        if self.pcm:
            self.pcm.set_comparison(i, j, value)
    
    def get_priority_vector(self):
        if self.pcm:
            return self.pcm.calculate_priority_vector()
    
    def get_consistency_ratio(self):
        if self.pcm:
            return self.pcm.calculate_consistency_ratio()
    
    def get_pcm(self):
        if self.pcm:
            return self.pcm.matrix
    
    def __str__(self) -> str:
        return self.name + '\n'
    
    def __eq__(self, value) -> bool:
        return self.name == value.name and self._id == value._id
    
    def __hash__(self) -> int:
        return hash(self.name) + hash(self._id)


class Problem(Node):
    _problem_id = 0
    def __init__(self, name, children=None):
        super().__init__(name, None, children, Problem._problem_id)
        Problem._problem_id += 1
    
    def add_child(self, child):
        if self._can_add(child):
            self.children.append(child)
            child._add_parent(self)
        else:
            pass  # TODO: raise an exception.


class Criteria(Node):
    _criteria_id = 0
    def __init__(self, name, parents=None, children=None):
        super().__init__(name, parents, children, Criteria._criteria_id)
        Criteria._criteria_id += 1
    
    def add_child(self, child):
        if self._can_add(child):
            self.children.append(child)
            child._add_parent(self)
        else:
            pass  # TODO: raise an exception.


class Alternative(Node):
    _alternative_id = 0
    def __init__(self, name):
        super().__init__(name, id=Alternative._alternative_id)
        Alternative._alternative_id += 1
    
    def add_child(self, child):
        pass  # Alternatives don't have children in this context
