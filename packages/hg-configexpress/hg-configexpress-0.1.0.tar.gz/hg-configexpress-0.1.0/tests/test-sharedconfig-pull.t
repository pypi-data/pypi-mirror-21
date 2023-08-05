Test pulling config from the server

Basic config
------------

  $ cat >> $HGRCPATH << EOF
  > [extensions]
  > configexpress = $(dirname $TESTDIR)/hgext3rd/configexpress.py
  > EOF

  $ hg init server
  $ hg clone server client_a
  updating to branch default
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg clone server client_b
  updating to branch default
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ mkdir server/.hg/config-express.server/
  $ cat >> server/.hg/config-express.server/foo << EOF
  > [section_a]
  > entry-one = Babar
  > entry-two = Celeste
  > [section_b]
  > some.entry = some text
  > other.entry = Other/Text
  > EOF
  $ cat >> server/.hg/hgrc << EOF
  > [configexpress:server2client]
  > fooconfig = config-express.server/foo
  > EOF

simple pull
-----------

  $ cd client_a
  $ hg pull
  pulling from $TESTTMP/server
  no changes found
  server suggests the following config changes:
    [section_a]
    entry-one=Babar
    entry-two=Celeste
    [section_b]
    other.entry=Other/Text
    some.entry=some text
  apply these changes to your repository config file (yn)?  y
  $ hg config | grep "section_" | sort
  section_a.entry-one=Babar
  section_a.entry-two=Celeste
  section_b.other.entry=Other/Text
  section_b.some.entry=some text

(re match for < hg-4.1.1)

  $ cat .hg/hgrc
  # example repository config (see 'hg help config' for more info)
  [paths]
  default = $TESTTMP/server
  
  # path aliases to other clones of this repo in URLs or filesystem paths
  # (see 'hg help config.paths' for more info)
  #
  # default(-push|:pushurl) = ssh://jdoe@example.net/hg/jdoes-fork (re)
  # my-fork      (   )?= ssh://jdoe@example.net/hg/jdoes-fork (re)
  # my-clone     (   )?= /home/jdoe/jdoes-clone (re)
  
  [ui]
  # name and email (local to this repository, optional), e.g.
  # username = Jane Doe <jdoe@example.com>
  # This "%include" enables config from the configexpress extension. keep at end of file
  %include ./hgrc-ext-config-express.rc
  $ cat .hg/hgrc-ext-config-express.rc
  # this file is managed by the configexpress extension
  # /!\ do not edit /!\
  %include ./hgrc-ext-config-express/fooconfig.rc
  $ ls .hg/hgrc-ext-config-express/
  fooconfig.rc

pulling a new entry
-------------------

  $ cat >> ../server/.hg/config-express.server/bar << EOF
  > [section_c]
  > south = west
  > north = east
  > [section_d]
  > hot = cold
  > low = high
  > EOF
  $ cat >> ../server/.hg/hgrc << EOF
  > [configexpress:server2client]
  > barconfig = config-express.server/bar
  > EOF
  $ hg pull
  pulling from $TESTTMP/server
  no changes found
  server suggests the following config changes:
    [section_c]
    north=east
    south=west
    [section_d]
    hot=cold
    low=high
  apply these changes to your repository config file (yn)?  y
  $ hg config | grep "section_" | sort
  section_a.entry-one=Babar
  section_a.entry-two=Celeste
  section_b.other.entry=Other/Text
  section_b.some.entry=some text
  section_c.north=east
  section_c.south=west
  section_d.hot=cold
  section_d.low=high

(re match for < hg-4.1.1)

  $ cat .hg/hgrc
  # example repository config (see 'hg help config' for more info)
  [paths]
  default = $TESTTMP/server
  
  # path aliases to other clones of this repo in URLs or filesystem paths
  # (see 'hg help config.paths' for more info)
  #
  # default(-push|:pushurl) = ssh://jdoe@example.net/hg/jdoes-fork (re)
  # my-fork      (   )?= ssh://jdoe@example.net/hg/jdoes-fork (re)
  # my-clone     (   )?= /home/jdoe/jdoes-clone (re)
  
  [ui]
  # name and email (local to this repository, optional), e.g.
  # username = Jane Doe <jdoe@example.com>
  # This "%include" enables config from the configexpress extension. keep at end of file
  %include ./hgrc-ext-config-express.rc
  $ cat .hg/hgrc-ext-config-express.rc
  # this file is managed by the configexpress extension
  # /!\ do not edit /!\
  %include ./hgrc-ext-config-express/barconfig.rc
  %include ./hgrc-ext-config-express/fooconfig.rc
  $ ls .hg/hgrc-ext-config-express/
  barconfig.rc
  fooconfig.rc
  $ cd ..

pulling multiple entry
----------------------

  $ cd client_b
  $ hg pull
  pulling from $TESTTMP/server
  no changes found
  server suggests the following config changes:
    [section_c]
    north=east
    south=west
    [section_d]
    hot=cold
    low=high
  apply these changes to your repository config file (yn)?  y
  server suggests the following config changes:
    [section_a]
    entry-one=Babar
    entry-two=Celeste
    [section_b]
    other.entry=Other/Text
    some.entry=some text
  apply these changes to your repository config file (yn)?  y
  $ hg config | grep section_ | sort
  section_a.entry-one=Babar
  section_a.entry-two=Celeste
  section_b.other.entry=Other/Text
  section_b.some.entry=some text
  section_c.north=east
  section_c.south=west
  section_d.hot=cold
  section_d.low=high

(re match for < hg-4.1.1)

  $ cat .hg/hgrc
  # example repository config (see 'hg help config' for more info)
  [paths]
  default = $TESTTMP/server
  
  # path aliases to other clones of this repo in URLs or filesystem paths
  # (see 'hg help config.paths' for more info)
  #
  # default(-push|:pushurl) = ssh://jdoe@example.net/hg/jdoes-fork (re)
  # my-fork      (   )?= ssh://jdoe@example.net/hg/jdoes-fork (re)
  # my-clone     (   )?= /home/jdoe/jdoes-clone (re)
  
  [ui]
  # name and email (local to this repository, optional), e.g.
  # username = Jane Doe <jdoe@example.com>
  # This "%include" enables config from the configexpress extension. keep at end of file
  %include ./hgrc-ext-config-express.rc
  $ cat .hg/hgrc-ext-config-express.rc
  # this file is managed by the configexpress extension
  # /!\ do not edit /!\
  %include ./hgrc-ext-config-express/barconfig.rc
  %include ./hgrc-ext-config-express/fooconfig.rc
  $ ls .hg/hgrc-ext-config-express/
  barconfig.rc
  fooconfig.rc

entries updated on server
-------------------------

  $ cat > ../server/.hg/config-express.server/foo << EOF
  > [section_a]
  > entry-one = Zephir
  > entry-two = Arthur
  > [section_b]
  > any.entry = bar
  > other.entry = foo
  > EOF
  $ cat > ../server/.hg/config-express.server/bar << EOF
  > [section_e]
  > south = west
  > north = east
  > [section_f]
  > hot = cold
  > low = high
  > EOF
  $ hg pull
  pulling from $TESTTMP/server
  no changes found
  server suggests the following config changes:
    [section_e]
    north=east
    south=west
    [section_f]
    hot=cold
    low=high
  apply these changes to your repository config file (yn)?  y
  server suggests the following config changes:
    [section_a]
    entry-one=Zephir
    entry-two=Arthur
    [section_b]
    any.entry=bar
    other.entry=foo
  this will overwrite these current user configurations:
    [section_a]
    entry-one=Babar
    entry-two=Celeste
    [section_b]
    other.entry=Other/Text
  apply these changes to your repository config file (yn)?  y

  $ hg config | grep section_
  section_a.entry-one=Zephir
  section_a.entry-two=Arthur
  section_b.any.entry=bar
  section_b.other.entry=foo
  section_e.south=west
  section_e.north=east
  section_f.hot=cold
  section_f.low=high

(re match for < hg-4.1.1)

  $ cat .hg/hgrc
  # example repository config (see 'hg help config' for more info)
  [paths]
  default = $TESTTMP/server
  
  # path aliases to other clones of this repo in URLs or filesystem paths
  # (see 'hg help config.paths' for more info)
  #
  # default(-push|:pushurl) = ssh://jdoe@example.net/hg/jdoes-fork (re)
  # my-fork      (   )?= ssh://jdoe@example.net/hg/jdoes-fork (re)
  # my-clone     (   )?= /home/jdoe/jdoes-clone (re)
  
  [ui]
  # name and email (local to this repository, optional), e.g.
  # username = Jane Doe <jdoe@example.com>
  # This "%include" enables config from the configexpress extension. keep at end of file
  %include ./hgrc-ext-config-express.rc
  $ cat .hg/hgrc-ext-config-express.rc
  # this file is managed by the configexpress extension
  # /!\ do not edit /!\
  %include ./hgrc-ext-config-express/barconfig.rc
  %include ./hgrc-ext-config-express/fooconfig.rc
  $ ls .hg/hgrc-ext-config-express/
  barconfig.rc
  fooconfig.rc

entries removed on server
-------------------------

Drop the one of the config entry

  $ grep -v barconfig ../server/.hg/hgrc > $TESTTMP/tmphgrc
  $ cp $TESTTMP/tmphgrc ../server/.hg/hgrc

dropped config no longer enforced on the client
(not sure about the behavior, especially the part where we do not ask the user)

  $ hg pull
  pulling from $TESTTMP/server
  no changes found

  $ hg config | grep section_
  section_a.entry-one=Zephir
  section_a.entry-two=Arthur
  section_b.any.entry=bar
  section_b.other.entry=foo

(re match for < hg-4.1.1)

  $ cat .hg/hgrc
  # example repository config (see 'hg help config' for more info)
  [paths]
  default = $TESTTMP/server
  
  # path aliases to other clones of this repo in URLs or filesystem paths
  # (see 'hg help config.paths' for more info)
  #
  # default(-push|:pushurl) = ssh://jdoe@example.net/hg/jdoes-fork (re)
  # my-fork      (   )?= ssh://jdoe@example.net/hg/jdoes-fork (re)
  # my-clone     (   )?= /home/jdoe/jdoes-clone (re)
  
  [ui]
  # name and email (local to this repository, optional), e.g.
  # username = Jane Doe <jdoe@example.com>
  # This "%include" enables config from the configexpress extension. keep at end of file
  %include ./hgrc-ext-config-express.rc
  $ cat .hg/hgrc-ext-config-express.rc
  # this file is managed by the configexpress extension
  # /!\ do not edit /!\
  %include ./hgrc-ext-config-express/fooconfig.rc
  $ ls .hg/hgrc-ext-config-express/
  barconfig.rc
  fooconfig.rc
