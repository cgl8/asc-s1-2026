import sys
import subprocess

if __name__ == "__main__":

    solutions = []

    filename = sys.argv[1]
    transformed_path = './ts/' + filename
    transformed_opb_path = "./ts/transformed_" + filename[:-4] + ".opb"


    transform = subprocess.run(["python3", "transform.py", filename, './ts/' + filename], check=True)


    try:
        sp = subprocess.run(
        ["python3", "scripts/hybrid_to_pbo.py", './ts/' + filename, transformed_opb_path], 
        capture_output=True, 
        text=True, 
        check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running hybrid_to_pbo.py: {e}", file=sys.stderr)
        print(f"stderr: {e.stderr}", file=sys.stderr)
        exit(1)

    sp = subprocess.run(["java", "-jar", "sat4j-pb.jar", transformed_opb_path], 
        capture_output=True, 
        text=True)
    
    result = sp.stdout.strip().split('\n')[-2]
    result = result.split(" ")[1:-1]
    assignments = []
    for var in result:
        if var[0] == '-':
            assignment = -int(var[2:])
        else:
            assignment = int(var[1:])
        assignments.append(assignment)

    print(assignments)
    #Check that assignments are correct with the original untransformed problem
    solution_filepath = "./ts/transformed_solution_" + filename[:-4] + ".sol"
    solution_file = open(solution_filepath, 'w')
    for assignment in assignments:
        solution_file.write(str(assignment) + " ")
    sp = subprocess.run(["python3", "scripts/validate_solution.py", filename, solution_filepath],
        capture_output=True, 
        text=True, 
        check=True)
    print(sp.stdout)
    print(sp.stderr)
    sys.close(solution_file)

    if sp.returncode == 10:
        print("SAT")
    elif sp.returncode == 20:
        print("UNSAT")
        print(solutions)
        exit()
    else:
        print("sat4j error")
        exit(1)



    