import numpy as np
import anahiepro.constants as const


class PairwiseComparisonMatrix:
    def __init__(self, size):
        self.size = size
        self.matrix = np.ones((size, size))
    
    def set_comparison(self, i, j, value):
        self.matrix[i, j] = value
        self.matrix[j, i] = 1 / value
    
    def set_matrix(self, matrix):
        if self._is_valid_matrix(matrix):
            self.matrix = matrix
        else:
            raise ValueError("Matrix is not consistent or not a valid pairwise comparison matrix")
    
    def _is_valid_matrix(self, matrix):
        if matrix.shape[0] != matrix.shape[1]:
            return False
        if not np.allclose(matrix, 1 / matrix.T):
            return False
        return True
    
    def get_matrix(self):
        return self.matrix
    
    def calculate_priority_vector(self):
        (eigvals, eigvecs) = np.linalg.eig(self.matrix)
        max_eigval_index = np.argmax(eigvals)
        priority_vector = np.real(eigvecs[:, max_eigval_index])
        priority_vector = priority_vector / np.sum(priority_vector)
        return priority_vector
    
    def calculate_consistency_ratio(self):
        eigvals, _ = np.linalg.eig(self.matrix)
        max_eigval = np.max(np.real(eigvals))
        CI = (max_eigval - self.size) / (self.size - 1)
        RI = const.HOMOGENEITY_INDEXES.get(self.size, 1.49)
        return CI / RI
