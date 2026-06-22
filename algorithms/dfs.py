from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        # Pilha de (estado, profundidade). Usamos pilha explícita em vez de
        # recursão para evitar estourar o limite de recursão do Python em
        # buscas mais profundas.
        stack = [(initial, 0)]

        # Conjunto global de estados já expandidos (graph search). Sem isso,
        # o DFS pode reentrar repetidamente nos mesmos estados por caminhos
        # diferentes dentro do limite de profundidade, e o número de nós
        # gerados explode de forma combinatória antes de esgotar a busca —
        # especialmente em estados insolúveis, onde toda a "metade" do
        # espaço de estados alcançável precisa ser varrida.
        visited = set()

        nodes_expanded = 0
        nodes_generated = 1  # estado inicial
        max_frontier_size = 1

        while stack:
            max_frontier_size = max(max_frontier_size, len(stack))

            current, depth = stack.pop()

            if current.tiles in visited:
                continue

            if current.is_goal:
                return SearchResult(
                    solution=current,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=current.cost,
                )

            visited.add(current.tiles)

            if depth >= self.depth_limit:
                continue

            nodes_expanded += 1

            for child in current.neighbors():
                nodes_generated += 1
                if child.tiles in visited:
                    continue
                stack.append((child, depth + 1))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=0,
        )