from enum import Enum
from typing import List
from dataclasses import dataclass


class DialogOptionType(Enum):
    SIMPLE = "simple"
    SKILL_CHECK = "skill_check"
    TERMINAL = "terminal"


@dataclass(frozen=True)
class DialogOption:
    text: str
    type: DialogOptionType = DialogOptionType.SIMPLE


class BaseDialog:
    def __init__(self):
        pass

    def current_text(self) -> str:
        pass

    def current_options(self) -> List[DialogOption]:
        pass

    def select_option(self, idx: int):
        pass
