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
  - `vfs-info` - имя загруженной VFS и SHA-256 хеш её данных

## Настройки

Параметры командной строки (при запуске их значения выводятся в окно
с пометкой `[debug]`):

- `--vfs PATH` - путь к CSV-файлу VFS (по умолчанию пустая VFS `vfs`)
- `--script PATH` - путь к стартовому скрипту

Стартовый скрипт - текстовый файл, по одной команде эмулятора в строке.
Команды выполняются последовательно, ввод и вывод отображаются в окне.
При первой ошибке выполнение останавливается и выводится сообщение
с номером строки.

## VFS

VFS загружается из CSV-файла целиком в память, файл не распаковывается.
Имя VFS - имя CSV-файла, оно выводится в заголовке окна. Колонки:

- `path` - полный путь элемента; вложенность задаётся путём
  (`/docs/notes/todo.txt`)
- `type` - `dir` или `file`
- `content` - содержимое файла в base64 (для папок пусто)

```
path,type,content
/hello.txt,file,aGVsbG8K
/docs,dir,
/docs/readme.txt,file,cmVhZG1lCg==
```

Ошибка загрузки (файл не найден, неверный формат) выводится в окно,
эмулятор продолжает работу с пустой VFS.

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

Скрипты проверки VFS и всех команд:

```sh
tests/vfs_variants.sh
tests/vfs_errors.sh
tests/all_commands.sh
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

```
$ vfs-info
name: min.csv
sha256: 34b4377a9fbb9e382d6a9cd879f3768d3714b0e4bf1955e5ea46d0575df64b13
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
