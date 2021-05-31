from __future__ import annotations

from typing import List, Optional, Set

from python.mstar.identifier import Identifier

from math import inf


class State:
    def __init__(self, identifier: Identifier):
        self.identifier = identifier
        self.collision_set: Set[int] = set()
        self.back_set = {}

        self.parent = None

        self.cost = inf
        self.heuristic = None

        self.hash = None

    def __hash__(self):
        if self.hash is None:
            self.hash = hash(self.identifier.partial)

        return self.hash

    def reset(self):
        self.cost = inf

    def copy(self) -> State:
        s = State(self.identifier)
        s.cost = self.cost
        s.heuristic = self.heuristic
        s.parent = self.parent
        s.collision_set = self.collision_set.copy()
        s.back_set = self.back_set.copy()
        return s

    @property
    def priority(self) -> int:
        return self.cost + self.heuristic

    @property
    def is_standard(self) -> bool:
        """
        Standard nodes are nodes which do not contain partial actions (as are generated by
        operator decomposition)
        :return: True if this state is standard.
        """
        return self.identifier.partial == self.identifier.actual

    def merge_collision_sets(self, other_collision_set: Set[int]):
        self.collision_set = self.collision_set.union(other_collision_set)

    def is_collision_subset(self, other_set) -> bool:
        return other_set.issubset(self.collision_set)

    def add_back_set(self, state: State):
        self.back_set[state.identifier] = state

    def get_back_set(self):
        return self.back_set.values()

    def backtrack(self, res: Optional[List[State]] = None) -> List[State]:
        if res is None:
            res: List[State] = []
        if self.parent is not None:
            self.parent.backtrack(res)

        if self.is_standard:
            res.append(self)

        return res

    def __eq__(self, other: State) -> bool:
        return self.identifier == other.identifier

    def __gt__(self, other: State) -> bool:
        return self.priority > other.priority

    def __ge__(self, other: State) -> bool:
        return self.priority >= other.priority

    def __lt__(self, other: State) -> bool:
        return self.priority < other.priority

    def __le__(self, other: State) -> bool:
        return self.priority <= other.priority

    def __repr__(self):
        return f"cost: {self.cost}, heuristic: {self.heuristic}, identifier: {self.identifier}"
