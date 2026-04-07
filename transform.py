import sys

if __name__ == "__main__":
    filename = sys.argv[1]
    outputdir = sys.argv[2]
    file = open(filename, 'r')
    tmpfile = open(outputdir, 'w')
    fl = file.readline().split(' ')
    numvars = int(fl[2])
    numcls = int(fl[3])

    body_lines = []

    for line in file:
        tok = line.split(' ')
        if tok[0] == 'eo' and len(tok) > 30: #TODO: find where it breaks
            tok = tok[1:len(tok)-1]
            chunks = [tok[i:i + 10] for i in range(0, len(tok), 10)] #TODO: different splitting methods?
            oldnumvars = numvars
            for chunk in chunks:
                body_line = "eo"
                for var in chunk:
                    body_line += " " + str(var)
                body_line += f" {numvars+1} 0\n"
                body_lines.append(body_line)
                numvars += 1
                numcls += 1
            body_line = "eo "
            for x in range(oldnumvars+1, numvars+1):
                body_line += str(x) + " "
            body_line += "0\n"
            body_lines.append(body_line)
        elif tok[0] != 'c' and len(tok) > 30: #cnf TODO: add more constraint types
                tok = tok[0:len(tok)-1]
                chunks = [tok[i:i + 10] for i in range(0, len(tok), 10)]
                oldnumvars = numvars
                for chunk in chunks:
                    body_line = ""
                    for var in chunk:
                        body_line += str(var) + " "
                    body_line += f"{numvars+1} 0\n"
                    body_lines.append(body_line)
                    numvars += 1
                    numcls += 1
                body_line = ""
                for x in range(oldnumvars+1, numvars+1):
                    body_line += "-" + str(x) + " "
                body_line += "0\n"
                body_lines.append(body_line)
        else:
            body_lines.append(line)

    tmpfile.write(f"p hybrid {numvars} {numcls}\n")
    tmpfile.writelines(body_lines)


    file.close()
    tmpfile.close()
    