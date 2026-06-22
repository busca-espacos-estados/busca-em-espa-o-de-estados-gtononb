import heapq
import itertools
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        """Distância de Manhattan: soma, para cada peça (exceto o espaço
        vazio), da distância (em movimentos horizontais + verticais) entre
        sua posição atual e sua posição no estado objetivo.

        É admissível porque cada movimento do quebra-cabeça move exatamente
        uma peça em uma unidade de distância de Manhattan, então a heurística
        nunca superestima o custo real restante até o objetivo.
        """
        total = 0
        for index, value in enumerate(state.tiles):
            if value == 0:
                continue
            current_row, current_col = divmod(index, 3)
            goal_row, goal_col = divmod(value - 1, 3)
            total += abs(current_row - goal_row) + abs(current_col - goal_col)
        return total

    def search(self, initial: State) -> SearchResult:
        # Cada item da fronteira: (f_score, contador, estado)
        # `contador` desempata estados com o mesmo f_score de forma estável,
        # evitando comparar objetos State entre si quando os custos empatam.
        counter = itertools.count()

        g_score = {initial.tiles: 0}
        f_initial = self.heuristic(initial)

        frontier = [(f_initial, next(counter), initial)]
        # Para cada estado já visto, guarda o menor g_score conhecido para
        # decidir se vale a pena reabrir/explorar um caminho melhor.
        best_g = {initial.tiles: 0}
        explored = set()

        nodes_expanded = 0
        nodes_generated = 1  # estado inicial
        max_frontier_size = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))

            f, _, current = heapq.heappop(frontier)

            # Entrada obsoleta: já encontramos um caminho melhor para este
            # estado depois que ele foi inserido na fronteira.
            if current.cost > best_g.get(current.tiles, current.cost):
                continue

            if current.tiles in explored:
                continue

            if current.is_goal:
                return SearchResult(
                    solution=current,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=current.cost,
                )

            explored.add(current.tiles)
            nodes_expanded += 1

            for child in current.neighbors():
                nodes_generated += 1

                if child.tiles in explored:
                    continue

                tentative_g = child.cost  # custo acumulado desde a raiz

                if tentative_g < best_g.get(child.tiles, float("inf")):
                    best_g[child.tiles] = tentative_g
                    f_score = tentative_g + self.heuristic(child)
                    heapq.heappush(frontier, (f_score, next(counter), child))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=0,
        )
