from anahiepro._criterias_builders._empty_criteria_builder import _EmptyCriteriaBuilder
from anahiepro._criterias_builders._list_dict_ctiteria_builder import _ListDictCriteriaBuilder
from anahiepro._criterias_builders._list_criteria_builder import _ListCriteriaBuilder
from anahiepro.nodes import Problem, Criteria, Alternative
import numpy as np



class Model:
    def __init__(self, problem: Problem, criterias: list, alternatives: list):
        self.problem = problem
        self.alternatives = alternatives
        self.criterias = self._build_criterias(criterias)

        self._build_model(criterias)
        self._build_pcm(self.problem)
    
    
    def _build_criterias(self, criterias):
        if criterias is None:
            return _EmptyCriteriaBuilder(criterias).build_criteria()
        
        if isinstance(criterias, list):
            if len(criterias) == 0:
                return _EmptyCriteriaBuilder().build_criteria()
            elif isinstance(criterias[0], dict):
                return _ListDictCriteriaBuilder(criterias).build_criteria()
            elif all(isinstance(c, Criteria) for c in criterias):
                return _ListCriteriaBuilder(criterias).build_criterias()
            
        raise TypeError("The type of criterias is invalid. It might be: 'Criteria' or 'list' of 'Criteria'.")
    
    
    def _build_model(self, criterias):
        """Build the problem hierarchy."""
        if len(criterias) == 0:
            self._build_model_witout_criterias()

        if criterias:
            self._build_model_with_criterias(criterias)


    def _build_model_witout_criterias(self):
        self._tie_alternatives(self.problem)
    

    def _build_model_with_criterias(self, criterias):
        self._tie_criterias(criterias)
        self._tie_problem(criterias)


    def _build_pcm(self, item):
        item.create_pcm()
        for child in item.children:
            self._build_pcm(child)
    
    
    def _tie_criterias(self, criterias):
        """Tie the criteria with their children and alternatives."""
        if not criterias:
            return
        
        for criteria_dict in criterias:
            for parent_criteria, criteria_list in criteria_dict.items():
                if criteria_list is None:
                    self._tie_alternatives(parent_criteria)
                else:
                    self._tie_criterias_with_parrent(parent_criteria, criteria_list)
                    self._tie_criterias(criteria_list)
    
    
    def _tie_alternatives(self, criteria):
        """Tie alternatives to the given criteria."""
        for alternative in self.alternatives:
            criteria.add_child(alternative)


    def _tie_criterias_with_parrent(self, parent_criteria, criteria_list):
        """Tie child criteria to the parent criteria."""
        for criteria_dict in criteria_list:
            for child_criteria in criteria_dict:
                parent_criteria.add_child(child_criteria)

    
    def _tie_problem(self, criterias):
        """Tie the top-level criteria to the problem."""
        for criteria_dict in criterias:
            for criteria_item in criteria_dict:
                self.problem.add_child(criteria_item)
    
    
    
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
        where.append((criteria.name, criteria._id))
    
    
    def _is_key_correct(self, key):
        CORRECT_LEN = 2
        if isinstance(key, tuple) and len(key) == CORRECT_LEN:
            if isinstance(key[0], str) and isinstance(key[1], int):
                return True
        return False


    def find_criteria(self, key: tuple):
        """Find criteria by (name, id) tuple."""
        if self._is_key_correct(key):
            return self._find_criteria(key, self.criterias)
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
    
    
    
    def attach_pcm(self, key: tuple, pcm):
        criteria = self.find_criteria(key)
        criteria.set_matrix(np.array(pcm))
    
    
    def __getitem__(self, key: tuple):
        return self.find_criteria(key)
    
    
    def solve(self):
        def calculate_global_vector(node):
            if not node.children or isinstance(node.children[0], Alternative):
                return node.get_priority_vector()

            children_global_vectors = []
            for child in node.children:
                children_global_vectors.append(calculate_global_vector(child))
            
            matrix = np.column_stack(children_global_vectors)
            parrent_vector = np.abs(node.get_priority_vector())
            global_vector = matrix.dot(parrent_vector)
            return global_vector

        return calculate_global_vector(self.problem)