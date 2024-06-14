from anahiepro._criterias_builders._base_criteria_builder import _BaseCriteriaBuilder


class _EmptyCriteriaBuilder(_BaseCriteriaBuilder):
    def __init__(self, criterias):
        super().__init__(criterias)
    
    def has_same_depth(self):
        return True

    def build_criteria(self):
        return list()