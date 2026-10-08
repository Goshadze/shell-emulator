# Shell Emulator

Эмулятор оболочки UNIX-подобной ОС с графическим интерфейсом (Python, tkinter).

## Описание

Окно с полем вывода и строкой ввода. Заголовок окна содержит имя VFS.

## Функции

- Парсер команд с поддержкой аргументов в кавычках (`"a b"`, `'a b'`).
- Сообщения об ошибках: неизвестная команда, неверные аргументы,
  незакрытая кавычка.
- Команды:
  - `ls [args...]` - заглушка, выводит имя и аргументы
  - `cd [args...]` - заглушка, выводит имя и аргументы
  - `exit` - завершение работы эмулятора

## Настройки

Параметры командной строки (при запуске их значения выводятся в окно
с пометкой `[debug]`):

- `--vfs PATH` - путь к физическому расположению VFS
- `--script PATH` - путь к стартовому скрипту

Стартовый скрипт - текстовый файл, по одной команде эмулятора в строке.
Команды выполняются последовательно, ввод и вывод отображаются в окне.
При первой ошибке выполнение останавливается и выводится сообщение
с номером строки.

## Запуск

Требуется Python 3 с tkinter.

```sh
./run.sh [--vfs PATH] [--script PATH]
```

Скрипты проверки параметров командной строки:

```sh
tests/params_vfs.sh
tests/params_script.sh
tests/params_all.sh
```

## Примеры

```
$ ls
ls: args=[]
$ cd "my dir" /tmp
cd: args=['my dir', '/tmp']
$ foo
foo: command not found
$ ls "oops
parse error: No closing quotation
$ exit 1
exit: too many arguments
$ exit
```

Запуск со стартовым скриптом `tests/emu/error.txt`:

```
$ ./run.sh --script tests/emu/error.txt
[debug] vfs=None
[debug] script=tests/emu/error.txt
$ ls
ls: args=[]
$ foo
foo: command not found
script: error at line 2
```
