class Encoding:
    def __init__(self, path):
        self.dict = {}
        with open(path) as file:
            for line in file.readlines():
                line = line.strip()
                if line.startswith("#"): continue
                if line == "": continue
                cell = line[:9]
                literal = line[9:].strip().strip("\"")
                cell = int("".join([str(cell[int(i)]) for i in "35746801"])[::-1], 2)
                self.dict[literal] = cell

    def encode(self, string):
        return "".join([chr(0x2800 + self.dict[char]) for char in string])
    
    def decodeByte(self, byte):
        for key, value in self.dict.items():
            if value == byte: return key
        return ""