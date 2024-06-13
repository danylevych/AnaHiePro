import numpy as np
import anahiepro.constants as const


"""
    PairwiseComparisonMatrix represents the the pairwise comparison matrix
"""
class PairwiseComparisonMatrix:
    def __init__(self, size):
        self.size = size
        self.matrix = np.ones((size, size))
    

    def set_comparison(self, i, j, value):
        self._try_to_set_comparison(i, j, value)
    

    def _try_to_set_comparison(self, i, j, value):
        if self._is_diagonal_item(i, j) and value != 1:
            raise ValueError("The element in diagonal of matrix must be 1")
        
        self.matrix[i, j] = value
        self.matrix[j, i] = 1 / value


    def _is_diagonal_item(self, i, j):
        return i == j


    def set_matrix(self, matrix):
        self._try_to_set_matrix(np.array(matrix))
    

    def _try_to_set_matrix(self, matrix):
        if self._is_valid_matrix(matrix):
            self.size = matrix.shape[0]
            self.matrix = np.array(matrix)
        else:
            raise ValueError("Matrix is not consistent or not a valid pairwise comparison matrix")
    

    def _is_valid_matrix(self, matrix):
        if matrix.shape[0] != matrix.shape[1]:
            return False
        if not np.allclose(matrix, 1 / matrix.T):
            return False
        
        for i in range(matrix.shape[0]):
            if matrix[i][i] != 1:
                return False

        return True
    

    def get_matrix(self):
        return self.matrix
    

    def calculate_priority_vector(self):
        (eigvals, eigvecs) = np.linalg.eig(self.matrix)
        max_eigval_index = np.argmax(eigvals)
        priority_vector = np.real(eigvecs[:, max_eigval_index])
        return priority_vector
    

    def calculate_consistency_ratio(self):
        eigvals, _ = np.linalg.eig(self.matrix)
        max_eigval = np.max(np.real(eigvals))
        CI = np.divide((max_eigval - self.size), (self.size - 1))
        RI = const.HOMOGENEITY_INDEXES.get(self.size, 1.49)
        return np.divide(CI, RI)


    def __getitem__(self, key):
        return self.matrix[key]
    
    
    def __setitem__(self, key, value):
        (i, j) = key
        self._try_to_set_comparison(i, j, value)