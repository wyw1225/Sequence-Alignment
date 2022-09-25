from typing import Tuple


def generate_input_string(path: str) -> Tuple[str, str]:
    f = open(path) #open file

    #generate base string A
    line = f.readline()
    A = line.strip() #delete /n

    # used for store digits
    a = []
    b = []

    # generate base string B, and integer string a,b
    while line:
        line = f.readline()
        line = line.strip()
        if (line.isdigit()):
            a.append(int(line))
        else:
            B = line
            while line:
                line = f.readline()
                line = line.strip()
                # handle empty line
                if (line == ""):
                    break
                b.append(int(line))
    f.close()

    #generate string SA, SB
    SA = A
    SB = B
    for i in range(0, len(a)):
        new_SA = SA[0:a[i]+1] + SA + SA[a[i]+1:len(SA)]
        SA = new_SA

    for j in range(0, len(b)):
        new_SB = SB[0:b[j]+1] + SB + SB[b[j]+1:len(SB)]
        SB = new_SB

    return SA, SB


if __name__ == "__main__":
    # input file path
#    path = "input.txt"
    path = "mp1.txt"
    # generate input string
    SA, SB = generate_input_string(path)
    with open('myout.txt', 'w') as f:
        f.write(SA)
        f.write("\n")
        f.write(SB)
        f.close()
    # print length of longer string
    MaxStrL = 0
    if len(SA) > len(SB):
        MaxStrL = len(SA)
    else:
        MaxStrL = len(SB)
    print(MaxStrL)
