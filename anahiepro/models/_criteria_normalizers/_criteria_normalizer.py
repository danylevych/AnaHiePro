from pprint import pprint
from anahiepro.models._criterias_builders._wrapper_criteria_builder import _WrapperCriteriaBuilder
from anahiepro.nodes import DummyCriteria


class _CriteriaNormalizer():
    def __init__(self, criteria_builder: _WrapperCriteriaBuilder):
        criteria_builder._builder.not_throw_exception_while_build() # The criterias do not have the same depth if we are here. 
        self._criterias = criteria_builder.build_criterias()
        self._criterias = self._normalize_criteria_depth(self._criterias)
        pprint(self._criterias)
        
    
    def _normalize_criteria_depth(self, criterias):        
        max_depth = max(self._get_depth(criterias))
        normalized_criterias = []
        
        for criteria_dict in criterias:
            normalized_criterias.append(self._normalize_criteria_dict(criteria_dict, max_depth))
        
        return normalized_criterias


    def _get_depth(self, criterias):
        depths = [0 for _ in range(len(criterias))]
        for index, criteria_dict in enumerate(criterias):
            for _, children in criteria_dict.items():
                depths[index] = self._get_max_child_depth(children, 0)
        return depths


    def _get_max_child_depth(self, children_list, depth=0):
        if children_list is None:
            return depth
        max_depth = depth
        
        for inner_children_list in children_list:
            for _, child_children in inner_children_list.items():
                child_depth = self._get_max_child_depth(child_children, depth + 1)
                if child_depth > max_depth:
                    max_depth = child_depth
        return max_depth


    def _normalize_criteria_dict(self, criteria_dict, max_depth, current_depth=0):
        normalized_dict = {}
        
        for parent, children in criteria_dict.items():
            if children is None and current_depth < max_depth:
                normalized_dict[DummyCriteria()] = [self._normalize_criteria_dict({parent: children}, max_depth, current_depth + 1)]
            elif children is not None:
                normalized_children = []
                for child in children:
                    normalized_children.append(self._normalize_criteria_dict(child, max_depth, current_depth + 1))
                normalized_dict[parent] = normalized_children
            
            else:
                normalized_dict[parent] = children
        
        return normalized_dict
    
    
    def get_normalized_criterias(self):
        return self._criterias