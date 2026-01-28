import sys

def read_input(filename):
    
    try:
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        if not lines:
            raise ValueError("Empty input file")
        
        n = int(lines[0])
        
        if n == 0:
            raise ValueError("n must be at least 1")
        
        if len(lines) != 2 * n + 1:
            raise ValueError(f"Expected {2*n + 1} lines, got {len(lines)}")
        
        
        hospital_prefs = {}
        for i in range(1, n + 1):
            prefs = list(map(int, lines[i].split()))
            if len(prefs) != n:
                raise ValueError(f"The hospital {i} has {len(prefs)} preferences, expected {n}")
            if sorted(prefs) != list(range(1, n + 1)):
                raise ValueError(f"The hospital {i} preferences aren't a valid permutation of 1..{n}")
            hospital_prefs[i] = prefs
        

        student_prefs = {}
        for i in range(n + 1, 2 * n + 1):
            student_id = i - n
            prefs = list(map(int, lines[i].split()))
            if len(prefs) != n:
                raise ValueError(f"The student {student_id} has {len(prefs)} preferences, expected {n}")
            if sorted(prefs) != list(range(1, n + 1)):
                raise ValueError(f"The student {student_id} preferences are not a valid permutation of 1..{n}")
            student_prefs[student_id] = prefs
        
        return n, hospital_prefs, student_prefs
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Invalid input - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input: {e}")
        sys.exit(1)

def gale_shapley(n, hospital_prefs, student_prefs):

    hospital_match = {h: None for h in range(1, n + 1)}
    student_match = {s: None for s in range(1, n + 1)}
    
    next_proposal_idx = {h: 0 for h in range(1, n + 1)}
    
    student_rank = {}
    for s in range(1, n + 1):
        student_rank[s] = {}
        for rank, h in enumerate(student_prefs[s]):
            student_rank[s][h] = rank
    
    proposal_count = 0
 
    while True:
        free_hospital = None
        for h in range(1, n + 1):
            if hospital_match[h] is None and next_proposal_idx[h] < n:
                free_hospital = h
                break
        
        if free_hospital is None:
            break
        
        h = free_hospital
        

        s = hospital_prefs[h][next_proposal_idx[h]]
        next_proposal_idx[h] += 1
        proposal_count += 1
  
        if student_match[s] is None:
        

            hospital_match[h] = s
            student_match[s] = h

        else:
        
            current_h = student_match[s]
        
            if student_rank[s][h] < student_rank[s][current_h]:

                hospital_match[current_h] = None
                hospital_match[h] = s
                student_match[s] = h
    
    return hospital_match, proposal_count

def main():
    if len(sys.argv) != 2:
        print("Usage: python matcher.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    n, hospital_prefs, student_prefs = read_input(input_file)

    matching, proposal_count = gale_shapley(n, hospital_prefs, student_prefs)

    for hospital in range(1, n + 1):
        print(f"{hospital} {matching[hospital]}")

if __name__ == "__main__":
    main()
