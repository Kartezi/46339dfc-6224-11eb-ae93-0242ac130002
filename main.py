"""
Для вебинара ООП Яндекс.Практикум
"""




class Reader:
    """
    это базовый класс, мы не будем и не планируем создавать экземпляры его класса, мы его используем для создания классов
    потомков
    """
    def read(self) -> str:
        # у всех классов-потомков будет такой же метод и они обязаны его реализовать
        # иначе будет происходить NotImplementedError при вызове read() у объекта
        raise NotImplementedError


class FileReader(Reader):
    """
    это класс-потомок, он реализует чтение строки из файла (я не буду писать реализацию, предположим что она есть :))
    """
    def read(self) -> str:
        # типа читаем из файла...
        string = "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOP"
        print(f'FileReader, Входящая строка: {string}')
        return string


class StringReader(Reader):
    """
    это класс-потомок, он просто принимает на вход строку и в методе read возвращает его. С точки зрения бизнес-логики
    это бесполезный класс, но нам главное понять принцип ООП на его примере.
    """
    def __init__(self, string: str):
        # self.string и string это разные переменные!
        self.string = string
        print(f'StringReader, Входящая строка: {string}')  # или можно print(f'Input is : {self.string}'), так как они имеют одинаковое значение

    def read(self) -> str:
        return self.string


# --------------------


class Compressor:
    """
    это базовый класс, мы не будем и не планируем создавать экземпляры его класса, мы его используем для создания классов
    потомков
    """
    def __init__(self, tag):
        # допустим мы хотим как-то пометить тегом компрессор и решили делать это через
        # конструктор базового класса
        # __tag значит что это приватное свойство класса Compressor, оно недолжно быть доступно классам потомкам
        self.__tag = tag

    def compress(self, string: str) -> str:
        raise NotImplementedError


class RLECompressor(Compressor):
    def __init__(self, tag):
        super().__init__(tag)    # так как у базового класса есть явный конструктор, то мы должны вызвать его здесь тоже явно

        # это все приватные поля, скрывающие детали реализации, мы не хотим чтоб они были доступны снаружи
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
    
    def __add_to_result(self):  # это приватный метод, должен использоваться только внутри класса RLECompressor как вспомогательный метод
        if self.__prev_char:
            self.__result += f'{self.__prev_char}{self.__counter}'

    def reset(self):  # это публичная функция, которую мы явно вызовем, чтобы сбросить все значения компрессора на начальные
        self.__prev_char = None
        self.__counter = 1
        self.__result = ''


# --------------------


class Writer:
    """
    это базовый класс, мы не будем и не планируем создавать экземпляры его класса, мы его используем для создания классов
    потомков
    """
    def write(self, string: str):
        raise NotImplementedError


class ConsoleWriter(Writer):
    def write(self, string: str):
        print(f'Результат: {string}')  # пишем в консольку


# --------------------


# эта функция - главная звезда программы
# принимает на вход reader, который должен быть объектом класса-потомка Reader
# тоже самое с compressor и writer
# функция абстрагируется от конкретной реализации ридера, компрессора и райтера
# Таким образом ей можно подставлять любой ридер (лишь бы он был отнаследован от Reader (или его потомков))
# и тоже самое про компрессор и райтер
def compress_string(reader: Reader, compressor: Compressor, writer: Writer):
    origin_string = reader.read()
    compressed_string = compressor.compress(origin_string)
    writer.write(compressed_string)


# этот блок кода исполнится только если данный модуль main.py будет вызываться как главный модуль (а не как импортнутый)
if __name__ == '__main__':  # если имя модуля программы является главным, то исполняем код этого блока
    # создаем два разных ридера
    string_reader = StringReader('AAAABBBCCCCCDDEEEE')
    file_reader = FileReader()

    # создаем один компрессор
    rle_compressor = RLECompressor('TAG_NAME_BEST_COMPRESSOR')

    # создаем один райтер
    console_writer = ConsoleWriter()

    # компрессим данные из string_reader и пишем в консоль
    compress_string(string_reader, rle_compressor, console_writer)

    # явно вызываем публичную функцию чтоб сбросить значения на начальные
    rle_compressor.reset()

    # компрессим данные из file_reader и пишем в консоль
    compress_string(file_reader, rle_compressor, console_writer)
