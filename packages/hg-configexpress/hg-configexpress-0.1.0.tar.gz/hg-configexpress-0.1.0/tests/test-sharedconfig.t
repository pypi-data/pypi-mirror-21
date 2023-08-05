#require killdaemons

prepare serverhook to show config that was sent
  $ cat >> serverhook.py << EOF
  > def ourserverhook(ui, repo, **kwargs):
  >     for (k, v) in sorted(kwargs.items()):
  >         if k == 'hgversion' or k.startswith('config_'):
  >             print('hookarg: %s - %s' % (k, v))
  >     return True
  > EOF
  $ export PYTHONPATH=$TESTTMP:$PYTHONPATH

  $ cat >> $HGRCPATH << EOF
  > [ui]
  > ssh=python "$RUNTESTDIR/dummyssh"
  > [extensions]
  > configexpress = $(dirname $TESTDIR)/hgext3rd/configexpress.py
  > [section_a]
  > entry1 = foo
  > entry2 = barbar
  > [section_b]
  > someentry = sometext
  > otherentry = test
  > EOF

setup repo
  $ hg init clientrepo
  $ cd clientrepo
  $ echo a > a
  $ hg add a
  $ hg commit -ma
  $ echo b > b
  $ hg add b
  $ hg commit -mb
  $ cd ..

setup server
  $ hg clone -U clientrepo serverrepo
  $ cat >> serverhgrc << EOF
  > [hooks]
  > pretxnchangegroup.serverhook = printenv.py serverhook 1 log
  > EOF
  $ cp serverhgrc serverrepo/.hg/hgrc

create additional change on the client side
  $ cd clientrepo
  $ echo c > c
  $ hg add c
  $ hg commit -mc
  $ cd ..

check push to the server without extra config options
  $ hg -R clientrepo push ssh://user@dummy/$TESTTMP/serverrepo
  pushing to ssh://user@dummy/$TESTTMP/serverrepo
  searching for changes
  remote: adding changesets
  remote: adding manifests
  remote: adding file changes
  remote: added 1 changesets with 1 changes to 1 files
  remote: transaction abort!
  remote: rollback completed
  remote: pretxnchangegroup.serverhook hook exited with status 1
  abort: push failed on remote
  [255]

For compat with hg-4.2, we have two alternative lines

  $ cat serverrepo/log && rm serverrepo/log
  serverhook hook: HG_BUNDLE2=1 HG_CLIENTCONFIG_HGVERSION=* HG_NODE=177f92b773850b59254aa5e923436f921b55483b HG_NODE_LAST=177f92b773850b59254aa5e923436f921b55483b HG_PENDING=$TESTTMP/serverrepo HG_SOURCE=serve HG_TXNID=TXN:* HG_URL=remote:ssh:127.0.0.1 (glob) (?)
  serverhook hook: HG_BUNDLE2=1 HG_CLIENTCONFIG_HGVERSION=* HG_HOOKNAME=pretxnchangegroup.serverhook HG_HOOKTYPE=pretxnchangegroup HG_NODE=177f92b773850b59254aa5e923436f921b55483b HG_NODE_LAST=177f92b773850b59254aa5e923436f921b55483b HG_PENDING=$TESTTMP/serverrepo HG_SOURCE=serve HG_TXNID=TXN:$ID$ HG_URL=remote:ssh:$LOCALIP (glob) (?)

check push to the server with additional config options sent
  $ cat >> $HGRCPATH << EOF
  > [configexpress:client2server]
  > listofentries = section_a.entry2 section_b.someentry nonexistingsection.entry
  > EOF
  $ hg -R clientrepo push ssh://user@dummy/$TESTTMP/serverrepo
  pushing to ssh://user@dummy/$TESTTMP/serverrepo
  searching for changes
  remote: adding changesets
  remote: adding manifests
  remote: adding file changes
  remote: added 1 changesets with 1 changes to 1 files
  remote: transaction abort!
  remote: rollback completed
  remote: pretxnchangegroup.serverhook hook exited with status 1
  abort: push failed on remote
  [255]

For compat with hg-4.2, we have two alternative lines

  $ cat serverrepo/log && rm serverrepo/log
  serverhook hook: HG_BUNDLE2=1 HG_CLIENTCONFIG_HGVERSION=* HG_CLIENTCONFIG_SECTION_A__ENTRY2=barbar HG_CLIENTCONFIG_SECTION_B__SOMEENTRY=sometext HG_NODE=177f92b773850b59254aa5e923436f921b55483b HG_NODE_LAST=177f92b773850b59254aa5e923436f921b55483b HG_PENDING=$TESTTMP/serverrepo HG_SOURCE=serve HG_TXNID=TXN:* HG_URL=remote:ssh:127.0.0.1 (glob) (?)
  serverhook hook: HG_BUNDLE2=1 HG_CLIENTCONFIG_HGVERSION=* HG_CLIENTCONFIG_SECTION_A__ENTRY2=barbar HG_CLIENTCONFIG_SECTION_B__SOMEENTRY=sometext HG_HOOKNAME=pretxnchangegroup.serverhook HG_HOOKTYPE=pretxnchangegroup HG_NODE=177f92b773850b59254aa5e923436f921b55483b HG_NODE_LAST=177f92b773850b59254aa5e923436f921b55483b HG_PENDING=$TESTTMP/serverrepo HG_SOURCE=serve HG_TXNID=TXN:$ID$ HG_URL=remote:ssh:$LOCALIP (glob) (?)

check push from a client that doesn't have the extension,
which should result in no extra hookargs
  $ hg -R clientrepo --config extensions.configexpress=! push ssh://user@dummy/$TESTTMP/serverrepo
  pushing to ssh://user@dummy/$TESTTMP/serverrepo
  searching for changes
  remote: this server recommends using the 'configexpress' extension
  remote: adding changesets
  remote: adding manifests
  remote: adding file changes
  remote: added 1 changesets with 1 changes to 1 files
  remote: transaction abort!
  remote: rollback completed
  remote: pretxnchangegroup.serverhook hook exited with status 1
  abort: push failed on remote
  [255]

For compat with hg-4.2, we have two alternative lines

  $ cat serverrepo/log && rm serverrepo/log
  serverhook hook: HG_BUNDLE2=1 HG_NODE=177f92b773850b59254aa5e923436f921b55483b HG_NODE_LAST=177f92b773850b59254aa5e923436f921b55483b HG_PENDING=$TESTTMP/serverrepo HG_SOURCE=serve HG_TXNID=TXN:* HG_URL=remote:ssh:127.0.0.1 (glob) (?)
  serverhook hook: HG_BUNDLE2=1 HG_HOOKNAME=pretxnchangegroup.serverhook HG_HOOKTYPE=pretxnchangegroup HG_NODE=177f92b773850b59254aa5e923436f921b55483b HG_NODE_LAST=177f92b773850b59254aa5e923436f921b55483b HG_PENDING=$TESTTMP/serverrepo HG_SOURCE=serve HG_TXNID=TXN:$ID$ HG_URL=remote:ssh:$LOCALIP (?)

check push to a server that doesn't have the extension
  $ cat >> serverrepo/.hg/hgrc << EOF
  > [extensions]
  > configexpress = !
  > EOF
  $ hg -R clientrepo push ssh://user@dummy/$TESTTMP/serverrepo
  pushing to ssh://user@dummy/$TESTTMP/serverrepo
  searching for changes
  remote: adding changesets
  remote: adding manifests
  remote: adding file changes
  remote: added 1 changesets with 1 changes to 1 files
  remote: transaction abort!
  remote: rollback completed
  remote: pretxnchangegroup.serverhook hook exited with status 1
  abort: push failed on remote
  [255]

For compat with hg-4.2, we have two alternative lines

  $ cat serverrepo/log && rm serverrepo/log
  serverhook hook: HG_BUNDLE2=1 HG_NODE=177f92b773850b59254aa5e923436f921b55483b HG_NODE_LAST=177f92b773850b59254aa5e923436f921b55483b HG_PENDING=$TESTTMP/serverrepo HG_SOURCE=serve HG_TXNID=TXN:* HG_URL=remote:ssh:127.0.0.1 (glob) (?)
  serverhook hook: HG_BUNDLE2=1 HG_HOOKNAME=pretxnchangegroup.serverhook HG_HOOKTYPE=pretxnchangegroup HG_NODE=177f92b773850b59254aa5e923436f921b55483b HG_NODE_LAST=177f92b773850b59254aa5e923436f921b55483b HG_PENDING=$TESTTMP/serverrepo HG_SOURCE=serve HG_TXNID=TXN:$ID$ HG_URL=remote:ssh:$LOCALIP (?)
  $ cp serverhgrc serverrepo/.hg/hgrc

check pull from a server
  $ hg clone clientrepo serverrepo2
  updating to branch default
  3 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ echo a > serverrepo2/a2
  $ hg -R serverrepo2 add serverrepo2/a2
  $ hg -R serverrepo2 commit -m "add a"
  $ cat >> serverrepo2/.hg/hgrc << EOF
  > [configexpress:server2client]
  > fooconfig = configproposal
  > EOF

(check for unknown proposed config)
  $ hg -R clientrepo pull serverrepo2
  pulling from serverrepo2
  searching for changes
  configexpress: proposedconfig not found: $TESTTMP/serverrepo2/.hg/configproposal
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  (run 'hg update' to get a working copy)

  $ cat >> serverrepo2/.hg/configproposal << EOF
  > [extensions]
  > rebase =
  > histedit =
  > [section_a]
  > entry1 = foo
  > entry2 = barbarbarbar
  > EOF
  $ hg -R clientrepo pull serverrepo2
  pulling from serverrepo2
  searching for changes
  no changes found
  server suggests the following config changes:
    [extensions]
    histedit=
    rebase=
    [section_a]
    entry2=barbarbarbar
  this will overwrite these current user configurations:
    [section_a]
    entry2=barbar
  apply these changes to your repository config file (yn)?  y
  $ hg -R clientrepo/ config extensions.histedit
  
  $ hg -R clientrepo/ config extensions.rebase
  
  $ hg -R clientrepo/ config section_a.entry2
  barbarbarbar
  $ cat clientrepo/.hg/hgrc
  # This "%include" enables config from the configexpress extension. keep at end of file
  %include ./hgrc-ext-config-express.rc
  $ cat clientrepo/.hg/hgrc-ext-config-express.rc
  # this file is managed by the configexpress extension
  # /!\ do not edit /!\
  %include ./hgrc-ext-config-express/fooconfig.rc
  $ cat clientrepo/.hg/hgrc-ext-config-express/fooconfig.rc
  # this file is managed by the configexpress extension
  # /!\ do not edit /!\
  [extensions]
  rebase =
  histedit =
  [section_a]
  entry1 = foo
  entry2 = barbarbarbar
  $ hg -R clientrepo pull serverrepo2
  pulling from serverrepo2
  searching for changes
  no changes found

(also test absolute import)

  $ cat >> serverrepo2/.hg/hgrc << EOF
  > [configexpress:server2client]
  > fooconfig = $TESTTMP/serverrepo2/.hg/configproposal
  > fooconfig:location = user
  > EOF
  $ cat >> serverrepo2/.hg/configproposal << EOF
  > [extensions]
  > foo =
  > rebase = !
  > EOF
  $ hg -R clientrepo pull serverrepo2
  pulling from serverrepo2
  searching for changes
  no changes found
  server suggests the following config changes:
    [extensions]
    foo=
    rebase=!
  this will overwrite these current user configurations:
    [extensions]
    rebase=
  apply these changes to your repository config file (yn)?  y
