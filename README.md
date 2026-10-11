# Shell Emulator

Эмулятор оболочки UNIX-подобной ОС с графическим интерфейсом (Python, tkinter).

## Описание

Окно с полем вывода и строкой ввода. Заголовок окна содержит имя VFS,
приглашение ввода содержит текущую папку (`/docs$`).

## Функции

- Парсер команд с поддержкой аргументов в кавычках (`"a b"`, `'a b'`).
- Сообщения об ошибках: неизвестная команда, неверные аргументы,
  незакрытая кавычка.
- Команды:
  - `ls [-l] [path]` - содержимое папки (по умолчанию текущей) или имя файла;
    с `-l` выводит тип (`d` - папка, `-` - файл), владельца и имя
  - `cd [path]` - смена текущей папки (без аргумента - `/`), поддерживаются
    абсолютные и относительные пути, `.` и `..`
  - `cat path...` - вывод содержимого файлов
  - `chown owner path...` - смена владельца; изменение выполняется только
    в памяти, CSV-файл не меняется
  - `cal [[month] year]` - календарь на текущий месяц, на год (`cal 2024`)
    или на месяц года (`cal 2 2024`)
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
- `owner` - владелец (необязательная колонка, по умолчанию `root`)

```
path,type,content,owner
/hello.txt,file,aGVsbG8K,root
/docs,dir,,root
/docs/readme.txt,file,cmVhZG1lCg==,alice
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
/$ ls
bin
docs
hello.txt
/$ cd docs/notes
/docs/notes$ ls
deep
todo.txt
/docs/notes$ cat todo.txt
todo
/docs/notes$ cd ../..
/$ cal 2 2024
   February 2024
Su Mo Tu We Th Fr Sa
             1  2  3
 4  5  6  7  8  9 10
11 12 13 14 15 16 17
18 19 20 21 22 23 24
25 26 27 28 29
/$ ls -l
d root bin
d root docs
- root hello.txt
/$ chown bob hello.txt /docs
/$ ls -l
d root bin
d bob docs
- bob hello.txt
/$ vfs-info
name: nested.csv
sha256: b2a2bfaa2b4c797cae5616e343e82846cbacce31313ebb49cae87d63e5476b82
```

Ошибки:

```
/$ foo
foo: command not found
/$ cd /nope
cd: /nope: no such file or directory
/$ cat /docs
cat: /docs: is a directory
/$ chown alice /missing
chown: /missing: no such file or directory
/$ ls "oops
parse error: No closing quotation
/$ exit 1
exit: too many arguments
```

Запуск со стартовым скриптом `tests/emu/error.txt`:

```
$ ./run.sh --script tests/emu/error.txt
[debug] vfs=None
[debug] script=tests/emu/error.txt
/$ ls
/$ foo
foo: command not found
script: error at line 2
```
