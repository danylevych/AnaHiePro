import numpy as np
import anahiepro.constants as const


"""
    PairwiseComparisonMatrix represents the the pairwise comparison matrix
"""
class PairwiseComparisonMatrix:
    def __init__(self, size=0, matrix=None):
        """
        Initialize a pairwise comparison matrix with the given size.
        
        Parameters
        ----------
        size : int
            The size of the matrix.
        """
        self.size = size
        self.matrix = np.ones((size, size))
        if matrix:
            self._try_to_set_matrix(np.array(matrix))
    

    def set_comparison(self, i, j, value):
        """
        Set the comparison value for the given indices.
        
        Parameters
        ----------
        i : int
            Row index.
        j : int
            Column index.
        value : float
            The value to set at (i, j) and its reciprocal at (j, i).
        """
        self._try_to_set_comparison(i, j, value)
    

    def _try_to_set_comparison(self, i, j, value):
        """
        Attempt to set the comparison value, ensuring consistency for the diagonal.
        
        Parameters
        ----------
        i : int
            Row index.
        j : int
            Column index.
        value : float
            The value to set at (i, j) and its reciprocal at (j, i).
        
        Raises
        ------
        ValueError
            If trying to set a non-1 value on the diagonal.
        """
        if self._is_diagonal_item(i, j) and value != 1:
            raise ValueError("The element in diagonal of matrix must be 1")
        
        self.matrix[i, j] = value
        self.matrix[j, i] = 1 / value


    def _is_diagonal_item(self, i, j):
        """
        Check if the given indices correspond to a diagonal element.
        
        Parameters
        ----------
        i : int
            Row index.
        j : int
            Column index.
        
        Returns
        -------
        bool
            True if the indices correspond to a diagonal element, False otherwise.
        """
        return i == j


    def set_matrix(self, matrix):
        """
        Set the entire matrix, ensuring it is a valid pairwise comparison matrix.
        
        Parameters
        ----------
        matrix : array_like
            The matrix to set.
        
        Raises
        ------
        ValueError
            If the matrix is not consistent or not valid.
        """
        self._try_to_set_matrix(np.array(matrix))
    

    def _try_to_set_matrix(self, matrix):
        """
        Attempt to set the matrix, checking for validity.
        
        Parameters
        ----------
        matrix : numpy.ndarray
            The matrix to set.
        
        Raises
        ------
        ValueError
            If the matrix is not consistent or not valid.
        """
        if self._is_valid_matrix(matrix):
            self.size = matrix.shape[0]
            self.matrix = matrix
        else:
            raise ValueError("Matrix is not consistent or not a valid pairwise comparison matrix")
    

    def _is_valid_matrix(self, matrix):
        """
        Check if the given matrix is a valid pairwise comparison matrix.
        
        Parameters
        ----------
        matrix : numpy.ndarray
            The matrix to check.
        
        Returns
        -------
        bool
            True if the matrix is valid, False otherwise.
        """
        if matrix.shape[0] != matrix.shape[1]:
            return False
        if not np.allclose(matrix, 1 / matrix.T):
            return False
        
        for i in range(matrix.shape[0]):
            if int(matrix[i][i]) != 1:  # cast to int, because floating comparing can have a bad accuracy.
                return False

        return True
    

    def get_matrix(self):
        """
        Get the current pairwise comparison matrix.
        
        Returns
        -------
        numpy.ndarray
            The current matrix.
        """
        return self.matrix
    

    def calculate_priority_vector(self):
        """
        Calculate the priority vector from the pairwise comparison matrix.
        
        Returns
        -------
        numpy.ndarray
            The priority vector.
        """
        (eigvals, eigvecs) = np.linalg.eig(self.matrix)
        max_eigval_index = np.argmax(eigvals)
        priority_vector = np.real(eigvecs[:, max_eigval_index])
        return priority_vector
    

    def calculate_consistency_ratio(self):
        """
        Calculate the consistency ratio of the pairwise comparison matrix.
        
        Returns
        -------
        float
            The consistency ratio.
        """
        eigvals, _ = np.linalg.eig(self.matrix)
        max_eigval = np.max(np.real(eigvals))
        CI = np.divide((max_eigval - self.size), (self.size - 1))
        RI = const.HOMOGENEITY_INDEXES.get(self.size, 1.49)
        return np.divide(CI, RI)


    def __getitem__(self, key):
        """
        Get the value at the specified index in the matrix.
        
        Parameters
        ----------
        key : tuple of int
            The index in the format (row, column).
        
        Returns
        -------
        float
            The value at the specified index.
        """
        return self.matrix[key]
    
    
    def __setitem__(self, key, value):
        """
        Set the value at the specified index in the matrix.
        
        Parameters
        ----------
        key : tuple of int
            The index in the format (row, column).
        value : float
            The value to set at the specified index.
        """
        (i, j) = key
        self._try_to_set_comparison(i, j, value)
