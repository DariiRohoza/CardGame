from typing import Optional

from constants_libraries import POSSIBLE_TECH, POSSIBLE_MODIFIERS


class MoveTech:
    def __init__(self, tech: str, modifiers: str | list[str], chain_count: int = 0):
        self.tech: Optional[str] = None
        self.modifiers: list[str] = []
        self.chain_count: int = 0

        self.add_info(tech, modifiers, chain_count)

    def __str__(self) -> str:
        if self.tech is None:
            return f"Not complete"
        tech, chain = "", ""
        if len(self.modifiers) != 0:
            tech += " : "
        for idx, mod in enumerate(self.modifiers):
            tech += f"{mod}"
            tech += " | " if idx < len(self.modifiers) - 1 else ""
        for _ in range(self.chain_count):
            chain += f" \\ CHAIN"
        return f"{self.tech}{tech}{chain}"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, value: MoveTech) -> bool:
        if type(value) is not MoveTech:
            return False
        if self.tech == value.tech and self.modifiers == value.modifiers:
            return True
        return False

    def add_info(self, tech: str, modifiers: str | list[str], chain_count: int = 0):
        if type(tech) is not str or type(chain_count) is not int:
            raise TypeError(f"Tech {tech} or chain_count {chain_count}: Invalid type")
        elif tech not in POSSIBLE_TECH or chain_count < 0:
            raise ValueError(f"Tech {tech} or chain_count {chain_count}: Invalid value")
        elif self.tech is not None:
            raise ValueError(f"Tech {self.tech}: A value is already assigned")
        else:
            self.tech = tech
            self.chain_count = chain_count

        if not self.modifiers:
            modifiers: list[str] = list(modifiers)
            for idx, mod in enumerate(modifiers):
                mod = mod.strip().upper()
                if type(mod) is not str:
                    raise TypeError(f"Modifier {mod}: Invalid type")
                elif mod not in POSSIBLE_MODIFIERS:
                    raise ValueError(f"Modifier {mod}: Invalid value")

                self.modifiers.append(mod)

    def add_chain(self):
        self.chain_count += 1