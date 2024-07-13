import set_up_test_pathes

import unittest
from anahiepro.models._criterias_builders._wrapper_criteria_builder import _WrapperCriteriaBuilder
from anahiepro.models._criteria_normalizers._criteria_normalizer import _CriteriaNormalizer
from anahiepro.nodes import Criteria, DummyCriteria



class TestCriteriaNormalizer(unittest.TestCase):
    
    def get_normalized_criterias(self, criterias):
        builder = _WrapperCriteriaBuilder(criterias)
        criteria_normalizer = _CriteriaNormalizer(builder)
        return criteria_normalizer.get_normalized_criterias()
    
    def test_criteria_normalizer_1(self):
        criterias = [
            {Criteria(): None},  # Not enough deep for being normal.
            {Criteria(): [
                {Criteria(): None}
            ]}
        ]
        
        normalized_criterias = self.get_normalized_criterias(criterias)
        dummy_criteria = list(normalized_criterias[0].keys())[0]
        self.assertIsInstance(dummy_criteria, DummyCriteria, "The first key in dict need to be DummyCriterias obj.")
        self.assertIsInstance(normalized_criterias[0][dummy_criteria], list, "The dummy criteria need to have one children.")
        self.assertTrue(len(normalized_criterias[0][dummy_criteria]) == 1, "DummyCriteria obj need to have only one child.")


    def test_criteria_normalizer_nested(self):
        criterias = [
            {Criteria(): [{Criteria(): [{Criteria(): None}]}]},
            {Criteria(): [
                {Criteria(): None},  # <- The parent will be DummyCriteria after normalizing.
                {Criteria(): [{Criteria(): None}]}]}
        ]
        
        normalized_criterias = self.get_normalized_criterias(criterias)
        
        # Getting nested criterias dict and than the dummy criteria obj.
        nested_dict = list(normalized_criterias[1].values())[0][0]
        dummy_criteria = list(nested_dict.keys())[0]
        
        self.assertIsInstance(dummy_criteria, DummyCriteria, "The nested criteria need to be DummyCriteria obj instance.")
        
        dummys_children = nested_dict[dummy_criteria]
        
        self.assertIsInstance(dummys_children, list, "The dummy criteria value need to be a list obj.")
        self.assertTrue(len(dummys_children) == 1, "The size of dummy's children need to be 1.")
        
    
    def test_criteria_normalizer_list_param_1(self):
        criterias = [Criteria(),
                     Criteria(children=[Criteria()])]
        
        normalized_criterias = self.get_normalized_criterias(criterias)
        dummy_criteria = list(normalized_criterias[0].keys())[0]
        self.assertIsInstance(dummy_criteria, DummyCriteria, "The first key in dict need to be DummyCriterias obj.")
        self.assertIsInstance(normalized_criterias[0][dummy_criteria], list, "The dummy criteria need to have one children.")
        self.assertTrue(len(normalized_criterias[0][dummy_criteria]) == 1, "DummyCriteria obj need to have only one child.")
        
        
    def test_criteria_normalizer_list_param_2(self):        
        criterias = [
            Criteria(children=[Criteria(children=[Criteria()])]),
            Criteria(children=[
                Criteria(),  # <- The parent will be DummyCriteria after normalizing.
                Criteria(children=[Criteria()])
            ])
        ]
        normalized_criterias = self.get_normalized_criterias(criterias)
        
        # Getting nested criterias dict and than the dummy criteria obj.
        nested_dict = list(normalized_criterias[1].values())[0][0]
        dummy_criteria = list(nested_dict.keys())[0]
        
        self.assertIsInstance(dummy_criteria, DummyCriteria, "The nested criteria need to be DummyCriteria obj instance.")
        
        dummys_children = nested_dict[dummy_criteria]
        
        self.assertIsInstance(dummys_children, list, "The dummy criteria value need to be a list obj.")
        self.assertTrue(len(dummys_children) == 1, "The size of dummy's children need to be 1.")
        
        

if __name__ == "__main__":
    unittest.main()
    