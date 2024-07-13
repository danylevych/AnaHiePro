from anahiepro.models._criterias_builders._wrapper_criteria_builder import _WrapperCriteriaBuilder
from anahiepro.nodes import Problem, Criteria, Alternative
from anahiepro.models._model_builder import _ModelBuilder
import numpy as np


class Model:
    def __init__(self, problem: Problem, criterias, alternatives: list):
        """
        Initialize the model with a problem, criteria, and alternatives.
        
        Parameters
        ----------
        problem : Problem
            The problem instance.
        criterias : object
            The criteria for the model.
        alternatives : list
            A list of alternatives.
        
        Raises
        ------
        TypeError
            If the problem is not an instance of Problem or if the alternatives are not a list of Alternatives.
        """
        self.problem = self._validate_problem(problem)
        self.alternatives = self._validate_alternatives(alternatives)
        self.criterias = _WrapperCriteriaBuilder(criterias).build_criterias()
        
        builder = _ModelBuilder(self.problem, self.criterias, self.alternatives)
        builder.build()
    
    
    def _validate_problem(self, problem):
        """
        Validate the problem instance.
        
        Parameters
        ----------
        problem : Problem
            The problem instance to validate.
        
        Returns
        -------
        Problem
            The validated problem instance.
        
        Raises
        ------
        TypeError
            If the problem is not an instance of Problem.
        """
        if not isinstance(problem, Problem):
            raise TypeError("Invalid problem type. Expected instance of Problem.")
        return problem
    

    def _validate_alternatives(self, alternatives):
        """
        Validate the list of alternatives.
        
        Parameters
        ----------
        alternatives : list
            The list of alternatives to validate.
        
        Returns
        -------
        list
            The validated list of alternatives.
        
        Raises
        ------
        TypeError
            If alternatives are not a list, if the list is empty, or if any item is not an instance of Alternative.
        """
        if not isinstance(alternatives, list):
            raise TypeError("Alternatives should be a list.")
        if len(alternatives) == 0:
            raise TypeError("Alternatives cannot be empty.")
        if not all(isinstance(alternative, Alternative) for alternative in alternatives):
            raise TypeError("All items in alternatives should be instances of Alternative.")
        return alternatives


    def get_problem(self):
        """
        Return the problem instance.
        
        Returns
        -------
        Problem
            The problem instance.
        """
        return self.problem
    
    
    def get_alternatives(self):
        """
        Return the list of alternatives.
        
        Returns
        -------
        list
            The list of alternatives.
        """
        return self.alternatives
    
    
    def get_criterias_name_ids(self):
        """
        Get the names and IDs of the criteria.
        
        Returns
        -------
        tuple
            A tuple of criteria names and IDs.
        """
        return tuple(self._get_around_and_collect_name_ids(self.criterias))
    
    
    def _get_around_and_collect_name_ids(self, criterias):
        """
        Collect the names and IDs of the criteria recursively.
        
        Parameters
        ----------
        criterias : list
            The list of criteria to collect names and IDs from.
        
        Returns
        -------
        list
            A list of criteria names and IDs.
        """
        criterias_name_ids = []
        
        for criteria_dict in criterias:
            for parent_criteria, criteria_list in criteria_dict.items():
                self._add_criteria_name_id(criterias_name_ids, parent_criteria)
                if criteria_list and not self._is_list_empty_or_has_instance_of_Alternative(criteria_list):
                    criterias_name_ids.extend(self._get_around_and_collect_name_ids(criteria_list))
        
        return criterias_name_ids
    
    
    
    def _is_list_empty_or_has_instance_of_Alternative(self, what):
        """
        Check if the list is empty or contains instances of Alternative.
        
        Parameters
        ----------
        what : list
            The list to check.
        
        Returns
        -------
        bool
            True if the list is empty or contains instances of Alternative, False otherwise.
        """
        return what is None or (isinstance(what, list) and len(what) > 0 and isinstance(what[0], Alternative))
    
    
    def _add_criteria_name_id(self, where: list, criteria: Criteria):
        """
        Add the criteria name and ID to the specified list.
        
        Parameters
        ----------
        where : list
            The list to add the criteria name and ID to.
        criteria : Criteria
            The criteria to add.
        """
        where.append((criteria._name, criteria._id))
    
    
    def _is_key_correct(self, key):
        """
        Check if the key is a valid (name, id) tuple.
        
        Parameters
        ----------
        key : tuple
            The key to check.
        
        Returns
        -------
        bool
            True if the key is valid, False otherwise.
        """
        CORRECT_LEN = 2
        if isinstance(key, tuple) and len(key) == CORRECT_LEN:
            if isinstance(key[0], str) and isinstance(key[1], int):
                return True
        return False


    def find_criteria(self, key: tuple):
        """
        Find criteria by (name, id) tuple.
        
        Parameters
        ----------
        key : tuple
            The (name, id) tuple of the criteria to find.
        
        Returns
        -------
        Criteria
            The found criteria.
        
        Raises
        ------
        KeyError
            If the key is not valid.
        ValueError
            If the criteria is not found.
        """
        if self._is_key_correct(key):
            criteria = self._find_criteria(key, self.criterias)
            if criteria is None:
                raise ValueError(f"The Criteria with key ({key[0]}, {key[1]}) not found.")
            return criteria
        else:
            raise KeyError
    
    
    def _find_criteria(self, key: tuple, criterias):
        """
        Recursive method to find criteria.
        
        Parameters
        ----------
        key : tuple
            The (name, id) tuple of the criteria to find.
        criterias : list
            The list of criteria to search in.
        
        Returns
        -------
        Criteria
            The found criteria, or None if not found.
        """
        for criteria_dict in criterias:
            for parent_criteria, criteria_list in criteria_dict.items():
                if parent_criteria.compare(key):
                    return parent_criteria
                
                if criteria_list is not None:
                    found_criteria = self._find_criteria(key, criteria_list)
                    if found_criteria is not None:
                        return found_criteria
        return None
    
    
    
    def attach_criteria_pcm(self, key: tuple, pcm):
        """
        Attach a pairwise comparison matrix to the criteria identified by the key.
        
        Parameters
        ----------
        key : tuple
            The (name, id) tuple of the criteria.
        pcm : array_like
            The pairwise comparison matrix to attach.
        """
        criteria = self.find_criteria(key)
        criteria.set_matrix(np.array(pcm))
    
    
    def __getitem__(self, key: tuple):
        """
        Get the criteria identified by the key.
        
        Parameters
        ----------
        key : tuple
            The (name, id) tuple of the criteria.
        
        Returns
        -------
        Criteria
            The found criteria.
        """
        return self.find_criteria(key)
    
    
    def solve(self, showAlternatives=False):
        """
        Solve the model to calculate the global priority vector.
        
        Parameters
        ----------
        showAlternatives : bool, optional
            Whether to show alternatives in the output, by default False.
        
        Returns
        -------
        numpy.ndarray or list
            The global priority vector, or a list of (alternative, value) tuples if showAlternatives is True.
        """
        def calculate_global_vector(node):
            if not node._children or isinstance(node._children[0], Alternative):
                return node.get_priority_vector()

            children_global_vectors = []
            for child in node._children:
                children_global_vectors.append(calculate_global_vector(child))
            
            matrix = np.column_stack(children_global_vectors)
            parrent_vector = np.abs(node.get_priority_vector())
            global_vector = matrix.dot(parrent_vector)
            return global_vector

        global_vector = calculate_global_vector(self.problem)
        
        if showAlternatives:
            return [(alternative, value) for (alternative, value) in zip(self.alternatives, global_vector)]
        
        return global_vector
    
    
    def show(self):
        """
        Display the problem.
        
        Returns
        -------
        object
            The problem display output.
        """
        return self.problem.show()
