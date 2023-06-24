class Clause:
    def __init__(self, literali, index, stvoren=(None, None)):
        self.literali = literali
        self.stvoren_od = stvoren
        self.index = index

    def __str__(self):
        ret = ""
        ret += f"{self.index}. "
        for i in range(len(self.literali)):
            ret += str(self.literali[i])
            if i != len(self.literali) - 1:
                ret += " v "
        if self.stvoren_od:
            ret += f"({self.stvoren_od[0]}, {self.stvoren_od[1]})"
        return ret


class Literal:
    def __init__(self, literal):
        if literal[0] == "~":
            self.negacija = True
            self.ime_literala = literal[1:]
        else:
            self.negacija = False
            self.ime_literala = literal

    def __eq__(self, other):
        return True if self.ime_literala == other.ime_literala and \
                       self.negacija == other.negacija else False

    def __hash__(self):
        return hash(self.ime_literala + str(self.negacija))

    def __str__(self):
        return self.ime_literala if not self.negacija \
            else f"~{self.ime_literala}"

    def komplement(self, other):
        return True if self.ime_literala == other.ime_literala and \
                        self.negacija != other.negacija else False
