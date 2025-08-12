from enum import Enum

class SingleAction:
    def __init__(self, function: object, callback: object = None, function_params: list = [], callback_params: list = []):
        self.function = function        
        self.callback = callback

        self.function_params = function_params
        self.callback_params = callback_params

    def execute(self):
        if self.function(*self.function_params):
            if self.callback:
                self.callback(*self.callback_params)
            return True
        return False

class BranchingAction:
    def __init__(self, condition: object, branch_a: object, branch_b: object, condition_params: list = [],  branch_a_params: list = [], branch_b_params: list = []):
        self.condition = condition
        self.branch_a = branch_a
        self.branch_b = branch_b

        self.condition_params = condition_params
        self.branch_a_params = branch_a_params
        self.branch_b_params = branch_b_params
    
    def execute(self):
        if self.condition(*self.condition_params):
            return self.branch_a(*self.branch_a_params)
        else:
            if self.branch_b:
                return self.branch_b(*self.branch_b_params)
            return False

class Procedure:
    def __init__(self):
        self.progress = None
        self.stage = None
        self.step = None

        self.tolerance = 0
        self.max_tol = 4

    def execute(self):
        if self.progress[self.stage][0][self.step].execute():
            self.step += 1
            self.tolerance = 0
            if self.step == len(self.progress[self.stage][0]):
                self.stage = self.progress[self.stage][1]
                self.step = 0
                return False
    
        return self.progress[self.stage][2]

    def goto_state(self, stage: Enum = None, step: int = None):
        if stage != None:
            self.stage = stage
        if step != None:
            self.step = step 

    def raise_tolerance(self, callback, params):
        self.tolerance += 1
        if self.tolerance == self.max_tol:
            self.tolerance = 0
            callback(*params)
    