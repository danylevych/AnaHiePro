import set_up_test_pathes

import unittest
import numpy as np
from anahiepro.nodes import Problem, Criteria, Alternative



class TestProblem(unittest.TestCase):

    def setUp(self):
        Problem._problem_id = 0
        self.problems = [Problem() for _ in range(5)]
        Problem._problem_id = 0


    def test_init_without_name(self):
        problems = [Problem() for _ in range(10)]

        for index, problem in enumerate(problems, start=0):
            self.assertEqual(problem.get_key(), ("Problem"+str(index), index), "The problem has unexpected name or id")

    
    def test_init_with_name(self):
        name = "Example Problem"
        problem = Problem(name=name)

        self.assertTrue(problem.get_key() == (name, 0))
    

    def test_add_invalid_child(self):
        parrent_problem = Problem()
        child_problem = Problem()

        with self.assertRaises(TypeError):
            parrent_problem.add_child(child_problem)


    def test_add_valid_child(self):
        parrent_problem = Problem()
        children = [Criteria() for _ in range(5)]

        for child in children:
            parrent_problem.add_child(child)
        
        self.assertListEqual(parrent_problem._children, children, "The children in the problem do not equal expected")


    def test_invalid_compare(self):
        key = ("Problem6", 6)

        for problem in self.problems:
            self.assertFalse(problem.compare(key), "The key was unexpected")

    def test_invalid_compare(self):
        key = ("Problem0", 0)

        has_key = False
        for problem in self.problems:
            if problem.compare(key):
                has_key = True
        
        if not has_key:
            self.assertTrue(False, "No problem with the expected key")

    
    def test_create_empty_pcm(self):
        problem = Problem()

        self.assertIsInstance(problem.get_pcm(), np.ndarray, "The pcm must be instance of np.ndarray")
        self.assertTrue(problem.get_pcm().shape == (0, 0), "The dimension of empty matrix is not correct")
        
        for child in [Criteria() for _ in range(4)]:
            problem.add_child(child)
        
        problem.create_pcm()
        self.assertTrue(problem.get_pcm().shape == (4, 4), "The dimension of matrix is not correct")
    


class TestCriteria(unittest.TestCase):
    def setUp(self):
        Criteria._criteria_id = 0
        self.criteria = Criteria()
        Criteria._criteria_id = 0


    def test_init_without_name(self):
        criterias = [Criteria() for _ in range(10)]

        for index, criteria in enumerate(criterias, start=0):
            self.assertEqual(criteria.get_key(), ("Criteria"+str(index), index), "The criteria has unexpected name or id")

    
    def test_init_with_name(self):
        name = "Example Criteria"
        criteria = Criteria(name=name)

        self.assertTrue(criteria.get_key() == (name, 0))
    

    def test_add_Problem_as_child(self):
        problem = Problem()

        with self.assertRaises(TypeError):
            self.criteria.add_child(problem)
    

    def test_add_valid_children(self):
        children = [Criteria() for _ in range(5)]
        children.extend([Alternative() for _ in range(5)])

        try:
            for child in children:
                self.criteria.add_child(child)
        except TypeError:
            self.assertFalse(True, "The criteria do not store some instance as a child")
    
    # The next test is not writen because in the past one we check also mhetods that are in all classes.



class TestAlternative(unittest.TestCase):
    def setUp(self):
        Alternative._alternative_id = 0
        self.alternative = Alternative()
        Alternative._alternative_id = 0


    def test_init_without_name(self):
        alternatives = [Alternative() for _ in range(10)]

        for index, alternative in enumerate(alternatives, start=0):
            self.assertEqual(alternative.get_key(), ("Alternative"+str(index), index), "The alternative has unexpected name or id")

    
    def test_init_with_name(self):
        name = "Example Alternative"
        alternative = Alternative(name=name)

        self.assertTrue(alternative.get_key() == (name, 0))


    def test_access_to_pcm_attribute(self):
        with self.assertRaises(AttributeError):
            self.alternative.pcm
        
    
    def test_add_child(self):
        with self.assertRaises(NotImplementedError):
            self.alternative.add_child(Criteria())

    
    def test_set_matrix(self):
        with self.assertRaises(NotImplementedError):
            self.alternative.set_matrix(np.ones((3, 3)))

    
    def test_set_comparison(self):
        with self.assertRaises(NotImplementedError):
            self.alternative.set_comparison(1, 1, 10)



if __name__ == "__main__":
    unittest.main()