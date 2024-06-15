from anahiepro._criterias_builders._base_criteria_builder import _BaseCriteriaBuilder
from anahiepro.nodes import Criteria



class _ListCriteriaBuilder(_BaseCriteriaBuilder):
    def __init__(self, criterias):
        if not self._is_valid_structure(criterias):
            raise TypeError("The criterias have wrong structure.")
        super().__init__(criterias)


    def has_same_depth(self):
        try:
            return len(set(self._get_depth())) == 1
        except Exception:
            return False
        

    def build_criteria(self):
        if not self.has_same_depth():
            raise TypeError("The depths of elements are different.")    

        def build_nested_criteria(criteria):
            if not isinstance(criteria, Criteria):
                return None

            children = criteria.get_children()
            if not children:
                return None

            nested_criteria = [{child.__copy__(): build_nested_criteria(child)} for child in children]
            return nested_criteria

        built_criteria = [{ criteria.__copy__() : build_nested_criteria(criteria) } for criteria in self.criterias]

        return built_criteria
    

    def _get_depth(self):
        upper_criterias_depth = [list() for _ in range(len(self.criterias))]

        def get_depth(depth, item):
            if not item.get_children():
                return depth
            return max(get_depth(depth + 1, child) for child in item.get_children())

        for depth_list, criteria in zip(upper_criterias_depth, self.criterias):
            depth_list.append(get_depth(0, criteria))

        flattened_data = [item for sublist in upper_criterias_depth for item in sublist]
        return flattened_data


    def _is_valid_structure(self, criterias):
        if not isinstance(criterias, list):
            return False
        
        return all(isinstance(c, Criteria) for c in criterias)
