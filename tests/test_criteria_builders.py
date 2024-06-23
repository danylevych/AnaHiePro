import set_up_test_pathes

import unittest
from anahiepro.models.model import Model, Problem, Criteria, Alternative
from anahiepro._criterias_builders._wrapper_criteria_builder import _WrapperCriteriaBuilder, _EmptyCriteriaBuilder, _ListCriteriaBuilder, _ListDictCriteriaBuilder



class TestListDictCriteriaBuilder(unittest.TestCase):
    """
        the correct representation of criterias for this type of builder is next:
        [
            { Criteria() : [
                { Criteria() : None },
                ]
            },
            { Criteria() : None }
        ]
    """

    def setUp(self):
        self.correct_criterias = [
            {Criteria(): [
                {Criteria(): [{Criteria(): None}]},
                {Criteria(): [{Criteria(): None}]}
        ]},
            {Criteria(): [
                {Criteria(): [{Criteria(): None}]},
                {Criteria(): [{Criteria(): None}]},
                {Criteria(): [{Criteria(): None}]},
                {Criteria(): [{Criteria(): None}]}
            ]}
        ]

    def test_invalide_structure(self):
        invalid_structure_key = [
            {Criteria(): [
                {Criteria(): [{Criteria(): None}]},
                {Criteria(): [{Criteria(): None}]}
        ]},
            {"The key here is invalid": [
                {Criteria(): [{Criteria(): None}]},
                {Criteria(): [{Criteria(): None}]},
                {Criteria(): [{Criteria(): None}]},
                {Criteria(): [{Criteria(): None}]}
            ]}
        ]
        
        invalid_structure_not_Criteria = [ {Criteria(): [
                {Alternative(): [{Criteria(): None}]},
                {Criteria(): [{Criteria(): None}]}
        ]}]
        
        invalid_structures = [invalid_structure_key, dict(), invalid_structure_not_Criteria]
        
        for invalide_value in invalid_structures:
            with self.assertRaises(TypeError):
                _ListDictCriteriaBuilder(invalide_value)
        
        
    def test_diff_depth(self):
        criterias = [
            {Criteria(): [
                {Criteria(): [{Criteria(): None}]},
                {Criteria(): [{Criteria(): None}]}
                ]},
            {Criteria(): None}
            ]
        
        self.assertFalse(_ListDictCriteriaBuilder(criterias).has_same_depth(), "The depth must be different.")
        
        
    def test_same_depth(self):
        criterias = [
            {Criteria(): [
                {Criteria(): [{Criteria(): None}]},
                {Criteria(): [{Criteria(): None}]}
                ]},
            {Criteria(): [{Criteria(): [{Criteria(): None }]}]}
            ]
        
        self.assertTrue(_ListDictCriteriaBuilder(criterias).has_same_depth(), "The depth must be the same.")


    def test_build_with_diff_depth(self):
        criterias = [
            {Criteria(): [
                {Criteria(): [{Criteria(): None}]},
                {Criteria(): [{Criteria(): None}]}
                ]},
            {Criteria(): None}
            ]
        
        with self.assertRaises(TypeError):
            _ListDictCriteriaBuilder(criterias).build_criteria()
            
    
    def test_build_with_same_depth(self):
        self.assertListEqual(_ListDictCriteriaBuilder(self.correct_criterias).build_criteria(), self.correct_criterias, 
                             "The expected values and actual values are different.")
     
        

class TestListCriteriaBuilder(unittest.TestCase):
    def test_build_empty(self):
        builder = _ListCriteriaBuilder([])
        self.assertFalse(builder.has_same_depth(), "The depth of empty need to be diff.")
        with self.assertRaises(TypeError):
            builder.build_criteria()
    
    
    def test_build_with_one_element(self):
        same_criteria = Criteria()
        builder = _ListCriteriaBuilder([same_criteria])
        self.assertTrue(builder.has_same_depth(), "The depth of one element need to be True.")


    def test_build_with_invalid_list(self):
        with self.assertRaises(TypeError):
            _ListCriteriaBuilder([Criteria(), Criteria(), "invalid"]).build_criteria()


    def test_build_valid(self):
        child1 = Criteria()
        child2 = Criteria()
        criteria = Criteria(children=[child1, child2])
        
        expected_structure = [
            {criteria: [
                {child1 : None},
                {child2 : None},
                ]}
        ]
        
        builder = _ListCriteriaBuilder([criteria])

        self.assertTrue(builder.has_same_depth(), "The depth need to be the True.")
        self.assertTrue(_ListDictCriteriaBuilder([{Criteria(): None}])._is_valid_structure(builder.build_criteria()), 
                        "The actual value & expected are not the same.")
        
        self.assertTrue(len(child1._parents) != 0, "The link sould not be cleared.")
        self.assertTrue(len(child2._parents) != 0, "The link sould not be cleared.")
        self.assertTrue(len(criteria._children) != 0, "The link sould not be cleared.")



class TestWrapperCriteriaBuilder(unittest.TestCase):
    def test_builder_as_empty_builder(self):
        examples = [list(), None]
        for example in examples:
            builder = _WrapperCriteriaBuilder(example)
            self.assertIsInstance(builder._builder, _EmptyCriteriaBuilder, "The _builder have to be _EmptyCriteriaBuilder instance.")
            criterias = builder.build_criterias()
            self.assertIsInstance(criterias, list, "The build method have to return an insatnce of list.")
            self.assertTrue(len(criterias) == 0, "The criterias need to be an empty list.")

    
    def test_builder_as_list_builder(self):
        examples = [[Criteria()], [Criteria(children=[Criteria(), Criteria()])]]
        
        for example in examples:
            builder = _WrapperCriteriaBuilder(example)
            self.assertIsInstance(builder._builder, _ListCriteriaBuilder, "The _builder have to be _ListCriteriaBuilder instance.")
            criterias = builder.build_criterias()
            self.assertTrue(_ListDictCriteriaBuilder([{Criteria(): None}])._is_valid_structure(criterias), "The structure of the criterias is not valid.")
            
    
    def test_builder_as_list_dict_builder(self):
        examples = [
                [{Criteria(): None}],
                [{Criteria(): [{Criteria(): None}]},
                 {Criteria(): [{Criteria(): None}]}]
            ]
        
        for example in examples:
            builder = _WrapperCriteriaBuilder(example)
            self.assertIsInstance(builder._builder, _ListDictCriteriaBuilder, "The _builder have to be _ListDictCriteriaBuilder instance.")
            
    
    def test_with_invalid_examples(self):
        examples = [
            dict(),
            set(),
            tuple()
        ]
        
        for example in examples:
            with self.assertRaises(TypeError):
                _WrapperCriteriaBuilder(example)
            


if __name__ == "__main__":
    unittest.main()