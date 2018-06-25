import StringIO


import cat


def test_read_single():
  f = StringIO.StringIO('''\
Line 1
Line 2
Line 3
''')
  g = cat.read(128, f)
  assert g.next() == '''\
Line 1
Line 2
Line 3
'''


def test_read_multiple():
  f = StringIO.StringIO('''\
Line 1
Line 2
Line 3
''')
  g = cat.read(7, f)
  assert g.next() == 'Line 1\n'
  assert g.next() == 'Line 2\n'
  assert g.next() == 'Line 3\n'


def test_expandendoflines():
  g = cat.expandendoflines([ 'huey\n',
                             'dewey',
                             'louie\n' ])
  assert g.next() == 'huey$\n'
  assert g.next() == 'dewey'
  assert g.next() == 'louie$\n'


def test_expandtabs():
  g = cat.expandtabs([ 'huey\tdewey',
                       '\t\tlouie' ])
  assert g.next() == 'huey^Idewey'
  assert g.next() == '^I^Ilouie'


def test_expandnonprintables():
  g = cat.expandnonprintables([ 'huey\001dewey',
                                '\002\003louie' ])
  assert g.next() == 'huey^Adewey'
  assert g.next() == '^B^Clouie'


def test_write():
  f = StringIO.StringIO()
  cat.write(f, [ 'huey\n',
                 'dewey',
                 'louie\n' ])
  assert f.getvalue() == 'huey\ndewey louie\n'


def test_parseargv_noarguments():
  assert cat.parseargv([], {}) == \
                       ( [], {} )


def test_parseargv_combinedoptions():
  assert cat.parseargv([ '-v', 'filename' ], {}) == \
                       (
                         [ 'filename' ],
                         { 'v': True }
                       )
  assert cat.parseargv([ '-ve', 'filename' ], {}) == \
                       (
                         [ 'filename' ],
                         { 'v': True, 'e': True }
                       )
  assert cat.parseargv([ '-vet', 'filename' ], {}) == \
                       (
                         [ 'filename' ],
                         { 'v': True, 'e': True, 't': True }
                       )


def test_parseargv_separateoptions():
  assert cat.parseargv([ '-v', 'filename' ], {}) == \
                       (
                         [ 'filename' ],
                         { 'v': True }
                       )
  assert cat.parseargv([ '-v' , '-e', 'filename' ], {}) == \
                       (
                         [ 'filename' ],
                         { 'v': True, 'e': True }
                       )
  assert cat.parseargv([ '-v', '-e', '-t', 'filename' ], {}) == \
                       (
                         [ 'filename' ],
                         { 'v': True, 'e': True, 't': True }
                       )
