from abc import ABC, abstractmethod


class _BaseCriteriaBuilder(ABC):
    def __init__(self, criterias):
        self.criterias = criterias
    
    @abstractmethod
    def has_same_depth(self):
        pass

    @abstractmethod
    def build_criteria(self):
        pass