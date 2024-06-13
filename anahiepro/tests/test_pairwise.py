import set_up_test_pathes

import unittest
import numpy as np
from anahiepro.pairwise import PairwiseComparisonMatrix
import anahiepro.constants as const



class TestPairwiseMatrix(unittest.TestCase):
    def setUp(self):
        self.matrix_size = 3
        self.pcm = PairwiseComparisonMatrix(self.matrix_size)


    def test_initial_matrix(self):
        expected_matrix = np.ones((self.matrix_size, self.matrix_size))
        np.testing.assert_array_equal(self.pcm.get_matrix(), expected_matrix, err_msg="Coeficients durring initializing the matrix are not 1")


    def test_set_comparison(self):
        self.pcm.set_comparison(0, 1, 3)
        expected_matrix = np.array([
            [1, 3, 1],
            [1/3, 1, 1],
            [1, 1, 1]
        ])
        np.testing.assert_array_almost_equal(self.pcm.get_matrix(), expected_matrix, err_msg="The commparison don't work well")



    def test_set_diagonal_value_not_to_1(self):
        with self.assertRaises(ValueError):
            self.pcm.set_comparison(1, 1, 5)  # Set 5 to the item in the main diagonal of the matrix. 


    def test_set_invalid_diagonal_due_setitem(self):
        with self.assertRaises(ValueError):
            self.pcm[1, 1] = 5


    def test_set_diagonal_value_to_1(self):
        expected_value = 1
        self.pcm.set_comparison(1, 1, 1)  # Set the 1 in diagonal.
        self.assertEqual(self.pcm[1][1], expected_value, "The value in main diagonal item is not 1")


    def test_set_invalid_matrix(self):
        invalid_matrix = np.array([
            [1,   3],
            [0.5, 1]
        ])
        with self.assertRaises(ValueError):
            self.pcm.set_matrix(invalid_matrix)


    def test_set_matrix_with_invalid_diagonal(self):
        invalid_matrix = np.array([
            [1,   2,   3],
            [0.5, 7,   2],  # Here is 7 in the main diagonal, this is not allow. 
            [1/3, 0.5, 1]
        ])
        with self.assertRaises(ValueError):
            self.pcm.set_matrix(invalid_matrix)
    

    def test_set_matrix_with_invalid_demesion(self):
        invalid_matrix = np.array([
            [1,   2,   3],
            [0.5, 7,   2]
        ])
        with self.assertRaises(ValueError):
            self.pcm.set_matrix(invalid_matrix)


    def test_set_valid_matrix(self):
        valid_matrix = np.array([
            [1, 3, 1/2],
            [1/3, 1, 1/4],
            [2, 4, 1]
        ])

        right_size = valid_matrix.shape[0]

        self.pcm.set_matrix(valid_matrix)
        np.testing.assert_array_almost_equal(self.pcm.get_matrix(), valid_matrix, err_msg="The matrixes are not equal")
        self.assertTrue(right_size == self.pcm.size, "The size of pcm is not equal expected size")


    def test_set_zero_matrix(self):
        matrix = np.zeros((3, 3))

        with self.assertRaises(ValueError):
            self.pcm.set_matrix(matrix)


    def test_type_of_matrix(self):
        matrixes = [np.ones((3, 3)), [[1, 1, 1] for _ in range(3)], [tuple([1, 1, 1]) for _ in range(3)]]

        for matrix in matrixes:
            self.pcm.set_matrix(matrix)
            self.assertIsInstance(self.pcm.matrix, np.ndarray, "The matrix is not np.array object")

    def test_calculate_priority_vector(self):
        self.pcm.set_comparison(0, 1, 3)
        self.pcm.set_comparison(0, 2, 1/2)
        self.pcm.set_comparison(1, 2, 1/4)
        priority_vector = self.pcm.calculate_priority_vector()
        
        expected_priority_vector = np.array([0.48805649, 0.1862284, 0.85271323])
        self.assertTrue(np.allclose(priority_vector, expected_priority_vector, atol=1e-6), "Culculated priority vector is not equal expected priority vector")


    def test_calculate_consistency_ratio(self):
        self.pcm.set_comparison(0, 1, 3)
        self.pcm.set_comparison(0, 2, 1/2)
        self.pcm.set_comparison(1, 2, 1/4)
        consistency_ratio = self.pcm.calculate_consistency_ratio()
        expected_consistency_ratio = 0.01577129938761093
        self.assertAlmostEqual(consistency_ratio, expected_consistency_ratio, places=3,
                               msg=f'Calculated consistency ratio {consistency_ratio} is not equal expected one {expected_consistency_ratio}')


    def test_calculate_consistency_ratio_for_2d_matrix(self):
        matrix = np.array([[1,   2],
                           [0.5, 1]])
        
        self.pcm.set_matrix(matrix)
        self.assertTrue(np.isnan(self.pcm.calculate_consistency_ratio()), "Consistency ratio have to be nan")


if __name__ == '__main__':
    unittest.main()
