from anahiepro._criterias_builders._base_criteria_builder import _BaseCriteriaBuilder


class _ListCriteriaBuilder(_BaseCriteriaBuilder):
    def __init__(self, criterias):
        super().__init__(criterias)

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
    

    def has_same_depth(self):
        try:
            depths = [self._get_depth(item) for item in self.criterias]
            return len(set(depths)) == 1
        except ValueError:
            return False


    def build_criteria(self):
        if self.has_same_depth():
            return self.criterias
        raise TypeError("The depth of elements is different.")