import textwrap

from .text import get_short_names, join, text_width, wrap_align


class _Node:
    _properties = ['align', 'format', 'wrap', 'missing', 'shorten']

    def __init__(self,
                 key,
                 *,
                 groups=None,
                 display=None,
                 align=None,
                 format=None,
                 wrap=None,
                 missing=None,
                 shorten=None):
        self.key = key
        self.groups = groups
        self.display = key if display is None else display
        for prop in _Node._properties:
            setattr(self, prop, locals()[prop])

    @property
    def depth(self):
        if self.groups is None:
            return 0
        else:
            return 1 + max((child.depth for child in self.groups), default=0)

    def __iter__(self):
        return iter(self.groups)

    def inherit(self, parent):
        updates = {}
        for prop in _Node._properties:
            my_value = getattr(self, prop)
            if my_value is None:
                updates[prop] = getattr(parent, prop)
        return self.update(**updates)

    def update(self, **updates):
        kwargs = {
            'key': self.key,
            'groups': self.groups,
            'display': self.display
        }
        for prop in _Node._properties:
            kwargs[prop] = getattr(self, prop)

        kwargs.update(updates)
        return _Node(**kwargs)

    def __repr__(self):
        repr_parts = []
        if self.display is not None:
            repr_parts.append(self.display)
        if self.key != self.display:
            repr_parts.append(f'key={self.key}')

        for prop in _Node._properties:
            value = getattr(self, prop)
            if value is not None:
                repr_parts.append(f'{prop}={value}')
        if self.key is None:
            name = 'table'
        elif self.groups is None:
            name = 'leaf'
        else:
            name = 'group'
        my_repr = f'{name}'
        if repr_parts:
            my_repr += f'({", ".join(repr_parts)})'
        if self.groups is not None:
            child_reprs = []
            for child in self.groups:
                child_reprs.append(textwrap.indent(repr(child), '  '))
            child_repr = "\n".join(child_reprs)
            my_repr += f':\n{child_repr}'
        return my_repr


def group(key, groups, **kwargs):
    return _Node(key=key, groups=groups, **kwargs)


def leaf(key, format='', **kwargs):
    return _Node(key=key, format=format, **kwargs)


def table(groups, **kwargs):
    return _Node(key=None, groups=groups, **kwargs)


def _treetable_terminal(lines, leaf):
    formatted = []
    for line in lines:
        if line is None:
            content = leaf.missing or ''
        else:
            content = format(line, leaf.format or '')
        formatted.append(content)
    return formatted


def _treetable(lines, group, separators):
    groups = group.groups
    if groups is None:
        return _treetable_terminal(lines, group)

    depth = group.depth
    if depth - 1 >= len(separators):
        raise ValueError(
            'Not enough separators for depth of tree '
            f'(depth is {depth} but got {len(separators)} separators)')

    displays = [child.display for child in groups]

    if group.shorten:
        short_names = get_short_names(displays)
    else:
        short_names = displays
    columns = []
    for child, short_name in zip(groups, short_names):
        child = child.inherit(group)
        if group.shorten:
            assert child.shorten
        child_depth = child.depth
        delta_depth = depth - child_depth
        terminal = child.groups is None
        child_lines = [
            line.get(child.key, None if terminal else {}) for line in lines
        ]
        if terminal:
            child_formatted = _treetable_terminal(child_lines, child)
        else:
            child_formatted = _treetable(
                child_lines, group=child, separators=separators)
        width = max((text_width(line) for line in child_formatted), default=0)
        width = max(width, len(short_name))
        if child.wrap is not None:
            width = min(child.wrap, width)

        if terminal:
            display_name = child.display[:width]
        else:
            display_name = child.display[:width].center(width)

        child_formatted = [''] * (delta_depth - 1) + [display_name
                                                      ] + child_formatted
        child_formatted = [
            wrap_align(line, width=width, alignment=child.align or '<')
            for line in child_formatted
        ]
        for l in child_formatted:
            for c in l.split('\n'):
                assert len(c) == width
        columns.append(child_formatted)
    return join(columns, separator=separators[depth - 1])


def treetable(lines, table, separators=['  ', ' | ', '  ||  ']):
    '''
    Pretty-print `lines` using the `table` structure.

    `separators` give the list of sub-tables separators. It needs to be
    as long as the maximum depth of `groups`. Deepest separators comes first.
    If longer than the maximum depth of `groups`, the first ones will be used.

    '''
    return '\n'.join(
        _treetable(lines=lines, group=table, separators=separators))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
