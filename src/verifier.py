import sys


def read_input(filename):
    try:
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]

        if not lines:
            raise ValueError("Empty input file")

        n = int(lines[0])
        if n < 1:
            raise ValueError("n must be at least 1")

        if len(lines) != 2 * n + 1:
            raise ValueError(f"Expected {2*n + 1} lines, got {len(lines)}")

        hospital_prefs = {}
        for i in range(1, n + 1):
            prefs = list(map(int, lines[i].split()))
            if len(prefs) != n:
                raise ValueError(f"The hospital {i} has {len(prefs)} preferences, expected {n}")
            if sorted(prefs) != list(range(1, n + 1)):
                raise ValueError(f"The hospital {i} preferences are not a permutation of 1..{n}")
            hospital_prefs[i] = prefs

        student_prefs = {}
        for i in range(n + 1, 2 * n + 1):
            s_id = i - n
            prefs = list(map(int, lines[i].split()))
            if len(prefs) != n:
                raise ValueError(f"The student {s_id} has {len(prefs)} preferences, expected {n}")
            if sorted(prefs) != list(range(1, n + 1)):
                raise ValueError(f"The student {s_id} preferences aren't a permutation of 1..{n}")
            student_prefs[s_id] = prefs

        return n, hospital_prefs, student_prefs

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Invalid input - {e}")
        sys.exit(1)


def read_matching(filename, n):

    try:
        with open(filename, 'r') as f:
            raw_lines = f.readlines()

        lines = [line.strip() for line in raw_lines if line.strip()]

        if len(lines) != n:
            raise ValueError(f"Expected exactly {n} non-empty lines, got {len(lines)}")

        matching = {}
        seen_hospitals = set()

        for idx, line in enumerate(lines, start=1):
            parts = line.split()
            if len(parts) != 2:
                raise ValueError(f"Line {idx}: invalid format '{line}', expected 'hospital student'")

            hospital = int(parts[0])
            student = int(parts[1])

            if hospital < 1 or hospital > n:
                raise ValueError(f"Line {idx}: invalid hospital ID: {hospital}")
            if student < 1 or student > n:
                raise ValueError(f"Line {idx}: invalid student ID: {student}")

            if hospital in seen_hospitals:
                raise ValueError(f"Duplicate hospital {hospital} in matching file")
            seen_hospitals.add(hospital)

            matching[hospital] = student

        return matching

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except ValueError as e:
        print(f"Invalid: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading matching: {e}")
        sys.exit(1)


def check_validity(n, matching):
    expected_h = set(range(1, n + 1))
    got_h = set(matching.keys())
    if got_h != expected_h:
        missing = sorted(expected_h - got_h)
        extra = sorted(got_h - expected_h)
        msg = []
        if missing:
            msg.append(f"Missing hospitals: {missing}")
        if extra:
            msg.append(f"Extra hospitals: {extra}")
        return False, "Invalid: " + "; ".join(msg)

    students = list(matching.values())
    if len(students) != n:
        return False, "Invalid: Matching does not contain n assignments"

    if set(students) != set(range(1, n + 1)):
        missing = sorted(set(range(1, n + 1)) - set(students))
        extra = sorted(set(students) - set(range(1, n + 1)))
        msg = []
        if missing:
            msg.append(f"Unmatched students: {missing}")
        if extra:
            msg.append(f"Invalid students: {extra}")
        return False, "Invalid: " + "; ".join(msg)

    if len(set(students)) != n:
        return False, "Invalid: Duplicate student assignments"

    return True, None

def check_stability(n, matching, hospital_prefs, student_prefs):

    student_match = {s: h for h, s in matching.items()}


    hospital_rank = {h: {s: r for r, s in enumerate(hospital_prefs[h])} for h in range(1, n + 1)}
    student_rank = {s: {h: r for r, h in enumerate(student_prefs[s])} for s in range(1, n + 1)}


    for h in range(1, n + 1):
        current_s = matching[h]
        cutoff_rank = hospital_rank[h][current_s]

        for s in hospital_prefs[h][:cutoff_rank]:
            current_h_for_s = student_match[s]
            if student_rank[s][h] < student_rank[s][current_h_for_s]:
                return False, (
                    f"Unstable: Blocking pair (Hospital {h}, Student {s}). "
                    f"Hospital {h} prefers {s} over its match {current_s}, "
                    f"and Student {s} prefers {h} over its match {current_h_for_s}."
                )

    return True, None

def main():
    if len(sys.argv) != 3:
        print("Usage: python verifier.py <input_file> <matching_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    matching_file = sys.argv[2]

    n, hospital_prefs, student_prefs = read_input(input_file)
    

    matching = read_matching(matching_file, n)

    ok, msg = check_validity(n, matching)
    if not ok:
        print(msg)
        sys.exit(1)

    ok, msg = check_stability(n, matching, hospital_prefs, student_prefs)
    if not ok:
        print(msg)
        sys.exit(1)

    print("VALID STABLE")

if __name__ == "__main__":
    main()
