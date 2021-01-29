# для вебинара 1 Яндекс.Практикум


class Reader:
    def read(self) -> str:
        raise NotImplementedError


class FileReader(Reader):
    def read(self) -> str:
        # read from file
        pass


class StringReader(Reader):
    def __init__(self, string: str):
        self.string = string
        print(f'Input is : {string}')

    def read(self) -> str:
        return self.string


class Compressor:
    def __init__(self, name):
        self.__name = name

    def compress(self, string: str) -> str:
        raise NotImplementedError


class RLECompressor(Compressor):
    def __init__(self, name):
        super().__init__(name)
        self.__prev_char = None
        self.__counter = 1
        self.__result = ''

    def compress(self, string) -> str:
        for ch in string:
            if ch == self.__prev_char:
                self.__counter += 1
            else:
                self.__add_to_result()
                self.__prev_char, self.__counter = ch, 1
        self.__add_to_result()

        return self.__result
    
    def __add_to_result(self):
        if self.__prev_char:
            self.__result += f'{self.__prev_char}{self.__counter}'


class Writer:
    def write(self, string: str):
        raise NotImplementedError


class ConsoleWriter(Writer):
    def write(self, string: str):
        print(f'Result is: {string}')


def compress_string(reader: Reader, compressor: Compressor, writer: Writer):
    origin_string = reader.read()
    compressed_string = compressor.compress(origin_string)
    writer.write(compressed_string)


if __name__ == '__main__':
    r = StringReader('AAAABBBCCCCCDDEEEE')
    c = RLECompressor('RLE Compressor')
    w = ConsoleWriter()
    compress_string(r, c, w)
