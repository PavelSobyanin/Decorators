import os
import datetime


# Задача 1


def logger1(old_function):
    start = datetime.datetime.now()

    def new_function(*args, **kwargs):
        key = f'\r\n{start}, {old_function}, {args}, {kwargs}, '

        with open('main.log', 'a') as main_list:
            main_list.write(key)
            result = old_function(*args, **kwargs)
            main_list.write(f'{result} \r\n')

        return result

    return new_function


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger1
    def hello_world():
        return 'Hello World'

    @logger1
    def summator(a, b=0):
        return a + b

    @logger1
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


# Задача 2

def logger(path):
    def _logger(old_function):
        print(old_function)
        PATH = path
        print(PATH)
        start = datetime.datetime.now()

        def new_function(*args, **kwargs):
            print(123)
            key = f'\r\n{start}, {old_function}, {args}, {kwargs}, '
            print(key)
            with open(PATH, 'a+') as main_list:
                main_list.write(key)
                result = old_function(*args, **kwargs)
                main_list.write(f'{result} \r\n')
            return result

        return new_function

    return _logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


# Задача 3

@logger1
def flat_generator(list_of_lists):
    cur = 0
    cur_1 = 0
    while cur < len(list_of_lists):
        result = list_of_lists[cur][cur_1]

        if cur_1 + 1 < len(list_of_lists[cur]):
            cur_1 += 1
        else:
            cur_1 = 0
            cur += 1
        yield result


if __name__ == '__main__':
    test_1()
    test_2()

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    flat_generator(list_of_lists_1)