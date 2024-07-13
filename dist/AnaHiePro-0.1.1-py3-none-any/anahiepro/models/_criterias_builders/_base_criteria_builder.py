from abc import ABC, abstractmethod


class _BaseCriteriaBuilder(ABC):
    def __init__(self, criterias):
        self.checkDepth = True
        self.criterias = criterias
    
    @abstractmethod
    def has_same_depth(self):
        pass

    @abstractmethod
    def build_criteria(self):
        pass
    
    @abstractmethod
    def _get_depth(self):
        pass
    
    def not_throw_exception_while_build(self):
        self.checkDepth = False