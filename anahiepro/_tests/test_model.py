import set_up_test_pathes


import unittest
import numpy as np

import unittest
from unittest.mock import Mock, patch
from anahiepro.model import Model, Problem, Criteria, Alternative

class TestModelCreation(unittest.TestCase):
    def setUp(self):
        self.problem = Problem()
        self.criterias = [Criteria(), Criteria()]
        self.alternatives = [Alternative(), Alternative()]
    

    def test_invalid_problem(self):
        with self.assertRaises(TypeError):
            Model(list(), self.criterias, self.alternatives)


    def test_invalid_alternatives(self):
        ivalid_alternatives = [dict(), list(), [Alternative(), Alternative(), Criteria()]]
        
        for invalid_avternative in ivalid_alternatives:
            with self.assertRaises(TypeError):
                Model(self.problem, self.criterias, invalid_avternative)


    def test_ivalid_criterias_another_type(self):
        with self.assertRaises(TypeError):
            Model(self.problem, dict(), self.alternatives)


    def test_ivalid_criterias_with_diff_depth(self):
        list_dict = [{Criteria("Criteria1"): [
                        {Criteria("Criteria2"): [{Criteria("Criteria7"): None}]},
                        {Criteria("Criteria3"): [{Criteria("Criteria7"): None}]}
                    ]},
                    {Criteria("Criteria5"): [
                        {Criteria("Criteria4"): None},
                        {Criteria("Criteria6"): [{Criteria("Criteria7"): None}]},
                        {Criteria("Criteria7"): [{Criteria("Criteria7"): None}]},
                        {Criteria("Criteria8"): [{Criteria("Criteria7"): None}]}
                    ]}]
        
        list_criterias = [Criteria("Criteria1", [Criteria("Criteria2"), Criteria("Criteria3")]),
                          Criteria("Criteria5", [Criteria("Criteria4"), Criteria("Criteria6", [Criteria("Criteria7")])])]

        invalide_criterias = [list_dict, list_criterias]
        
        for invalide_criteria in invalide_criterias:
            with self.assertRaises(TypeError):
                Model(self.problem, invalide_criteria, self.alternatives)


    def test_invalid_criterias_list_dict(self):
        list_dict = [{Criteria("Criteria1"): [
                        {Criteria("Criteria2"): [{Alternative("Invalid type"): None}]},
                        {Criteria("Criteria3"): [{Criteria("Criteria7"): None}]}
                    ]}]
        
        list_dict_invalid_key = [{"invalid key": None}]
        
        list_dict_invalid_value = [{Criteria("Criteria10"): []}]
        
        invalid_criterias = [list_dict_invalid_value, list_dict, list_dict_invalid_key]

        for invalid_criteria in invalid_criterias:
            with self.assertRaises(TypeError):
                self.setUp()
                Model(self.problem, invalid_criteria, self.alternatives)
        
        
    def test_model_creation_success(self):
        """Test successful creation of Model instance."""
        self.criterias = [{Criteria(): None}, {Criteria(): None}]
        model = Model(self.problem, self.criterias, self.alternatives)
        
        self.assertIsInstance(model, Model)
        self.assertEqual(model.problem, self.problem)
        self.assertEqual(model.alternatives, self.alternatives)
        self.assertEqual(model.criterias, self.criterias)

    def test_model_creation_invalid_criterias_type(self):
        """Test creation of Model with invalid criterias type."""
        invalid_criterias = "invalid_criterias"
        with self.assertRaises(TypeError):
            Model(self.problem, invalid_criterias, self.alternatives)

    def test_model_creation_invalid_criterias_structure(self):
        """Test creation of Model with invalid criterias structure."""
        invalid_criterias = ["invalid_criteria"]
        with self.assertRaises(TypeError):
            Model(self.problem, invalid_criterias, self.alternatives)

    def test_model_creation_empty_criterias(self):
        """Test creation of Model with empty criterias list."""
        empty_criterias = []
        model = Model(self.problem, empty_criterias, self.alternatives)
        self.assertIsInstance(model, Model)
        self.assertEqual(model.criterias, [], "The criterias list is not empty")

    # def test_model_creation_none_criterias(self):
    #     """Test creation of Model with None as criterias."""
    #     with self.assertRaises(TypeError):
    #         Model(self.problem, None, self.alternatives)



if __name__ == "__main__":
    unittest.main()