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

    def test_model_creation_none_criterias(self):
        """Test creation of Model with None as criterias."""
        with self.assertRaises(TypeError):
            Model(self.problem, None, self.alternatives)



if __name__ == "__main__":
    unittest.main()