import subprocess
import sys
filename = "./ts/performance.hybrid"
times  = []
for clause_length in range(2, 100):
    file = open(filename, 'w')
    file.write("p hybrid " + str(clause_length) + " 1\n")
    for var in range(1, clause_length+1):
        file.write(str(var) + " ")
    file.write("0")
    file.close()

    try:
        afsat = subprocess.run(["python3", "afsat.py", filename, "-d", "INFO"], 
        capture_output=True, 
        text=True,
        check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running transform.py: {e}", file=sys.stderr)
        print(f"stderr: {e.stderr}", file=sys.stderr)
        exit(1)
    #print(afsat.stderr)
    time = afsat.stderr.strip().split('\n')[-1]
    time = time.split()[-1]
    print(time)
    times.append(time)
print(times)
with open("times.txt", 'w') as f:
    f.writelines(times)
