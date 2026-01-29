Team
- Tyler Pencinger — UFID: 86826331
- Dominick Dupuy — UFID: 39922039

Language / Dependencies
- Python 3 (tested with Python 3.12)
- No external packages required (standard library only)

Build / Compile
- No build step required

Input Format
- Line 1: integer n
- Next n lines: hospital preference lists (each line is a permutation of 1..n)
- Next n lines: student preference lists (each line is a permutation of 1..n)
- Example input file: data/example.in

Output Format (Matcher)
- The matcher prints n lines, one per hospital i
- Each line is: i j meaning hospital i is matched to student j

Repository Layout
- src/matcher.py : hospital-proposing Gale–Shapley (Task A)
- src/verifier.py : validity + stability checker (Task B)
- src/scalability.py : timing + graph generation (Task C)
- data/example.in : example input
- data/example.out : expected output for example.in
- data/edge_case_n1.in, data/edge_case_n1.out : additional edge-case test (n=1)
- data/scalability_graph.png : Task C graph output

Running the Matcher (Task A)
- From the repository root:
  python src/matcher.py data/example.in
- To save output to a file:
  python src/matcher.py data/example.in > data/example.out

Running the Verifier (Task B)
- The verifier checks validity (every hospital and student is matched exactly once, no duplicates) and stability (no blocking pair)
- From the repository root:
  python src/verifier.py data/example.in data/example.out
- If the matching is correct, the verifier prints:
  VALID STABLE
- Otherwise it prints:
  Invalid: ... or Unstable: ...

Scalability Analysis (Task C)
- Run the scalability test:
  python src/scalability.py
- This measures running time for n = 1, 2, 4, 8, 16, 32, 64, 128, 256, 512
- Results are saved to data/scalability_graph.png

Scalability Results:
| n | Matcher (ms) | Verifier (ms) |
|---|--------------|---------------|
| 1 | 0.005 | 0.006 |
| 2 | 0.004 | 0.005 |
| 4 | 0.004 | 0.005 |
| 8 | 0.009 | 0.009 |
| 16 | 0.032 | 0.023 |
| 32 | 0.084 | 0.087 |
| 64 | 0.288 | 0.276 |
| 128 | 1.252 | 1.148 |
| 256 | 4.764 | 4.502 |
| 512 | 36.968 | 27.058 |

Trend Analysis:
The matcher and the verifier both show a time complexity of O(n^2) because Gale-Shapley scales with n^2 
as discussed in lecture. To elaborate, the Gale-Shapley algorithm causes each hospital to propose to all students in the worst-case. The verifier must also run in O(n^2) because the algorithm needs to check all
potential blocking pairs (n students times n hospitals) to check for stability. The graph shows this quadratic growth pattern clearly.

Assumptions / Notes
- Hospitals and students are labeled 1..n
- Preference lists are complete and strict (each list is a permutation of 1..n)
- The matching file must contain exactly n non-empty lines in the format: hospital student
- Input files must contain exactly 2n + 1 non-empty lines
- Files should be saved in UTF-8 encoding
