import sys

file_name = sys.argv[1]
print(file_name)

with open(file_name) as file:
    for line in file:
        clean = line.split("#")[0].strip()
        # print(clean)

        if clean == "":
            continue
        else:
            print(clean)
