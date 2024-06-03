from anahiepro.nodes import Problem, Criteria, Alternative


# TODO: Create methods for solving the problem and for setting the matrix to each layer.

class Model:
    def __init__(self, problem, criterias: list, alternatives: list):
        self.problem = problem
        self.alternatives = alternatives
        self.criterias = criterias
        self._build_problem(criterias)
        self._build_pcm(self.problem)
    
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
    
    def find_criteria(self, key: tuple):
        """Find criteria by (name, id) tuple."""
        return self._find_criteria(key, self.criterias)
    
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