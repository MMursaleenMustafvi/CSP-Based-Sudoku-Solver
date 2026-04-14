# 🧩 CSP-Based Sudoku Solver

A Python implementation of a Sudoku solver built as a **Constraint Satisfaction Problem (CSP)**, using **Backtracking Search**, **Forward Checking**, and **AC-3 Arc Consistency**.

Built for the Artificial Intelligence course at **NUCES – Chiniot-Faisalabad Campus**.

---

## 📌 Features

- ✅ AC-3 arc consistency as a preprocessing step
- ✅ Forward checking with constraint propagation on every assignment
- ✅ Naked Single and Hidden Single elimination rules
- ✅ Minimum Remaining Values (MRV) heuristic for variable ordering
- ✅ Solves Easy → Very Hard puzzles in milliseconds
- ✅ Tracks backtrack call count and failure count per puzzle

---

## 🗂️ Project Structure

```
sudoku-solver/
├── sudoku_solver.py   # Main solver (all logic in one file)
├── easy.txt           # Easy puzzle input
├── medium.txt         # Medium puzzle input
├── hard.txt           # Hard puzzle input
├── veryhard.txt       # Very hard puzzle input
└── README.md
```

---

## ▶️ How to Run

**Requirements:** Python 3.x — no external libraries needed.

```bash
# Clone the repo
git clone https://github.com/your-username/sudoku-csp-solver.git
cd sudoku-csp-solver

# Run the solver (solves all 4 boards automatically)
python3 sudoku_solver.py
```

---

## 📄 Input Format

Each puzzle is a plain `.txt` file with exactly **9 lines** of **9 digits**.  
Use `0` for empty cells.

**Example (`easy.txt`):**
```
004030050
609400000
005100489
000060930
300807002
026040000
453009600
000004705
090050200
```

---

## 📊 Results

### Easy Board
```
  1 2 3   4 5 6   7 8 9
 +-------+-------+-------+
A| 7 8 4 | 9 3 2 | 1 5 6 |
B| 6 1 9 | 4 8 5 | 3 2 7 |
C| 2 3 5 | 1 7 6 | 4 8 9 |
 +-------+-------+-------+
D| 5 7 8 | 2 6 1 | 9 3 4 |
E| 3 4 1 | 8 9 7 | 5 6 2 |
F| 9 2 6 | 5 4 3 | 8 7 1 |
 +-------+-------+-------+
G| 4 5 3 | 7 2 9 | 6 1 8 |
H| 8 6 2 | 3 1 4 | 7 9 5 |
I| 1 9 7 | 6 5 8 | 2 4 3 |
 +-------+-------+-------+
Backtrack calls: 1  |  Failures: 0  |  Time: ~5ms
```

### Medium Board
```
  1 2 3   4 5 6   7 8 9
 +-------+-------+-------+
A| 3 2 6 | 7 5 4 | 9 1 8 |
B| 8 5 9 | 6 1 2 | 4 7 3 |
C| 1 7 4 | 3 8 9 | 6 2 5 |
 +-------+-------+-------+
D| 7 4 1 | 8 6 3 | 5 9 2 |
E| 9 8 5 | 4 2 1 | 3 6 7 |
F| 6 3 2 | 5 9 7 | 8 4 1 |
 +-------+-------+-------+
G| 2 1 3 | 9 4 8 | 7 5 6 |
H| 5 9 8 | 2 7 6 | 1 3 4 |
I| 4 6 7 | 1 3 5 | 2 8 9 |
 +-------+-------+-------+
Backtrack calls: 18  |  Failures: 3  |  Time: ~29ms
```

### Hard Board
```
  1 2 3   4 5 6   7 8 9
 +-------+-------+-------+
A| 8 3 7 | 5 4 6 | 1 9 2 |
B| 6 5 9 | 1 3 2 | 4 7 8 |
C| 2 1 4 | 7 9 8 | 5 6 3 |
 +-------+-------+-------+
D| 1 4 5 | 2 6 7 | 8 3 9 |
E| 7 8 3 | 4 5 9 | 6 2 1 |
F| 9 2 6 | 8 1 3 | 7 5 4 |
 +-------+-------+-------+
G| 4 7 1 | 3 2 5 | 9 8 6 |
H| 5 9 2 | 6 8 4 | 3 1 7 |
I| 3 6 8 | 9 7 1 | 2 4 5 |
 +-------+-------+-------+
Backtrack calls: 18  |  Failures: 0  |  Time: ~29ms
```

### Very Hard Board
```
  1 2 3   4 5 6   7 8 9
 +-------+-------+-------+
A| 8 2 6 | 1 5 7 | 4 9 3 |
B| 9 4 3 | 6 8 2 | 1 7 5 |
C| 1 7 5 | 3 9 4 | 2 8 6 |
 +-------+-------+-------+
D| 2 6 8 | 4 1 5 | 9 3 7 |
E| 3 1 4 | 9 7 8 | 5 6 2 |
F| 7 5 9 | 2 6 3 | 8 1 4 |
 +-------+-------+-------+
G| 4 8 7 | 5 3 9 | 6 2 1 |
H| 6 9 2 | 7 4 1 | 3 5 8 |
I| 5 3 1 | 8 2 6 | 7 4 9 |
 +-------+-------+-------+
Backtrack calls: 10  |  Failures: 0  |  Time: ~17ms
```

---

## 🔍 Stats Analysis

| Board     | Backtrack Calls | Failures | Time  |
|-----------|-----------------|----------|-------|
| Easy      | 1               | 0        | ~5ms  |
| Medium    | 18              | 3        | ~29ms |
| Hard      | 18              | 0        | ~29ms |
| Very Hard | 10              | 0        | ~17ms |

**Easy (calls=1, failures=0):** Solved entirely by constraint propagation — AC-3 and elimination rules reduce every cell to a singleton before backtracking even begins. No guessing required.

**Medium (calls=18, failures=3):** Propagation alone isn't sufficient. The solver guesses 3 wrong values before finding the solution, showing that medium puzzles occasionally send search down a wrong branch.

**Hard (calls=18, failures=0):** Same call count as medium but zero failures — AC-3 preprocessing was strong enough that every guess happened to be correct. This demonstrates that AC-3 can make structurally "harder" puzzles cheaper to solve than easier ones.

**Very Hard (calls=10, failures=0):** Fewest calls of all four boards. The "very hard" label reflects human difficulty (fewer given clues), but AC-3 + MRV exploit the puzzle's constraint structure so efficiently that no wrong branches are explored at all.

---

## 🧠 Algorithm Overview

```
solve(grid)
  └── parse_grid()          → build domain dict {cell: "123456789"}
  └── ac3()                 → preprocessing: enforce arc consistency
  └── backtrack()
        └── if all domains are singletons → return solution
        └── select_unassigned_var()  ← MRV heuristic
        └── for each value in domain:
              └── assign()           ← forward checking + propagation
              └── ac3()              ← tighten remaining domains
              └── backtrack()        ← recurse
```

### Key Components

| Component | Role |
|---|---|
| `parse_grid()` | Converts 81-char string to CSP domain dictionary |
| `assign()` | Assigns a value; eliminates all others (Forward Checking) |
| `eliminate()` | Propagates Naked Single and Hidden Single rules |
| `ac3()` | Enforces arc consistency across all peer pairs |
| `revise()` | Removes unsupported values from a cell's domain |
| `select_unassigned_var()` | MRV — picks the cell with fewest remaining values |
| `backtrack()` | Recursive search with undo via deep copy |

---

## 📚 References

- Russell, S. & Norvig, P. — *Artificial Intelligence: A Modern Approach*, 4th ed. (Chapter 6: CSP)
- Norvig, P. — [Solving Every Sudoku Puzzle](http://norvig.com/sudoku.html)

---

## 👤 Author

**[Your Name]**  
BS Computer Science — NUCES Chiniot-Faisalabad Campus  
Course: Artificial Intelligence
