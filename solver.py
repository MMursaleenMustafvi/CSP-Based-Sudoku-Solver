"""
=============================================================
  CSP-Based Sudoku Solver
  Techniques: Backtracking Search + Forward Checking + AC-3
=============================================================
  Author : [Your Name]
  Course : Artificial Intelligence
  Inst.  : NUCES – Chiniot-Faisalabad Campus
=============================================================
"""

from collections import deque
import copy
import time

# ─────────────────────────────────────────────
# GLOBAL PERFORMANCE COUNTERS
# ─────────────────────────────────────────────
backtrack_calls = 0   # total times backtrack() was entered
failures        = 0   # total times backtrack() returned None (failure)

# ─────────────────────────────────────────────
# SUDOKU STRUCTURE  (cells, units, peers)
# ─────────────────────────────────────────────
ROWS = "ABCDEFGHI"
COLS = "123456789"

def cross(A, B):
    """Cartesian product of characters in A and characters in B."""
    return [a + b for a in A for b in B]

# All 81 cell labels: A1, A2, … I9
CELLS = cross(ROWS, COLS)

# The 27 units: 9 rows + 9 columns + 9 3×3 boxes
ROW_UNITS = [cross(r, COLS) for r in ROWS]
COL_UNITS = [cross(ROWS, c) for c in COLS]
BOX_UNITS = [
    cross(rs, cs)
    for rs in ("ABC", "DEF", "GHI")
    for cs in ("123", "456", "789")
]
UNITS = ROW_UNITS + COL_UNITS + BOX_UNITS

# Pre-compute: for every cell, the set of all cells that share a unit with it
PEERS = {
    s: set(sum([u for u in UNITS if s in u], [])) - {s}
    for s in CELLS
}

# ─────────────────────────────────────────────
# PARSE INPUT  →  CSP domains
# ─────────────────────────────────────────────
def parse_grid(grid):
    """
    Convert an 81-character string (0 = empty) into a domain dictionary.

    Each cell starts with domain '123456789'.
    Known clues are immediately *assigned*, which propagates constraints
    via eliminate() before search begins.

    Returns the domain dict, or None if a contradiction is found.
    """
    values = {s: "123456789" for s in CELLS}

    for s, d in zip(CELLS, grid):
        if d != "0":                       # clue cell
            if not assign(values, s, d):   # propagate from the start
                return None                # puzzle is already unsatisfiable
    return values


# ─────────────────────────────────────────────
# ASSIGN  (Forward Checking entry-point)
# ─────────────────────────────────────────────
def assign(values, var, value):
    """
    Assign `value` to `var` by eliminating every OTHER value from its domain.

    This is the Forward Checking step: after each assignment we immediately
    reduce peer domains so that impossible values are pruned early.

    Returns values on success, False on contradiction.
    """
    other_values = values[var].replace(value, "")
    for v in other_values:
        if not eliminate(values, var, v):
            return False
    return True


# ─────────────────────────────────────────────
# ELIMINATE  (Constraint Propagation)
# ─────────────────────────────────────────────
def eliminate(values, var, value):
    """
    Remove `value` from domain of `var` and propagate two rules:

    Rule 1 – Naked Single:
        If after removal only ONE value remains in var's domain,
        that value can be eliminated from all of var's peers.

    Rule 2 – Hidden Single:
        If a unit now has only ONE cell where `value` can appear,
        assign that value to that cell.

    Returns True on success, False if a contradiction is detected.
    """
    # Value already absent – nothing to do
    if value not in values[var]:
        return True

    values[var] = values[var].replace(value, "")

    # ── Rule 0: Domain wipe-out → contradiction ──────────────────────────
    if len(values[var]) == 0:
        return False

    # ── Rule 1: Naked Single ─────────────────────────────────────────────
    elif len(values[var]) == 1:
        sole = values[var]
        for peer in PEERS[var]:
            if not eliminate(values, peer, sole):
                return False

    # ── Rule 2: Hidden Single (per unit) ─────────────────────────────────
    for unit in [u for u in UNITS if var in u]:
        places = [s for s in unit if value in values[s]]

        if len(places) == 0:          # value has nowhere to go → contradiction
            return False
        elif len(places) == 1:        # only one possible cell for value in this unit
            if not assign(values, places[0], value):
                return False

    return True


# ─────────────────────────────────────────────
# AC-3  (Arc Consistency)
# ─────────────────────────────────────────────
def revise(values, xi, xj):
    """
    Remove values from domain of xi that have NO consistent support in xj.

    In Sudoku all peers must be *different*, so a value x in xi is
    supported if xj can take some value y ≠ x.
    Returns True if the domain of xi was changed.
    """
    revised   = False
    to_remove = []

    for x in values[xi]:
        # x is consistent only if xj can hold at least one value ≠ x
        if not any(x != y for y in values[xj]):
            to_remove.append(x)

    for x in to_remove:
        values[xi] = values[xi].replace(x, "")
        revised = True

    return revised


def ac3(values):
    """
    AC-3 algorithm – enforces arc consistency across all peer pairs.

    Initialises the queue with every ordered arc (xi, xj) where xj is
    a peer of xi.  Whenever the domain of xi shrinks, all arcs pointing
    *into* xi are re-added so their consistency can be re-checked.

    Returns True if arc-consistency is achieved, False on contradiction.
    """
    queue = deque([(xi, xj) for xi in CELLS for xj in PEERS[xi]])

    while queue:
        xi, xj = queue.popleft()

        if revise(values, xi, xj):
            if len(values[xi]) == 0:        # domain empty → contradiction
                return False

            # Re-examine all arcs that feed into xi (excluding xj)
            for xk in PEERS[xi] - {xj}:
                queue.append((xk, xi))

    return True


# ─────────────────────────────────────────────
# MRV HEURISTIC  (variable ordering)
# ─────────────────────────────────────────────
def select_unassigned_var(values):
    """
    Minimum Remaining Values (MRV) heuristic.

    Picks the unassigned cell (domain size > 1) whose domain is smallest.
    This "fail-first" strategy detects dead ends early and prunes the
    search tree aggressively.
    """
    return min(
        [v for v in CELLS if len(values[v]) > 1],
        key=lambda var: len(values[var])
    )


# ─────────────────────────────────────────────
# BACKTRACKING SEARCH
# ─────────────────────────────────────────────
def backtrack(values):
    """
    Recursive backtracking search with Forward Checking + AC-3.

    At each step:
      1. Check if the puzzle is already solved (all domains are singletons).
      2. Choose the next variable with MRV.
      3. For each candidate value:
            a. Deep-copy the current domains (so we can undo on failure).
            b. Assign the value (triggers Forward Checking / propagation).
            c. Run AC-3 to further tighten remaining domains.
            d. Recurse.
      4. If no value leads to a solution, increment the failure counter
         and return None (triggers backtracking in the caller).
    """
    global backtrack_calls, failures
    backtrack_calls += 1

    # ── Base case: every cell has exactly one value ───────────────────────
    if all(len(values[s]) == 1 for s in CELLS):
        return values

    # ── Choose variable (MRV) ─────────────────────────────────────────────
    var = select_unassigned_var(values)

    # ── Try each value in the chosen cell's domain ────────────────────────
    for value in values[var]:
        new_values = copy.deepcopy(values)   # snapshot for undo

        if assign(new_values, var, value):   # Forward Checking
            if ac3(new_values):              # Arc Consistency (AC-3)
                result = backtrack(new_values)
                if result:
                    return result            # propagate solution upward

    # ── All values exhausted → backtrack ─────────────────────────────────
    failures += 1
    return None


# ─────────────────────────────────────────────
# TOP-LEVEL SOLVE
# ─────────────────────────────────────────────
def solve(grid):
    """
    Entry point: parse the puzzle, run AC-3 as preprocessing,
    then launch backtracking search.

    Returns (solution_dict | None, backtrack_calls, failures).
    """
    global backtrack_calls, failures
    backtrack_calls = 0
    failures        = 0

    values = parse_grid(grid)
    if not values:
        return None, 0, 0          # contradiction in given clues

    # Pre-processing: AC-3 before any guessing
    ac3(values)

    result = backtrack(values)
    return result, backtrack_calls, failures


# ─────────────────────────────────────────────
# DISPLAY
# ─────────────────────────────────────────────
def display(values):
    """Pretty-print the Sudoku grid with box separators."""
    print("  1 2 3   4 5 6   7 8 9")
    print(" +" + "-------+" * 3)
    for ri, r in enumerate(ROWS):
        row_str = f"{r}|"
        for ci, c in enumerate(COLS):
            row_str += " " + (values[r + c] if len(values[r + c]) == 1 else ".")
            if ci in (2, 5):
                row_str += " |"
        print(row_str + " |" if (len(row_str) - row_str.count("|")) else row_str)
        if ri in (2, 5):
            print(" +" + "-------+" * 3)
    print(" +" + "-------+" * 3)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    puzzles = [
        ("Easy",      "easy.txt"),
        ("Medium",    "medium.txt"),
        ("Hard",      "hard.txt"),
        ("Very Hard", "veryhard.txt"),
    ]

    for difficulty, filename in puzzles:
        print(f"\n{'='*52}")
        print(f"  {difficulty.upper()} BOARD  ({filename})")
        print(f"{'='*52}")

        try:
            with open(filename) as f:
                grid = "".join(line.strip() for line in f)

            if len(grid) != 81 or not set(grid).issubset(set("0123456789")):
                print("  ✗  Invalid input format (need 81 digits 0–9).")
                continue

            t0 = time.perf_counter()
            result, calls, fails = solve(grid)
            elapsed = time.perf_counter() - t0

            if result:
                display(result)
                print(f"\n  Backtrack calls  : {calls}")
                print(f"  Backtrack failures: {fails}")
                print(f"  Time             : {elapsed*1000:.2f} ms")
            else:
                print("  ✗  No solution found.")

        except FileNotFoundError:
            print(f"  ✗  File '{filename}' not found.")