# Interpreter

## Requirements
* Python 3.8
* [PLY (Python Lex-Yacc)](https://www.dabeaz.com/ply/)
* [NumPy](https://numpy.org/)
* [pytest](https://docs.pytest.org/en/stable/)
* [Flake8](https://flake8.pycqa.org/en/latest/)

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python main.py examples/fibonacci.m
```
Windows:
```bash
type examples\fibonacci.m | python main.py
```
Linux:
```bash
cat examples/fibonacci.m | python main.py
```

## Examples
```
$ python main.py
   1 |  n = 3;
   2 |  A = eye(n);
   3 |  print A;
   4 |  ^Z
[[1. 0. 0.]
 [0. 1. 0.]
 [0. 0. 1.]]
```

```
$ python main.py examples/fibonacci.m
1
1
2
3
5
8
13
21
34
55
89
...
```

```
$ python main.py examples/primes.m
2
3
5
7
11
13
17
...
```

```
$ python main.py examples/sqrt.m
1, 1.0
2, 1.414213562373095
3, 1.7320508075688772
4, 2.0
5, 2.23606797749979
6, 2.449489742783178
7, 2.6457513110645907
8, 2.82842712474619
9, 3.0
```

```
$ python main.py examples/triangle.m
*
**
***
****
*****
******
*******
********
*********
**********
```

## Pipeline

### Parser

### Scanner

### Treeprinter

### Typechecker

### Interpreter
