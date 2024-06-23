from anahiepro.models._criterias_builders._base_criteria_builder import _BaseCriteriaBuilder
from anahiepro.nodes import Criteria



class _ListDictCriteriaBuilder(_BaseCriteriaBuilder):
    def __init__(self, criterias):
        if not self._is_valid_structure(criterias):
            raise TypeError("The criterias have wrong structure.")
        super().__init__(criterias)
    
    
    def has_same_depth(self):
        try:
            depths = [self._get_depth(item) for item in self.criterias]
            return len(set(depths)) == 1
        except ValueError:
            return False


    def build_criteria(self):
        if not self.has_same_depth() and self.checkDepth:  # Throw an exception only if the flag enabled.
            raise TypeError("The depths of elements are different.")
        return self.criterias
    
    
    def _get_depth(self, structure, depth=0):
        if isinstance(structure, dict):
            for key, value in structure.items():
                return self._get_depth(value, depth + 1)
        elif isinstance(structure, list):
            depths = [self._get_depth(item, depth) for item in structure]
            if len(set(depths)) != 1:
                raise ValueError("Different depths found in list: {}".format(depths))
            return depths[0]
        return depth
    

    def _is_valid_structure(self, obj):
        if not isinstance(obj, list):
            return False

        for item in obj:
            if not isinstance(item, dict):
                return False
            for key, value in item.items():
                if not isinstance(key, Criteria):
                    return False
                if value is not None:
                    if not self._is_valid_structure(value):
                        return False
        return True
