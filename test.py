from treetable import treetable, table, group, leaf
import random
import string


def _gen_line(group):
    if group.groups is None:
        format_ = group.format
        if format_ is None or 's' in format_:
            size = format_.rstrip('s')
            if size:
                size = int(size)
            else:
                size = random.randrange(4, 16)
            return ''.join(
                random.choice(string.ascii_letters) for _ in range(size))
        if 'd' in format_:
            return random.randrange(50)
        elif '%' in format_:
            return random.random()
        else:
            raise ValueError(f"Don't know how to handle format {format_}")
    else:
        return {group.key: _gen_line(group) for group in group.groups}


def print_groups(table, num_lines=4):
    lines = []
    for _ in range(num_lines):
        lines.append(_gen_line(table))
    print(treetable(lines, table))
    print()
    print(treetable(lines, table.update(shorten=True)))
    print()


mytable = table([
    leaf('name', 's', wrap=7),
    group('info',
          [leaf('index', 'd'), leaf('status', '1s')]),
    group(
        'metrics',
        align='>',
        groups=[
            group('train', [
                leaf('precision', '.1%', display='P//'),
                leaf('recall', '.1%')
            ]),
            group('test', [leaf('auc', '.1%'),
                           leaf('accuracy', '.1%')])
        ])
])

print(repr(mytable))
print_groups(mytable)
print_groups(mytable, 0)

mytable.groups.append(group('plop', []))
print_groups(mytable)

groups = {
    'info': {
        'index': 'd',
        'status': '1s',
    },
    'metrics>': {
        'precision': '.1%',
        'recall': '.1%',
    }
}
mytable = table([
    group('info',
          [leaf('index', 'd'), leaf('status', '1s')]),
    group('metrics', [leaf('precision', '.1%'),
                      leaf('recall', '.1%')])
])
print_groups(mytable)
