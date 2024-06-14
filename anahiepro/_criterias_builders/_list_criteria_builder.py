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

            nested_criteria = [{child: build_nested_criteria(child)} for child in children]
            return nested_criteria

        built_criteria = [{ criteria: build_nested_criteria(criteria) } for criteria in self.criterias if build_nested_criteria(criteria)]
        
        for item in self.criterias[:]:
            self._clear_criterias(item)
            self.criterias.remove(item)

        return built_criteria


    def _clear_criterias(self, item):
        if not item.children:
            for parent in item.parents:
                parent.children.remove(item)
            item.parents = []
            return

        for child in item.children[:]:
            child.parents.remove(item)
            self._clear_criterias(child)

        item.children = []
    

    def _get_depth(self):
        upper_criterias_depth = [list() for _ in range(len(self.criterias))]

        def get_depth(depth, item, depth_list):
            if len(item.get_children()) == 0:
                return depth
            for child in item.get_children():
                depth_list.append(get_depth(depth + 1, child, depth_list))

        for depth_list, criteria in zip(upper_criterias_depth, self.criterias):
            get_depth(0, criteria, depth_list)

        flattened_data = [item for sublist in upper_criterias_depth for item in sublist]
        return flattened_data


    def _is_valid_structure(self, criterias):
        return all(isinstance(c, Criteria) for c in criterias)
