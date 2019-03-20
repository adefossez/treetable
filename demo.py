from treetable import treetable, table, group, leaf

mytable = table([
    group('info', [leaf('name'), leaf('index')]),
    group(
        'metrics',
        align='>',
        groups=[
            leaf('speed', '.0f'),
            leaf('accuracy', '.1%'),
            leaf('special', '.1%', align='=')
        ]),
])

lines = [
    {
        'info': {
            'name': 'bob',
            'index': 4
        },
        'metrics': {
            'speed': 200,
            'accuracy': 0.21,
            'special': 0.1
        }
    },
    {
        'info': {
            'name': 'alice',
            'index': 2
        },
        'metrics': {
            'speed': 67,
            'accuracy': 0.45,
            'special': 4.56
        }
    },
]

colors = ['30', '39']

print(treetable(lines, mytable, colors=colors))
mytable.shorten = True
print("shortened version:")
print(treetable(lines, mytable, colors=colors))

# wrapping columns
mytable.groups[0].groups[0].wrap = 3
print(treetable(lines, mytable))
