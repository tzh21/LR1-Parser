Symbol = str
SymbolString = list[str]
Production = tuple[Symbol, SymbolString]
ProductionTable = dict[Symbol, list[SymbolString]]
# LR(1) 表的项，比如 jump <state>, reduce <production>
Lr1Command = tuple[str, str]

START_SYMBOL = 'S\''
EOF_SYMBOL = '$'

class Item:
    def __init__(self, lhs: Symbol, rhs: SymbolString, dotPos: int, lookahead: str) -> None:
        self.lhs = lhs
        self.rhs = rhs
        self.dotPos = dotPos
        self.lookahead = lookahead
    def __str__(self) -> str:
        return f'{self.lhs} -> {self.rhs}, {self.dotPos}, {self.lookahead}'
    def __eq__(self, other) -> bool:
        return (self.lhs, self.rhs, self.dotPos, self.lookahead) == (other.lhs, other.rhs, other.dotPos, other.lookahead)
    def __hash__(self) -> int:
        return hash((self.lhs, tuple(self.rhs), self.dotPos, self.lookahead))

from enum import Enum

class Lr1Command(Enum):
    SHIFT = 'shift'
    GOTO = 'goto'
    REDUCE = 'reduce'
    ACCEPT = 'accept'

class TableAlreadyFilledException(Exception):
    pass


Collection = set[Item]
CollToId = dict[Collection, int]
Action = tuple[Lr1Command, Collection | Production | str]
Lr1Table = dict[(Collection, str), Action]

class AstNode:
    def __init__(self, symbol: str, isTerminal: bool, children: list | str) -> None:
        self.symbol: str = symbol
        self.isTerminal: bool = isTerminal
        self.children: list[AstNode] | str = children
    def to_dict(self):
        if isinstance(self.children, str):
            children_data = self.children
        else:
            children_data = [child.to_dict() for child in self.children]
        return {
            "symbol": self.symbol,
            "isTerminal": self.isTerminal,
            "children": children_data
        }

emptyString = 'epsilon'