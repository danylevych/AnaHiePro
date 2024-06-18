import set_up_test_pathes

import unittest
import numpy as np
from anahiepro.model import Model, Problem, Criteria, Alternative



def load_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            values = line.replace('\n', '').split()
            inner_array = []
            for value in values:
                if '/' in value:
                    fruction = value.split('/')
                    inner_array.append(float(fruction[0])/float(fruction[1]))
                else:
                    inner_array.append(float(value))
            data.append(inner_array)
    return np.array(data)



class TestModelCreation(unittest.TestCase):
    def setUp(self):
        Problem._problem_id = 0
        Criteria._criteria_id = 0
        Alternative._alternative_id = 0
        
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


    def test_model_creation_success_list(self):
        self.criterias = [Criteria(children=[Criteria()]), Criteria(children=[Criteria()])]
        model = Model(self.problem, self.criterias, self.alternatives)
        
        self.assertEqual(model.problem, self.problem)
        self.assertEqual(model.alternatives, self.alternatives)
        self.assertIsInstance(model.criterias, list, "The criterias in instance have to be list obj.")
        CORRECT_PARENT_NUM = 2
        for alternative in model.alternatives:
            self.assertEqual(len(alternative._parents), CORRECT_PARENT_NUM, "The number of alternative's parents is wrong.")
        
        CORRECT_CHILDREN_NUM = 2
        self.assertEqual(len(model.get_problem().get_children()), CORRECT_CHILDREN_NUM, "The number of parent's children is wrong.")
        
        
        
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

    

class TestModelFunctionality(unittest.TestCase):
    def setUp(self):
        Problem._problem_id = 0
        Criteria._criteria_id = 0
        Alternative._alternative_id = 0
        
        self.problem = Problem()

        self.criterias = [
            {Criteria(): [
                {Criteria(): None},
                {Criteria(): None},
                {Criteria(): None}
            ]},    
            {Criteria(): [
                {Criteria(): None},
                {Criteria(): None},
                {Criteria(): None}
            ]}
        ]

        self.alternatives = [Alternative(), Alternative(), Alternative()]

        self.model = Model(self.problem, self.criterias, self.alternatives)
    
    
    def test_get_problem(self):
        self.assertIsInstance(self.model.get_problem(), Problem, "The problem must be an instance of Problem.")
        
    
    def test_get_alternaives(self):
        alternatives = self.model.get_alternatives()
        self.assertIsInstance(alternatives, list, "get_alternatives have to return an instance of list.")
        
        CORRECT_PARENT_NUM = 6
        for alternative in alternatives:
            self.assertIsInstance(alternative, Alternative)
            self.assertEqual(len(alternative._parents), CORRECT_PARENT_NUM, f"The number of alternative's parrent must be {CORRECT_PARENT_NUM}.")
    
    
    def test_find_criteria(self):
        name = "Criteria"
        
        for index in range(8):
            criteria = self.model.find_criteria((name + str(index), index))
            self.assertIsInstance(criteria, Criteria, "Found criteria is not an instance of Criteria class.")


    def test_find_criteria_invalid_key(self):
        invalid_keys = [["Criteria10", 10], list(), dict(), ("Criteria0", 0, "invalid key")]
        
        for invalid_key in invalid_keys:
            with self.assertRaises(KeyError):
                self.model.find_criteria(invalid_key)

    
    def test_find_criteria_key_does_not_exixt(self):
        key_not_exist = ("Criteria10000", 10000)
        
        with self.assertRaises(ValueError):
            self.model.find_criteria(key_not_exist)
        
    
    def test_get_criterias_name_ids(self):
        expected_name_ids = [("Criteria"+str(index), index) for index in range(8)]
        actual_name_ids = list(self.model.get_criterias_name_ids())
        
        self.assertListEqual(expected_name_ids, actual_name_ids)

    
    def test_set_pcms(self):
        two_2_two = np.ones((2, 2))
        three_2_three = np.ones((3, 3))
        
        self.model.get_problem().set_matrix(two_2_two)
        
        name_ids = self.model.get_criterias_name_ids()
        for key in name_ids:
            self.model[key].set_matrix(three_2_three)
            
        self.assertEqual(self.model.get_problem().pcm.matrix.shape, (2, 2))
        
        for key in name_ids:
            self.assertEqual(self.model[key].pcm.matrix.shape, (3, 3)) 



class TestModelSolve(unittest.TestCase):
    def setUp(self):
        Problem._problem_id = 0
        Criteria._criteria_id = 0
        Alternative._alternative_id = 0
        
    
    def test_solve_1(self):
        problem = Problem("Choose TV")
        
        criterias = [
            {Criteria("Product attract"): [
                {Criteria("Price"): None},
                {Criteria("Reviews"): None}]},
            {Criteria("Characteristics"): [
                {Criteria("Screen"): None},
                {Criteria("Functionality"): None},
                {Criteria('System parameters'): None},
                {Criteria("Physical params"): None}
            ]}
        ]
        
        alternatives = [
            Alternative("Samsung UE50AU7100UXUA"),
            Alternative("LG 55UP77006LB"),
            Alternative("Samsung QE50Q60AAUXUA"),
            Alternative("Samsung UE32T5300AUXUA"),
            Alternative("Kivi 40F500LB"),
        ]
        
        model = Model(problem, criterias, alternatives)
        path = "/home/danylevych/Desktop/Projects/AnaHiePro/tests/data"
        model.problem.set_matrix(load_data(path + "/problem_data.txt"))
        
        criterias_key = model.get_criterias_name_ids()
        for key in criterias_key:
            file_path = path + '/' + key[0] + '.txt'
            model.attach_criteria_pcm(key, load_data(file_path))
        
        result = model.solve()
        expected = np.array([0.483, 0.663, 0.34, 0.972, 0.495])
        np.testing.assert_array_almost_equal(result, expected, decimal=2)


if __name__ == "__main__":
    unittest.main()