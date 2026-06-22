from __future__ import annotations
from typing import List, Optional, Tuple


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


class State:
    """Representa um estado do 8-puzzle como tupla imutável de 9 inteiros (0 = espaço vazio)."""

    def __init__(self, tiles: Tuple[int, ...], parent: Optional["State"] = None, action: Optional[str] = None, cost: int = 0):
        if len(tiles) != 9 or set(tiles) != set(range(9)):
            raise ValueError("Estado inválido: deve conter exatamente os valores 0-8.")
        self.tiles = tiles
        self.parent = parent
        self.action = action
        self.cost = cost

    @property
    def is_goal(self) -> bool:
        return self.tiles == GOAL_STATE

    @property
    def blank_index(self) -> int:
        return self.tiles.index(0)

    def neighbors(self) -> List["State"]:
        """Retorna os estados filhos válidos a partir deste estado.

        O tabuleiro é tratado como uma grade 3x3 (linha = índice // 3,
        coluna = índice % 3). Para cada movimento possível do espaço vazio
        (cima, baixo, esquerda, direita) que não sai da grade, gera um novo
        estado trocando o espaço vazio com a peça vizinha.

        A ação é nomeada pela direção do MOVIMENTO DA PEÇA (não do espaço
        vazio), pois é assim que normalmente se descreve a jogada: "mover a
        peça de baixo para cima" equivale a "Up" quando o espaço sobe.
        """
        moves = {
            "Up": -3,
            "Down": 3,
            "Left": -1,
            "Right": 1,
        }

        row, col = divmod(self.blank_index, 3)
        children: List["State"] = []

        for action, delta in moves.items():
            new_index = self.blank_index + delta

            # valida limites da grade conforme a direção
            if action == "Up" and row == 0:
                continue
            if action == "Down" and row == 2:
                continue
            if action == "Left" and col == 0:
                continue
            if action == "Right" and col == 2:
                continue

            new_tiles = list(self.tiles)
            new_tiles[self.blank_index], new_tiles[new_index] = (
                new_tiles[new_index],
                new_tiles[self.blank_index],
            )

            child = State(
                tuple(new_tiles),
                parent=self,
                action=action,
                cost=self.cost + 1,
            )
            children.append(child)

        return children

    def path(self) -> List["State"]:
        """Retorna a sequência de estados do estado inicial até este."""
        states: List["State"] = []
        current: Optional["State"] = self
        while current is not None:
            states.append(current)
            current = current.parent
        states.reverse()
        return states

    def actions(self) -> List[str]:
        """Retorna a sequência de ações do estado inicial até este."""
        return [state.action for state in self.path() if state.action is not None]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and self.tiles == other.tiles

    def __hash__(self) -> int:
        return hash(self.tiles)

    def __lt__(self, other: "State") -> bool:
        return self.cost < other.cost

    def __repr__(self) -> str:
        t = self.tiles
        return (
            f"+-------+\n"
            f"| {t[0]} {t[1]} {t[2]} |\n"
            f"| {t[3]} {t[4]} {t[5]} |\n"
            f"| {t[6]} {t[7]} {t[8]} |\n"
            f"+-------+"
        ).replace("0", " ")
