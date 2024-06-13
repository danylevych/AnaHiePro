from anahiepro.nodes import Problem, Criteria, Alternative
import numpy as np



class Model:
    def __init__(self, problem: Problem, criterias: list, alternatives: list):
        self.problem = problem
        self.alternatives = alternatives
        self.criterias = self._build_criterias(criterias)
        self._build_problem(criterias)
        self._build_pcm(self.problem)
    
    
    def _build_criterias(self, criterias):
        # TODO: Add more flexability to creating the criterias.
        if isinstance(criterias, list):
            return self._build_criterias_from_list(criterias)
        
        raise TypeError("The type of criterias is invalid. It might be: 'Criteria' or 'list' of 'Criteria'.")
    
    
    def _build_criterias_from_list(self, criterias):
        if self._is_valid_structure(criterias):
            return criterias
        raise TypeError("The list of criterias has an invalid type.")
    
    
    def _is_valid_structure(self, obj):
        if not isinstance(obj, list):
            return False

        for item in obj:
            if not isinstance(item, dict):
                return False
            for key, value in item.items():
                if not isinstance(key, Criteria):
                    return False
                if value is not None:
                    if not self._is_valid_structure(value):
                        return False
        return True
    
    
    
    def _build_problem(self, criterias):
        """Build the problem hierarchy."""
        if criterias:
            self._tie(criterias)
            self._tie_problem(criterias)
    
    
    def _build_pcm(self, item):
        item.create_pcm()
        for child in item.children:
            self._build_pcm(child)
    
    
    def _tie(self, criterias):
        """Tie the criteria with their children and alternatives."""
        if not criterias:
            return
        
        for criteria_dict in criterias:
            for parent_criteria, criteria_list in criteria_dict.items():
                if criteria_list is None:
                    self._tie_alternatives(parent_criteria)
                else:
                    self._tie_criteries(parent_criteria, criteria_list)
                    self._tie(criteria_list)
    
    
    def _tie_alternatives(self, criteria):
        """Tie alternatives to the given criteria."""
        for alternative in self.alternatives:
            criteria.add_child(alternative)


    def _tie_criteries(self, parent_criteria, criteria_list):
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