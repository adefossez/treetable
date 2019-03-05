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


def text_width(text):
    return max((len(line) for line in text.split('\n')), default=0)


def wrap(text, width, tabwidth=4):
    text = text.replace('\t', ' ' * tabwidth)
    if not text:
        yield ''
        return
    for index in range(0, len(text), width):
        yield text[index:index + width]


def align(text, width, alignment):
    if alignment == '=':
        return text.center(width)
    elif alignment == '<':
        return text.ljust(width)
    elif alignment == '>':
        return text.rjust(width)
    else:
        raise ValueError(f'Invalid value for align {alignment}')


def wrap_align(text, width=None, alignment='<'):
    '''
    Return value justified to the given width, either
    to the left if align is '<', to the right if it is '>' or centered
    if it is '='.
    '''
    lines = text.split('\n')
    width = max(map(len, lines)) if width is None else width
    lines = [sub_line for line in lines for sub_line in wrap(line, width)]
    return '\n'.join(
        align(line, width=width, alignment=alignment) for line in lines)


def join(columns, separator=''):
    widths = [len(column[0].split('\n', 1)[0]) for column in columns]
    joined = []
    for rows in zip(*columns):
        rows_lines = [row.split('\n') for row in rows]
        height = max(map(len, rows_lines))
        rows_lines = [
            row_lines + [' ' * width] * (height - len(row_lines))
            for row_lines, width in zip(rows_lines, widths)
        ]
        joined_row = []
        for lines in zip(*rows_lines):
            joined_row.append(separator.join(lines))
        joined.append('\n'.join(joined_row))
    return joined
