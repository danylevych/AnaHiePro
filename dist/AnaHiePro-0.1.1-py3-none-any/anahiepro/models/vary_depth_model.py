from pprint import pprint
from anahiepro.models.model import Model
from anahiepro.models._criterias_builders._wrapper_criteria_builder import _WrapperCriteriaBuilder
from anahiepro.models._criteria_normalizers._criteria_normalizer import _CriteriaNormalizer


class VaryDepthModel(Model):
    def __init__(self, problem, criterias, alternatives):
        builder = _WrapperCriteriaBuilder(criterias)
        if not builder.has_same_depth():
            criteria_normalizer = _CriteriaNormalizer(builder)
            criterias = criteria_normalizer.get_normalized_criterias()
        
        super().__init__(problem, criterias, alternatives)
        
  