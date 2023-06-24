# Takoder sam koristio svoja proslogodisnja rjesenja koja 
# ne rade bas najsretnije :'(
import re
import sys
from functools import reduce
from operator import and_

import logic


def cnf_convert(klauzula):
    ret = []
    for x in klauzula:
        x.negacija = not x.negacija
        ret.append([x])
    return ret


def select_clauses(klauzule):
    ret = []
    key = klauzule[-1]
    brojac = 1
    for x in klauzule[:-1]:
        ret.append((key, x, brojac, len(klauzule)))
        brojac += 1

    return ret


def pl_resolve(c1c2):
    if len(c1c2[0]) == 1 == len(c1c2[1]) and c1c2[0][0].komplement(c1c2[1][0]):
        return "NIL"

    res = []
    for x in c1c2[0]:
        for y in c1c2[1]:
            if x.komplement(y):
                tmp = c1c2[0] + c1c2[1]
                tmp.remove(x)
                tmp.remove(y)
                res.append(tmp)
    return res


def print_nil(klauzule, kombinacija):
    kl = dict(enumerate(klauzule, 1))
    for k, v in kl.items():
        klauzula = logic.Clause(v, k, kombinacija)
        print(klauzula)


def pl_resolution(kl, zadnja):
    klauzule = kl[:-1] + cnf_convert(kl[-1])
    new = []

    for k, v in dict(enumerate(klauzule, 1)).items():
        print(f"{k}. ", end="")
        for i in range(len(v)):
            print(str(v[i]), end="")
            if i != len(v) - 1:
                print(" v ", end="")
        print()
    print("===============")

    index = len(klauzule) + 1

    while True:
        for c1c2 in select_clauses(klauzule):
            rezolventi = pl_resolve(c1c2[:2])
            if rezolventi:
                if "NIL" == rezolventi:
                    print(f"{index}. NIL ({c1c2[2]}, {c1c2[3] - 1})")
                    print("===============")
                    print(f"[CONCLUSION]: {zadnja} is true")
                    return True
                for x in rezolventi:
                    print(f"{index}. {x[0]} {c1c2[2:]}")
                    index += 1
                new += rezolventi
        try:
            if reduce(and_, [i in klauzule for i in new]):
                return False
        except TypeError:
            return False
        klauzule += new


def main():
    if sys.argv[1] == 'resolution':  # drugi argument je putanja do datoteke
        with open(sys.argv[2], encoding='utf-8') as f:
            data = [re.sub('^#.*', '', x.strip().lower()) for x in f if
                    re.sub('^#.*', '', x)]
        zadnja = data[-1]
        klauzule = []
        for linija in data:
            tmp = []
            if linija:
                x = linija.split(" v ")
                for y in x:
                    tmp.append(logic.Literal(y))
                klauzule.append(tmp)

        if not pl_resolution(klauzule, zadnja):
            print(f"[CONCLUSION]: {zadnja} is unknown")
    elif sys.argv[1] == 'cooking':
        with open(sys.argv[2]) as f:
            popis_klauzula = [re.sub('^#.*', "", x.strip().lower()) for x in f if
                              re.sub('^#.*', "", x)]

        klauzule = []
        for linija in popis_klauzula:
            if linija:
                x = linija.split(" v ")
                tmp = []
                for y in x:
                    tmp.append(logic.Literal(y))
                klauzule.append(tmp)

        with open(sys.argv[3]) as f:
            popis_kor_nar = [re.sub('^#.*', '', x.strip().lower()) for x in f if
                             re.sub('^#.*', '', x)]

        for naredba in popis_kor_nar:
            zadnja, znak = naredba.split()
            print(f"User's command: {zadnja} {znak}")
            if znak == "?":
                klauzule.append([logic.Literal(zadnja)])
                if not pl_resolution(klauzule, zadnja):
                    print(f"[CONCLUSION]: {zadnja} is unknown\n")
            elif znak == "-":
                try:
                    klauzule.remove([logic.Literal(zadnja)])
                except ValueError:
                    continue
                print(f"Removed {zadnja}\n")
            elif znak == "+":
                klauzule.append([logic.Literal(zadnja)])
                print(f"Removed {zadnja}\n")

    else:
        print("Oops, invalid task name!")
        exit(0)


if __name__ == '__main__':
    main()
