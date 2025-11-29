from dataclasses import dataclass
from typing import List
from typing import Union

from src.core.sources import Resources
from src.dialogs.dialog import BaseDialog, DialogOption, DialogOptionType
from src.repositories.consequences import ConsequencesRepository


@dataclass()
class MainQuestions:
    text: str
    options: List[DialogOption]


@dataclass()
class TeacherIsAngryBecausePlayerAskedAgain:
    text: str
    options: List[DialogOption]


@dataclass()
class TeacherIsAngryBecausePlayerStartedScreaming:
    text: str
    options: List[DialogOption]


TeacherDialogState = Union[
    MainQuestions,
    TeacherIsAngryBecausePlayerAskedAgain,
    TeacherIsAngryBecausePlayerStartedScreaming
]


#   dialog branching
#   ^ - options
#   * - answers
#   |, -, _ - paths
#
#   |--> ^ ^ ^    ^    ^
#   |    | | |    |    |
#   |    | | |    *   end
#   ---- * * *  ^ ^ ^
#        | | |  | | |
#        *      *
#      ^ ^ ^    _____
#      | | |     end
#      *   *
#      -----
#       end
#
# TODO(@TrueWarg): replace textes on localised versions
class TeacherMainDialog(BaseDialog):
    def __init__(
            self,
            resources: Resources,
            consequences: ConsequencesRepository,
    ):
        super().__init__()
        self.resources = resources
        self.consequences = consequences
        self.teacher_patience = 2
        self.dialog = MainQuestions(
            text="\"Oh, sensei... is saying something. Maybe wake up from sleep?\"",
            options=[
                DialogOption("Sensei, may I leave?"),
                DialogOption("Sensei, what are people who hate technology called?"),
                DialogOption(
                    "[Knowledge] Sensei, could you remind me why neural networks are so hard to train? Especially human ones...",
                    DialogOptionType.SKILL_CHECK
                ),
                DialogOption("Shout \"Ооооо, Моя Оборона!\""),
                DialogOption("Nah, just keep sleeping...", DialogOptionType.TERMINAL),
            ],
        )

    def current_text(self) -> str:
        return self.dialog.text

    def current_options(self) -> List[DialogOption]:
        return self.dialog.options

    def select_option(self, idx: int):
        match self.dialog:
            case MainQuestions():
                self._main_question_transition(idx)
            case TeacherIsAngryBecausePlayerAskedAgain():
                self._teacher_is_angry_after_ask_transition(idx)
            case TeacherIsAngryBecausePlayerStartedScreaming():
                self._teacher_is_angry_after_screaming_transition(idx)

    def _main_question_transition(self, idx: int):
        match idx:
            case 0:
                if self.teacher_patience == 0:
                    self.consequences.is_Kento_off = True
                    self.dialog = TeacherIsAngryBecausePlayerAskedAgain(
                        text="Alright, off you go! And put the explanatory note on my desk!",
                        options=[
                            DialogOption("Sorry, sensei..."),
                            DialogOption(
                                "[Leave with Braveheart face] Freeeeedoooooooooooom!",
                                DialogOptionType.TERMINAL
                            ),
                            DialogOption("Petrovich, I’ll pour you a shot!"),
                        ]
                    )
                else:
                    new_text = "No, Kento. The lesson draws to an end."
                    if self.teacher_patience == 1:
                        new_text = "Kento, I said \"NO\""

                    new_first_option = DialogOption("Please, let me leave")

                    if self.teacher_patience == 1:
                        new_first_option = DialogOption("Leave. Leave. Leave. Leave. Leave. Leave")

                    self.dialog.text = new_text
                    self.dialog.options[0] = new_first_option
                    self.teacher_patience -= 1
            case 1:
                self.dialog.text = (
                    "People who strongly dislike or oppose technology are commonly called Luddites—a term "
                    "dating back to early 19th-century textile workers who smashed mechanized looms. Nowadays, "
                    "we use it more loosely for anyone skeptical or resistant to technological change.")
            case 2:
                self.dialog.text = (
                    "Neural networks are hard to train because they have millions of tiny settings "
                    "that all need to be adjusted just right. If you adjust them too much or too little "
                    "the network either learns nothing or breaks completely. They also need tons of examples—like "
                    "thousands or millions—before they start making sense of things."
                )

            case 3:
                self.consequences.is_Kento_off = True
                self.dialog = TeacherIsAngryBecausePlayerStartedScreaming(
                    text="What the hell are you yelling for, you fool! Get out!",
                    options=[
                        DialogOption("Leave with words \"Солнечный зайчик стеклянного глаза!\"",
                                     DialogOptionType.TERMINAL),
                        DialogOption("[Strength] Knock out the old fool.", DialogOptionType.SKILL_CHECK),
                        DialogOption("[Leave silently]", DialogOptionType.TERMINAL),
                    ]
                )

    def _teacher_is_angry_after_ask_transition(self, idx: int):
        match idx:
            case 0:
                self.dialog.text = "No \"sorry\"! OUT!"
                self.dialog.options = [DialogOption("Leave silently.", DialogOptionType.TERMINAL)]
            case 2:
                self.consequences.is_teacher_very_angry = True
                self.dialog.text = "What??? What Petrovich? What shot of...? PARENTS—TO SCHOOL!"
                self.dialog.options = [DialogOption("[Leave very quickly]", DialogOptionType.TERMINAL)]

    def _teacher_is_angry_after_screaming_transition(self, idx: int):
        if idx == 1:
            self.consequences.is_teacher_knocked = True
            self.dialog.text = "Kento, what are you doing?!... AAAAaaah... (The teacher collapses unconscious amid the shrieks of your classmates.)"
            self.dialog.options = [DialogOption("我が歌を中断するとは…… 次こそ、その無礼の代償を骨の髄まで味わうがよい。",
                                                DialogOptionType.TERMINAL)]


class TeacherPostMainDialog(BaseDialog):
    def __init__(
            self,
            resources: Resources,
            consequences: ConsequencesRepository,
    ):
        self.resources = resources
        self.consequences = consequences
        super().__init__()

    def current_text(self) -> str:
        if self.consequences.is_teacher_knocked:
            return "Keep silent..! Sensei is sleeping..."
        if self.consequences.is_teacher_very_angry:
            return "GET. OUT. HERE."
        return "Kento, please, leave the class."

    def current_options(self) -> List[DialogOption]:
        if self.consequences.is_teacher_knocked:
            return [DialogOption("[Leave silently]", DialogOptionType.TERMINAL)]
        else:
            return [DialogOption("[Leave] ", DialogOptionType.TERMINAL)]
