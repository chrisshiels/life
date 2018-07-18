import StringIO
import sys


import cat


def test_pipe():
  def add1(x):
    return x + 1

  assert cat.pipe([ add1, add1, add1 ])(0) == 3


def test_partial():
  def add(x, y):
    return x + y

  add1 = cat.partial(add, 1)

  assert add1(1) == 2


def test_read():
  f = StringIO.StringIO('''\
Line 1
Line 2
Line 3
''')
  g = cat.read(f)
  assert g.next() == 'Line 1\n'
  assert g.next() == 'Line 2\n'
  assert g.next() == 'Line 3\n'


def test_removerepeatedemptylines():
  g = cat.removerepeatedemptylines([ 'huey\n',
                                     '\n',
                                     '\n',
                                     'dewey\n',
                                     '\n',
                                     '\n',
                                     '\n',
                                     '\n',
                                     'louie\n' ])
  assert g.next() == 'huey\n'
  assert g.next() == '\n'
  assert g.next() == 'dewey\n'
  assert g.next() == '\n'
  assert g.next() == 'louie\n'


def test_expandendoflines():
  g = cat.expandendoflines([ 'huey\n',
                             'dewey\n',
                             'louie\n' ])
  assert g.next() == 'huey$\n'
  assert g.next() == 'dewey$\n'
  assert g.next() == 'louie$\n'


def test_expandtabs():
  g = cat.expandtabs([ 'huey\tdewey\n',
                       '\t\tlouie\n' ])
  assert g.next() == 'huey^Idewey\n'
  assert g.next() == '^I^Ilouie\n'


def test_expandnonprintables():
  g = cat.expandnonprintables([ 'huey\001dewey\n',
                                '\002\003louie\n' ])
  assert g.next() == 'huey^Adewey\n'
  assert g.next() == '^B^Clouie\n'


def test_prependlinenumbers():
  g = cat.prependlinenumbers([ 'huey\n',
                               'dewey\n',
                               'louie\n' ])
  assert g.next() == '     1\thuey\n'
  assert g.next() == '     2\tdewey\n'
  assert g.next() == '     3\tlouie\n'


def test_write():
  f = StringIO.StringIO()
  cat.write(f, [ 'huey\n',
                 'dewey\n',
                 'louie\n' ])
  assert f.getvalue() == 'huey\ndewey\nlouie\n'


def test_parseargs_noarguments():
  assert cat.parseargs({}, []) == \
                       ( {}, [] )


def test_parseargs_combinedoptions():
  assert cat.parseargs({}, [ '-v', 'filename' ]) == \
                       (
                         { 'v': True },
                         [ 'filename' ]
                       )
  assert cat.parseargs({}, [ '-ve', 'filename' ]) == \
                       (
                         { 'v': True, 'e': True },
                         [ 'filename' ]
                       )
  assert cat.parseargs({}, [ '-vet', 'filename' ]) == \
                       (
                         { 'v': True, 'e': True, 't': True },
                         [ 'filename' ]
                       )


def test_parseargs_separateoptions():
  assert cat.parseargs({}, [ '-v', 'filename' ]) == \
                       (
                         { 'v': True },
                         [ 'filename' ]
                       )
  assert cat.parseargs({}, [ '-v' , '-e', 'filename' ]) == \
                       (
                         { 'v': True, 'e': True },
                         [ 'filename' ]
                       )
  assert cat.parseargs({}, [ '-v', '-e', '-t', 'filename' ]) == \
                       (
                         { 'v': True, 'e': True, 't': True },
                         [ 'filename' ]
                       )


def test_pipelineget():
  assert cat.expandendoflines not in cat.pipelineget({}, sys.stdout)
  assert cat.expandendoflines in cat.pipelineget({ 'e': True }, sys.stdout)

  assert cat.expandtabs not in cat.pipelineget({}, sys.stdout)
  assert cat.expandtabs in cat.pipelineget({ 't': True }, sys.stdout)

  assert cat.expandnonprintables not in cat.pipelineget({}, sys.stdout)
  assert cat.expandnonprintables in cat.pipelineget({ 'e': True }, sys.stdout)
  assert cat.expandnonprintables in cat.pipelineget({ 't': True }, sys.stdout)
  assert cat.expandnonprintables in cat.pipelineget({ 'v': True }, sys.stdout)
