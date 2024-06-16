class _ModelBuilder:
    def __init__(self, problem, criterias, alternatives):
        self.problem = problem
        self.criterias = criterias
        self.alternatives = alternatives
    
    def build(self):
        self._build_model(self.criterias)
        self._build_pcm(self.problem)
    
    def _build_model(self, criterias):
        if len(criterias) == 0:
            self._build_model_without_criterias()
        else:
            self._build_model_with_criterias(criterias)
    
    def _build_model_without_criterias(self):
        self._tie_alternatives(self.problem)
    
    def _build_model_with_criterias(self, criterias):
        self._tie_criterias(criterias)
        self._tie_problem(criterias)
    
    def _build_pcm(self, item):
        item.create_pcm()
        for child in item.get_children():
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
    
    
    