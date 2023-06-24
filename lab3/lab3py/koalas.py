from csv import reader


class DataFrame:
    def __init__(self, data):
        self._dataset = data
        self.features = data[0][:-1]
        self.x_train = [lst[:-1] for lst in data[1:]]
        self.y_train = [x[-1] for x in data[1:]]

    def print_df(self):
        print(*self._dataset[0])
        for index, items in dict(enumerate(self._dataset[1:])).items():
            print(index, *items)


def read_csv(file_path: str) -> DataFrame:
    tmp = []
    with open(file_path) as f:
        for row in reader(f):
            tmp.append(row)
    return DataFrame(tmp)
