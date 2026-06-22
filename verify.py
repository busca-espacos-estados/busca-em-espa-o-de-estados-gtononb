"""
Script de verificação manual: roda BFS, DFS e A* em alguns estados
e confirma que a sequência de ações retornada realmente resolve o puzzle.

Uso:
    python3 verify.py
"""

from puzzle.state import State, GOAL_STATE
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.a_star import AStar


def apply_action(tiles, action):
    """Aplica uma ação ('Up'/'Down'/'Left'/'Right') a uma tupla de tiles."""
    tiles = list(tiles)
    blank = tiles.index(0)
    row, col = divmod(blank, 3)
    delta = {"Up": -3, "Down": 3, "Left": -1, "Right": 1}[action]
    idx = blank + delta
    tiles[blank], tiles[idx] = tiles[idx], tiles[blank]
    return tuple(tiles)


def resolve(tiles, actions):
    """Aplica a sequência inteira de ações e retorna o estado final."""
    for a in actions:
        tiles = apply_action(tiles, a)
    return tiles


def check(name, algo, initial_tiles):
    result = algo.search(State(initial_tiles))
    if not result.found:
        print(f"[{name}] NÃO encontrou solução (pode ser esperado se o estado for insolúvel)")
        return

    final = resolve(initial_tiles, result.actions)
    ok = final == GOAL_STATE
    status = "OK ✅" if ok else "FALHOU ❌"

    print(f"[{name}] {status} | custo={result.path_cost} | "
          f"passos retornados={len(result.actions)} | "
          f"expandidos={result.nodes_expanded}")

    if not ok:
        print(f"   -> Esperado objetivo {GOAL_STATE}, obteve {final}")


if __name__ == "__main__":
    casos = [
        ("Já no objetivo", GOAL_STATE),
        ("1 movimento", (1, 2, 3, 4, 5, 6, 7, 0, 8)),
        ("Embaralhado moderado (16 ótimo)", (1, 2, 5, 3, 0, 6, 4, 8, 7)),
    ]

    for nome_caso, tiles in casos:
        print(f"\n=== Caso: {nome_caso} ===")
        check("BFS", BFS(), tiles)
        check("DFS", DFS(), tiles)
        check("A*", AStar(), tiles)
