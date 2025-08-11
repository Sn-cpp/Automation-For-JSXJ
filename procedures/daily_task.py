from enum import Enum

from cores.enum_header import SignalTypeEnum


from cores.procedure_utils import Procedure, SingleAction, BranchingAction
from cores.game_interface import GameInteface

class ProgressEnum(Enum):
        IDLE = 0
        GOTO_NPC = 1
        REACH_NPC = 2
        RECEIVE_TASK = 3
        REACH_FIELD_MAP = 4
        GOTO_FIELD = 5
        REACH_FIELD = 6
        START_TASK = 7
        AWAIT_COMPLETE = 8
        GOTO_BASE = 9
        REACH_BASE = 10
        GOTO_NPC_2 = 11
        REACH_NPC_2 = 12
        RETURN_TASK = 13

class DailyTask(Procedure):
    def __init__(self, interface: GameInteface, num: int):
        self.stage = ProgressEnum(value=0)
        self.step = 0
        
        self.tolerance = 0
        self.max_tol = 10
        self.count = num

        self.progress = {
            ProgressEnum.IDLE : ([
                SingleAction(interface.check_location, function_params=['Đạo Hương Thôn'])
            ], ProgressEnum.GOTO_NPC, False),
            ProgressEnum.GOTO_NPC: ([
                SingleAction(interface.goto_npc, function_params=['BaoV'])
            ], ProgressEnum.REACH_NPC, False),
            ProgressEnum.REACH_NPC: ([
                SingleAction(interface.is_reach_npc, lambda: interface.press('esc'))
            ], ProgressEnum.RECEIVE_TASK, False),
            ProgressEnum.RECEIVE_TASK: ([
                SingleAction(interface.click_from_center, function_params=[0, -25]),
                BranchingAction(interface.detect_dialog, lambda: True, self.raise_tolerance, condition_params=[SignalTypeEnum.NPC_DIALOG], branch_b_params=[self.goto_state, (None, 0)] ),
                SingleAction(interface.click_from_center, function_params=[-150, -60]),
                BranchingAction(interface.detect_dialog, lambda: True, self.raise_tolerance, condition_params=[SignalTypeEnum.NPC_DIALOG], branch_b_params=[self.goto_state, (None, 0)] ),                
                SingleAction(interface.click_from_center, function_params=[-150, 85]), 
                BranchingAction(interface.detect_dialog, lambda: True, self.raise_tolerance, condition_params=[SignalTypeEnum.NPC_DIALOG], branch_b_params=[self.goto_state, (None, 0)] ),
                SingleAction(interface.click_from_center, function_params=[-150, -65])
            ], ProgressEnum.REACH_FIELD_MAP, True),
            ProgressEnum.REACH_FIELD_MAP: ([
                BranchingAction(interface.check_location, lambda: True, self.raise_tolerance, condition_params=['Thục Cương Bí Cảnh'], branch_b_params=[self.goto_state, (ProgressEnum.RECEIVE_TASK, 0)]),
            ], ProgressEnum.GOTO_FIELD, False),
            ProgressEnum.GOTO_FIELD: ([
                SingleAction(interface.press, function_params=['f4']),
                SingleAction(interface.detect_and_click, function_params=[SignalTypeEnum.TASK_MARK]),
                SingleAction(interface.goto_mob)
            ], ProgressEnum.REACH_FIELD, True),
            ProgressEnum.REACH_FIELD: ([
                SingleAction(interface.is_reached)
            ], ProgressEnum.START_TASK, False),
            ProgressEnum.START_TASK: ([
                SingleAction(interface.click_center),
                SingleAction(interface.press, function_params=['f']),
                SingleAction(interface.set_timer)
            ], ProgressEnum.AWAIT_COMPLETE, True),
            ProgressEnum.AWAIT_COMPLETE: ([
                SingleAction(interface.elapse, function_params=[5]),
                SingleAction(interface.press, function_params=['f4']),
                BranchingAction(interface.is_task_complete, lambda: True, lambda : interface.set_timer() and self.goto_state(step=0) )
            ], ProgressEnum.GOTO_BASE, False),
            ProgressEnum.GOTO_BASE: ([
                SingleAction(interface.press, function_params=['2']),
                BranchingAction(interface.detect_dialog, lambda: True, self.raise_tolerance, condition_params=[SignalTypeEnum.NPC_DIALOG], branch_b_params=[self.goto_state, (None, 1)] ),
                SingleAction(interface.click_from_center, function_params=[-327, -110]),
                BranchingAction(interface.detect_dialog, lambda: True, self.raise_tolerance, condition_params=[SignalTypeEnum.NPC_DIALOG], branch_b_params=[self.goto_state, (None, 1)] ),
                SingleAction(interface.click_from_center, function_params=[-309, 21]),
                SingleAction(interface.set_timer)
            ], ProgressEnum.REACH_BASE, True),
            ProgressEnum.REACH_BASE: ([
                SingleAction(interface.elapse, function_params=[11]),
                BranchingAction(interface.check_location, lambda: True, lambda params: interface.set_timer() and self.raise_tolerance(*params), condition_params=['Đạo Hương Thôn'], branch_b_params=[self.goto_state, (ProgressEnum.GOTO_BASE, 0)])
            ], ProgressEnum.GOTO_NPC_2, False),
            ProgressEnum.GOTO_NPC_2: ([
                SingleAction(interface.get_on_horse),
                SingleAction(interface.goto_npc, function_params=['BaoV'])
            ], ProgressEnum.REACH_NPC_2, True),
            ProgressEnum.REACH_NPC_2: ([
                SingleAction(interface.is_reach_npc, lambda: interface.press('esc'))            
            ], ProgressEnum.RETURN_TASK, False),
            ProgressEnum.RETURN_TASK: ([
                SingleAction(interface.click_from_center, function_params=[0, -25]),
                BranchingAction(interface.detect_dialog, lambda: True, self.raise_tolerance, condition_params=[SignalTypeEnum.NPC_DIALOG], branch_b_params=[self.goto_state, (None, 0)] ),                
                SingleAction(interface.click_from_center, function_params=[-260, 52]),
                BranchingAction(interface.detect_dialog, lambda: True, self.raise_tolerance, condition_params=[SignalTypeEnum.REWARD], branch_b_params=[self.goto_state, (None, 0)] ),
                SingleAction(interface.click_from_center, function_params=[-153, 185]),
                SingleAction(interface.click_from_center, function_params=[68, 275]),
                SingleAction(interface.click_from_center, self.reduce_task_count,  function_params=[0, -25]),
            ], ProgressEnum.RECEIVE_TASK, True)
        }
        
    def reduce_task_count(self):
        self.count -= 1

