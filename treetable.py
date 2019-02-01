# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org/>

from collections import defaultdict


def get_short_names(names):
    '''
    Given an iterable names, return the shortest prefix for each element
    so that all prefixes are different. All elements in names must be unique.
    
    >>> get_short_names(['cat', 'castor', 'could', 'fire', 'first'])
    ['cat', 'cas', 'co', 'fire', 'firs']

    '''
    lengths = {name: 1 for name in names}
    if len(lengths) != len(names):
        raise ValueError('names must only contain unique values')
    while True:
        buckets = defaultdict(list)
        valid = True
        for name in names:
            bucket = buckets[name[:lengths[name]]]
            if bucket:
                valid = False
            bucket.append(name)
        for bucket in buckets.values():
            if len(bucket) > 1:
                for name in bucket:
                    lengths[name] += 1
        if valid:
            break
    return [name[:lengths[name]] for name in names]


def _get_name_justify(name, default='<'):
    if name:
        for justify in ['<', '=', '>']:
            if name[-1] == justify:
                return name[:-1], justify
    return name, default


def justified(value, width, justify):
    '''
    Return value justified to the given width, either 
    to the left if justify is '<', to the right if it is '>' or centered
    if it is '='.
    '''
    if justify == '=':
        return value.center(width)
    elif justify == '<':
        return value.ljust(width)
    elif justify == '>':
        return value.rjust(width)
    else:
        raise ValueError(f'Invalid value for justify {justify}')


def _treetable_terminal(lines, format_, missing):
    formatted = []
    for line in lines:
        if line is None:
            formatted.append(missing)
        else:
            formatted.append(format(line, format_))
    return formatted


def _tree_depth(groups):
    if isinstance(groups, dict):
        return 1 + max(
            (_tree_depth(group) for group in groups.values()), default=0)
    else:
        return 0


def _treetable(lines, groups, shorten, missing, default_justify, separators):
    depth = _tree_depth(groups)
    if depth - 1 >= len(separators):
        raise ValueError(
            'Not enough separators for depth of tree '
            f'(depth is {depth} but got {len(separators)} separators)')
    if shorten:
        short_names = get_short_names(groups.keys())
    else:
        short_names = groups.keys()

    columns = []
    for (name, group), short_name in zip(groups.items(), short_names):
        group_depth = _tree_depth(group)
        delta_depth = depth - group_depth
        terminal = not isinstance(group, dict)
        name, justify = _get_name_justify(name, default_justify)
        group_lines = [
            line.get(name, None if terminal else {}) for line in lines
        ]
        if terminal:
            group_formatted = _treetable_terminal(group_lines, group, missing)
        else:
            group_formatted = _treetable(group_lines, group, shorten, missing,
                                         justify, separators)
            justify = '<'
        width = max(
            len(short_name),
            max((len(line) for line in group_formatted), default=0))
        if not group:
            group_formatted = ['' for _ in lines]
        group_formatted = [
            justified(line, width, justify) for line in group_formatted
        ]
        display_name = name[:width].center(width)

        group_formatted = [' ' * width] * (
            delta_depth - 1) + [display_name] + group_formatted
        columns.append(group_formatted)

    return [separators[depth - 1].join(line) for line in zip(*columns)]


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

    return line_separator.join(
        _treetable(lines, groups, shorten, missing, default_justify,
                   separators))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
