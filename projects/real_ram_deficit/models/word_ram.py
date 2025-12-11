"""Word RAM model for integer operations with bit tracking."""

from dataclasses import dataclass


@dataclass
class WordRAMCost:
    word_operations: int = 0
    comparisons: int = 0
    memory_accesses: int = 0
    
    def total(self) -> int:
        return self.word_operations + self.comparisons + self.memory_accesses
    
    def reset(self) -> None:
        self.word_operations = 0
        self.comparisons = 0
        self.memory_accesses = 0


_word_ram_counter = WordRAMCost()


class WordRAMInteger:
    def __init__(self, value: int, word_size: int = 64):
        self.value = value
        self.word_size = word_size
    
    def _track_op(self):
        global _word_ram_counter
        _word_ram_counter.word_operations += 1
    
    def __add__(self, other):
        self._track_op()
        other_val = other.value if isinstance(other, WordRAMInteger) else other
        return WordRAMInteger(self.value + other_val, self.word_size)
    
    def __mul__(self, other):
        self._track_op()
        other_val = other.value if isinstance(other, WordRAMInteger) else other
        return WordRAMInteger(self.value * other_val, self.word_size)
    
    def __lt__(self, other) -> bool:
        _word_ram_counter.comparisons += 1
        other_val = other.value if isinstance(other, WordRAMInteger) else other
        return self.value < other_val
    
    def __repr__(self) -> str:
        return f"WordRAMInteger({self.value})"