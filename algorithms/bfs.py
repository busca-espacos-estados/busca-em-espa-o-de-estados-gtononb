from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        if initial.is_goal:
            return SearchResult(
                solution=initial,
                nodes_expanded=0,
                nodes_generated=1,
                max_frontier_size=1,
                depth=0,
            )

        frontier = deque([initial])
        frontier_set = {initial.tiles}
        explored = set()

        nodes_expanded = 0
        nodes_generated = 1  # conta o estado inicial
        max_frontier_size = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))

            current = frontier.popleft()
            frontier_set.discard(current.tiles)
            explored.add(current.tiles)
            nodes_expanded += 1

            for child in current.neighbors():
                nodes_generated += 1

                if child.tiles in explored or child.tiles in frontier_set:
                    continue

                if child.is_goal:
                    max_frontier_size = max(max_frontier_size, len(frontier) + 1)
                    return SearchResult(
                        solution=child,
                        nodes_expanded=nodes_expanded,
                        nodes_generated=nodes_generated,
                        max_frontier_size=max_frontier_size,
                        depth=child.cost,
                    )

                frontier.append(child)
                frontier_set.add(child.tiles)

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=0,
        )
