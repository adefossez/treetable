# treetable

Helper to pretty print an ascii table with a tree-like structure.

## Installation and requirements

`treetable` requires at least python3.6. This is because I heavily rely on
dictionary preserving the insertion order. I could have forced users to
provide `OrderedDict` but I prefer having this behavior for the builtin
`dict`. For this reason I also allowed myself to use f-strings ;)

`treetable` uses only the standard lib.

```
pip3 install --upgrade git+http://github.com/adefossez/treetable
```


## Quick example

`treetable` allows to easily output complex ascii tables like

```
            ||         ||            metrics
            ||   info  ||     train     |     test
   name     ||  in  s  ||  preci  recal |  auc   accur
xIw         ||  29  S  ||   0.7%  10.5% | 27.2%  96.2%
cLTA        ||  6   n  ||   1.3%  27.7% | 81.1%  21.4%
clCWCDzb    ||  23  B  ||  52.8%  94.3% | 44.8%  58.4%
cSBD        ||  39  N  ||  92.7%  56.6% | 22.2%  46.8%
```

## Usage and example

The main function is `treetable.treetable`. It takes a tree-like structure
to represent the table. For instance, I could have a subtable `info` and
a subtable `metrics`, each one being recursively composed of other subtables.

Each extra level of subtable use a different separator (by default up to 3
levels but you can provide extra separators with the `separators` arguments).

At the leaf level of the tree, a format string (that can be passed to the
`format` builtin) is specified. Let's take an example

```python
groups = {
    'info': { # subtable info
        'name' : 's', # name is an actual column, of type string
        'index': 'd', # and here an int
    },
    'metrics>': { # another subtable
        'speed': '.0f',
        'accuracy': '.1%',
        'special=': '.1f'
    }
}
```

It is possible to specify alignment for a particular column or entire subtable
by adding either `<` (left align), `>` (right align) or `=` (centered)
after its namne. In this case, all the columns in the `metrics` subtable
will be right aligned except for `special` which will be centered.
Subtable header are always centered. Column header are aligned like the
corresponding column.

The lines of the table should be provided following a list of nested
dictionaries with the same shape, for instance:

```python
lines = [
    {'info': {'name': 'bob', 'index': 4}, 'metrics':{'speed': 200, 'accuracy': 0.21, 'special': 0.1}},
    {'info': {'name': 'alice', 'index': 2}, 'metrics':{'speed': 67, 'accuracy': 0.45, 'special': 4.56}},
]
```

Now running `print(treetable(lines, groups))` will give you

```
    info     |          metrics
name   index | speed  accuracy  special
bob    4     |   200     21.0%    0.1
alice  2     |    67     45.0%    4.6
```

`treetable` can automatically shorten columns headers by passing `shorten=True`.
It will use the shortest prefix that is non ambiguous. It won't shorten
the header name more than the width of the data in the corresponding column.
For instance with the previous example you would get:

```
  info   |      metrics
name   i | spee  accur  spec
bob    4 |  200  21.0%  0.1
alice  2 |   67  45.0%  4.6
```

`name` wasn't shortened because `alice` is longer than `name` so there would
be no point in shortening it. However `spec` and `speed` are kept long enough
to avoid ambiguity.


## Documentation
Copied from `treetable.treetable` documentation.

```python
def treetable(lines,
              groups,
              shorten=False,
              missing='',
              default_justify='<',
              separators=['  ', ' | ', '  ||  '],
              line_separator='\n'):
    '''
    Return a `str` representing a tree-like table. `groups` is a dictionary,
    each key, value pair represents a sub-table. The key is the name
    of the sub-table while the value can either be another dict to represent
    another nested sub-table or a format string if we reached a column.

    Similarly, `lines` will follow the same nested dictionary structure
    up to a final object that will be formatted using the builtin `format`
    and the format string obtained from `groups`.

    If `shorten` is True, all the sub-table names will be shortened as much
    as possible to prevent confusion (see `get_short_names` above).
    It won't be shortened more than needed by the content of the sub-table,
    e.g. if the sub-table is wide, then there is no need to shorten
    the name too much.

    `missing` is used when a value is missing.

    `default_justify` is used to justify a value either to the left ('<'),
    right ('>') or centered ('='). This can be overriden using a specific
    syntax in the sub-table name. If the sub-table name ends with one of
    '<', '>', '=', then this will override the default. This suffix will
    be removed from the displayed name. The suffix should only be added in
    `groups`, not `lines`.

    `separators` give the list of sub-tables separators. It needs to be
    as long as the maximum depth of `groups`. Deepest separators comes first.
    If longer than the maximum depth of `groups`, the first ones will be used.

    `line_separator` is used to separate the lines in the table.
    '''
```


## License

`treetable` is distributed under the Unlicense license.
See the LICENSE file for more information.
