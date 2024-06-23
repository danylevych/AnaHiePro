from anahiepro.models._criterias_builders._base_criteria_builder import _BaseCriteriaBuilder
from anahiepro.models._criterias_builders._empty_criteria_builder import _EmptyCriteriaBuilder
from anahiepro.models._criterias_builders._list_criteria_builder import _ListCriteriaBuilder
from anahiepro.models._criterias_builders._list_dict_ctiteria_builder import _ListDictCriteriaBuilder
from anahiepro.nodes import Criteria



class _WrapperCriteriaBuilder():
    def __init__(self, criterias):
        self._builder : _BaseCriteriaBuilder = self._set_builder(criterias)
    

    def build_criterias(self):
        return self._builder.build_criteria()
    
    
    def has_same_depth(self):
        return self._builder.has_same_depth()
    
    
    def get_depth(self):
        return self._builder._get_depth()
    
    
    def _set_builder(self, criterias):
        if criterias is None:
            return _EmptyCriteriaBuilder(criterias)
        
        if isinstance(criterias, list):
            if len(criterias) == 0:
                return _EmptyCriteriaBuilder(criterias)
            elif isinstance(criterias[0], dict):
                return _ListDictCriteriaBuilder(criterias)
            elif all(isinstance(c, Criteria) for c in criterias):
                return _ListCriteriaBuilder(criterias)
            
        raise TypeError("The type of criterias is invalid. It might be: 'Criteria' or 'list' of 'Criteria'.")
    