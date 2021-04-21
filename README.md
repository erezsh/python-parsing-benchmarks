# Python Parsing Benchmarks

This repository contains a suite of test cases and implementations for
parsing text using Python. Both speed an memory usage are compared for
each implementation. Each implementation must be:

* **Correct** -- it implements the specification exactly
  - Syntax -- it parses all valid inputs and rejects bad ones
  - Semantics -- it produces the expected data structures
* **Plausible** -- it only uses generally known parser features or
  parsing strategies

Validation tests can ensure the correctness of an implementation, but
its plausibility is harder to pin down. Basically, grammars that
require knowlege of a parser's internals or undocumented features to
increase performance are discouraged. The grammar should be
understandable by someone with access to the parser's documentation
and examples.


## Implementations

This table lists the tasks performed and the libraries benchmarked.

| Implementation | Algorithm           | [JSON]                   | [Arithmetic]             | [INI]             |
| -------------- | ------------------- | ------------------------ | ---------------------    | -------           |
| [stdlib]       | handwritten         | [yes][stdlib-json]       | [yes][stdlib-arithmetic] | [yes][stdlib-ini] |
| [Lark]         | [LALR]              | [yes][Lark-json]         | [yes][lark-arithmetic]   | [yes][lark-ini]   |
| [parsimonious] | [Recursive Descent] | [yes][parsimonious-json] |                          |                   |
| [pe]           | [Recursive Descent] | [yes][pe-json]           | [yes][pe-arithmetic]     | [yes][pe-ini]     |
| [pyparsing]    | [Recursive Descent] | [yes][pyparsing-json]    |                          |                   |
| [SLY]          | [LALR]              | [yes][SLY-json]          |                          |                   |
| [textX]        | [Recursive Descent] | [yes][textx-json]        |                          |                   |


[stdlib]: https://docs.python.org/3/
[Lark]: https://github.com/lark-parser/lark
[parsimonious]: https://github.com/erikrose/parsimonious
[pe]: https://github.com/goodmami/pe
[pyparsing]: https://github.com/pyparsing/pyparsing/
[SLY]: https://github.com/dabeaz/sly/
[textX]: https://github.com/textX/textX/

[JSON]: tasks/json.md
[Arithmetic]: tasks/arithmetic.md
[INI]: tasks/ini.md

[stdlib-json]: bench/stdlib/json.py
[Lark-json]: bench/lark/json.py
[parsimonious-json]: bench/parsimonious/json.py
[pe-json]: bench/pe/json.py
[pyparsing-json]: bench/pyparsing/json.py
[SLY-json]: bench/sly/json.py
[textx-json]: bench/textx/json.py

[stdlib-arithmetic]: bench/stdlib/arithmetic.py
[Lark-arithmetic]: bench/lark/arithmetic.py
[pe-arithmetic]: bench/pe/arithmetic.py

[stdlib-ini]: bench/stdlib/ini.py
[Lark-ini]: bench/lark/ini.py
[pe-ini]: bench/pe/ini.py

[LALR]: https://en.wikipedia.org/wiki/LALR_parser
[Recursive Descent]: https://en.wikipedia.org/wiki/Recursive_descent_parser

## Results

The following bar chart shows the time in milliseconds to parse a ~5MB
JSON file using both CPython and PyPy.

```
[cpython] stdlib      : ▏ 63 ms
[cpython] pe          : ▇▇▇▇▇ 1646 ms
[cpython] sly         : ▇▇▇▇▇▇▇▇▇▇▇▇ 3693 ms
[cpython] lark        : ▇▇▇▇▇▇▇▇▇▇▇▇▇ 3817 ms
[cpython] parsimonious: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 7590 ms
[cpython] pyparsing   : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 11560 ms
[cpython] textx       : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 14309 ms
[pypy]    stdlib      : ▏ 268 ms
[pypy]    sly         : ▇▇ 630 ms
[pypy]    lark        : ▇▇ 651 ms
[pypy]    pe          : ▇▇ 663 ms
[pypy]    pyparsing   : ▇▇▇▇▇▇▇ 2085 ms
[pypy]    parsimonious: ▇▇▇▇▇▇▇▇▇ 2821 ms
[pypy]    textx       : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 5653 ms
```

Here are the results for parsing 10k complicated (from a parsing point
of view) arithmetic expressions:


```
[cpython] stdlib: ▇▇ 104 ms
[cpython] pe    : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 1908 ms
[cpython] lark  : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 2113 ms
[pypy]    stdlib: ▇▇▇▇▇ 212 ms
[pypy]    lark  : ▇▇▇▇▇ 217 ms
[pypy]    pe    : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 712 ms
```

And here is an INI file with 1000 sections:

```
[cpython] stdlib: ▇▇▇▇▇▇▇▇▇▇ 71 ms
[cpython] pe    : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 146 ms
[cpython] lark  : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 338 ms
[pypy]    stdlib: ▇▇▇ 25 ms
[pypy]    lark  : ▇▇▇▇▇▇ 47 ms
[pypy]    pe    : ▇▇▇▇▇▇▇ 54 ms
```


*Charts produced with [termgraph](https://github.com/mkaz/termgraph)*

These benchmarks were run on a Lenovo Thinkpad with an Intel Core-i5
6200U with 24GB memory running Pop!_OS Linux 18.04. The millisecond
values will change across systems but the relative performance should
be similar (but I'd be interested in hearing if you find otherwise!).

## Setup

Python 3.6+ is required.

First create a virtual environment (recommended) and install the
package and requirements:

``` console
$ python3 -m venv cpy
$ source cpy/bin/activate
(cpy) $ pip install -r requirements.txt
```

You can also use PyPy by creating its own virtual environment:

``` console
$ pypy3 -m venv pypy
$ source pypy/bin/activate
(pypy) $ pip install -r requirements.txt
```

From here on it's assumed you're in one of the `(cpy)` or `(pypy)` environments.

## Run Benchmarks

The benchmarks are implemented using [pytest](https://pytest.org) and
[pytest-benchmark](https://github.com/ionelmc/pytest-benchmark), so
you can run the tests with `pytest` if you adjust `PYTHONPATH`:

``` console
$ PYTHONPATH=. pytest
```

But it might be easier to just run the included `validate.py` and
`benchmark.py` scripts, which pass the appropriate options on to
`pytest`:

``` console
$ python validate.py            # skip performance tests (they take a while)
$ python benchmark.py           # skip validity tests
```

You can give specific library names to limit the tests that are run:

``` console
$ python validate.py pe stdlib  # only run validation for pe and stdlib
```

Some tests print to stdout diagnostic information that can be useful,
such as the recursion limit in JSON parsing. Use the following option to see that information:

``` console
$ python validate.py -rP        # print stdout for each test
```


## Disclaimer

Performance benchmarks are not the only criterion one should use when
choosing a parsing library, and this repository is not meant to
declare some winner. On the one hand, there are many other valid
criteria (ease of use, stability, security, availability, support,
etc.), but on the other hand we can't discuss relative performance
without numbers, so here we are.
