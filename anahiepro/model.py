from anahiepro._criterias_builders._wrapper_criteria_builder import _WrapperCriteriaBuilder
from anahiepro.nodes import Problem, Criteria, Alternative
from anahiepro._model_builder import _ModelBuilder
import numpy as np



class Model:
    def __init__(self, problem: Problem, criterias, alternatives: list):
        self.problem = self._validate_problem(problem)
        self.alternatives = self._validate_alternatives(alternatives)
        self.criterias = _WrapperCriteriaBuilder(criterias).build_criterias()
        
        builder = _ModelBuilder(self.problem, self.criterias, self.alternatives)
        builder.build()
    
    
    def _validate_problem(self, problem):
        if not isinstance(problem, Problem):
            raise TypeError("Invalid problem type. Expected instance of Problem.")
        return problem
    

    def _validate_alternatives(self, alternatives):
        if not isinstance(alternatives, list):
            raise TypeError("Alternatives should be a list.")
        if len(alternatives) == 0:
            raise TypeError("Alternatives can not be empty.")
        if not all(isinstance(alternative, Alternative) for alternative in alternatives):
            raise TypeError("All items in alternatives should be instances of Alternative.")
        return alternatives


    def get_problem(self):
        """Return the problem instance."""
        return self.problem
    
    
    def get_alternatives(self):
        return self.alternatives
    
    
    def get_criterias_name_ids(self):
        return tuple(self._get_around_and_collect_name_ids(self.criterias))
    
    
    def _get_around_and_collect_name_ids(self, criterias):
        criterias_name_ids = []
        
        for criteria_dict in criterias:
            for parent_criteria, criteria_list in criteria_dict.items():
                self._add_criteria_name_id(criterias_name_ids, parent_criteria)
                if criteria_list and not self._is_list_empty_or_has_instance_of_Alternative(criteria_list):
                    criterias_name_ids.extend(self._get_around_and_collect_name_ids(criteria_list))
        
        return criterias_name_ids
    
    
    
    def _is_list_empty_or_has_instance_of_Alternative(self, what):
        return what is None or (isinstance(what, list) and len(what) > 0 and isinstance(what[0], Alternative))
    
    
    def _add_criteria_name_id(self, where: list, criteria: Criteria):
        where.append((criteria._name, criteria._id))
    
    
    def _is_key_correct(self, key):
        CORRECT_LEN = 2
        if isinstance(key, tuple) and len(key) == CORRECT_LEN:
            if isinstance(key[0], str) and isinstance(key[1], int):
                return True
        return False


    def find_criteria(self, key: tuple):
        """Find criteria by (name, id) tuple."""
        if self._is_key_correct(key):
            criteria = self._find_criteria(key, self.criterias)
            if criteria is None:
                raise ValueError(f"The Criteria with key ({key[0]}, {key[1]}) not found.")
            return criteria
        else:
            raise KeyError
    
    
    def _find_criteria(self, key: tuple, criterias):
        """Recursive method to find criteria."""
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
        criteria = self.find_criteria(key)
        criteria.set_matrix(np.array(pcm))
    
    
    def __getitem__(self, key: tuple):
        return self.find_criteria(key)
    
    
    def solve(self):
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

        return calculate_global_vector(self.problem)
    
    
    def show(self):
        return self.problem.show()