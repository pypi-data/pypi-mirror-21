Test scenario where we enforce (or encourage) client to have the extension.

  $ cat >> $HGRCPATH << EOF
  > [ui]
  > ssh=python "$RUNTESTDIR/dummyssh"
  > EOF

Basic setup
-----------

  $ hg init server
  $ hg clone --quiet ssh://user@dummy/server/ client-noext
  $ hg clone --quiet ssh://user@dummy/server/ client-pull-noext
  $ hg clone --quiet ssh://user@dummy/server/ client-ext
  $ hg clone --quiet ssh://user@dummy/server/ client-pull-ext
  $ cat >> server/.hg/hgrc << EOF
  > [extensions]
  > configexpress = $(dirname $TESTDIR)/hgext3rd/configexpress.py
  > EOF
  $ cat >> client-ext/.hg/hgrc << EOF
  > [extensions]
  > configexpress = $(dirname $TESTDIR)/hgext3rd/configexpress.py
  > EOF
  $ cat >> client-pull-ext/.hg/hgrc << EOF
  > [extensions]
  > configexpress = $(dirname $TESTDIR)/hgext3rd/configexpress.py
  > EOF

  $ cd server
  $ echo z > z
  $ hg add z
  $ hg commit -m 'Z0'
  $ cd ..

Exchange from a client with the extension
-----------------------------------------

  $ cd client-ext
  $ hg pull
  pulling from ssh://user@dummy/server/
  requesting all changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  (run 'hg update' to get a working copy)
  $ hg update
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ echo a > a
  $ hg add a
  $ hg commit -m 'A0'
  $ hg push
  pushing to ssh://user@dummy/server/
  searching for changes
  remote: adding changesets
  remote: adding manifests
  remote: adding file changes
  remote: added 1 changesets with 1 changes to 1 files

Exchange from a client without the extension
-------------------------------------------

  $ cd ../client-noext
  $ hg pull
  pulling from ssh://user@dummy/server/
  requesting all changes
  remote: this server recommends using the 'configexpress' extension
  adding changesets
  adding manifests
  adding file changes
  added 2 changesets with 2 changes to 2 files
  (run 'hg update' to get a working copy)
  $ hg update
  2 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ echo b > b
  $ hg add b
  $ hg commit -m 'B0'
  $ hg push
  pushing to ssh://user@dummy/server/
  searching for changes
  remote: this server recommends using the 'configexpress' extension
  remote: adding changesets
  remote: adding manifests
  remote: adding file changes
  remote: added 1 changesets with 1 changes to 1 files
  $ cd ..

Test Cloning
------------

  $ hg clone ssh://user@dummy/server clone-ext --config "extensions.configexpress=$(dirname $TESTDIR)/hgext3rd/configexpress.py"
  requesting all changes
  adding changesets
  adding manifests
  adding file changes
  added 3 changesets with 3 changes to 3 files
  updating to branch default
  3 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg clone ssh://user@dummy/server clone-noext
  requesting all changes
  remote: this server recommends using the 'configexpress' extension
  adding changesets
  adding manifests
  adding file changes
  added 3 changesets with 3 changes to 3 files
  updating to branch default
  3 files updated, 0 files merged, 0 files removed, 0 files unresolved

Configure the enforcement policy
--------------------------------

ignore

  $ cd client-noext
  $ cat >> ../server/.hg/hgrc << EOF
  > [configexpress]
  > enforce = ignore
  > EOF
  $ echo b >> b
  $ hg commit -m C0
  $ hg push
  pushing to ssh://user@dummy/server/
  searching for changes
  remote: adding changesets
  remote: adding manifests
  remote: adding file changes
  remote: added 1 changesets with 1 changes to 1 files
  $ hg -R ../client-pull-noext pull -r 0
  pulling from ssh://user@dummy/server/
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  (run 'hg update' to get a working copy)
  $ hg -R ../client-pull-ext pull -r 0
  pulling from ssh://user@dummy/server/
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  (run 'hg update' to get a working copy)

warn

  $ echo enforce = warning >> ../server/.hg/hgrc
  $ echo b >> b
  $ hg commit -m D0
  $ hg push
  pushing to ssh://user@dummy/server/
  searching for changes
  remote: this server recommends using the 'configexpress' extension
  remote: adding changesets
  remote: adding manifests
  remote: adding file changes
  remote: added 1 changesets with 1 changes to 1 files
  $ hg -R ../client-pull-noext pull -r 1
  pulling from ssh://user@dummy/server/
  searching for changes
  remote: this server recommends using the 'configexpress' extension
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  (run 'hg update' to get a working copy)
  $ hg -R ../client-pull-ext pull -r 1
  pulling from ssh://user@dummy/server/
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  (run 'hg update' to get a working copy)

custom warning

  $ echo enforcewarningmsg = a different warning >> ../server/.hg/hgrc
  $ hg -R ../client-pull-noext pull -r 1
  pulling from ssh://user@dummy/server/
  no changes found
  remote: a different warning

abort

  $ echo enforce = abort >> ../server/.hg/hgrc
  $ echo b >> b
  $ hg commit -m E0
  $ hg push
  pushing to ssh://user@dummy/server/
  searching for changes
  remote: this server requires the 'configexpress' extension
  abort: push failed on remote
  [255]
  $ hg -R ../client-pull-noext pull -r 2
  pulling from ssh://user@dummy/server/
  searching for changes
  remote: abort: this server requires the 'configexpress' extension
  abort: pull failed on remote
  [255]
  $ hg -R ../client-pull-ext pull -r 2
  pulling from ssh://user@dummy/server/
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  (run 'hg update' to get a working copy)

custom abort

  $ cp ../server/.hg/hgrc ../server/.hg/hgrc.backup
  $ echo enforceabortmsg = a different abort >> ../server/.hg/hgrc
  $ hg -R ../client-pull-noext pull -r 2
  pulling from ssh://user@dummy/server/
  searching for changes
  remote: abort: a different abort
  abort: pull failed on remote
  [255]
  $ echo enforceabortmsg = A very long abort message >> ../server/.hg/hgrc
  $ echo " message that has too much text, which" >> ../server/.hg/hgrc
  $ echo " previously caused a cut-off abort" >> ../server/.hg/hgrc
  $ echo " message to appear. We now handle" >> ../server/.hg/hgrc
  $ echo " this issue by no longer placing" >> ../server/.hg/hgrc
  $ echo " the full text in the exception," >> ../server/.hg/hgrc
  $ echo " but showing a warning message." >> ../server/.hg/hgrc
  $ hg -R ../client-pull-noext pull -r 2
  pulling from ssh://user@dummy/server/
  searching for changes
  remote: A very long abort message
  remote: message that has too much text, which
  remote: previously caused a cut-off abort
  remote: message to appear. We now handle
  remote: this issue by no longer placing
  remote: the full text in the exception,
  remote: but showing a warning message.
  remote:     - - -
  remote: abort: A very long abort message
  message that has too much text, which
  previously cause...
  abort: pull failed on remote
  [255]
  $ mv ../server/.hg/hgrc.backup ../server/.hg/hgrc

unknown

  $ echo enforce = someunknownconfigvalue >> ../server/.hg/hgrc
  $ echo b >> b
  $ hg commit -m F0
  $ hg push
  pushing to ssh://user@dummy/server/
  searching for changes
  remote: unknown value for 'configexpress.enforce': someunknownconfigvalue
  remote: adding changesets
  remote: adding manifests
  remote: adding file changes
  remote: added 2 changesets with 2 changes to 1 files
  $ hg -R ../client-pull-noext pull -r 3
  pulling from ssh://user@dummy/server/
  searching for changes
  remote: unknown value for 'configexpress.enforce': someunknownconfigvalue
  adding changesets
  adding manifests
  adding file changes
  added 2 changesets with 2 changes to 1 files
  (run 'hg update' to get a working copy)
  $ hg -R ../client-pull-ext pull -r 3
  pulling from ssh://user@dummy/server/
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  (run 'hg update' to get a working copy)
  $ cd ..

#if serve

Basic HTTP testing
------------------

warning parts

  $ echo enforce = warning >> server/.hg/hgrc
  $ hg -R server serve -p $HGPORT -d --pid-file=hg.pid -E error.log
  $ cat hg.pid >> $DAEMON_PIDS
  $ hg clone http://localhost:$HGPORT/ http-clone-noext-warn
  requesting all changes
  adding changesets
  adding manifests
  adding file changes
  added 7 changesets with 7 changes to 3 files
  updating to branch default
  3 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ ${RUNTESTDIR}/killdaemons.py

  $ echo enforce = abort >> server/.hg/hgrc
  $ hg -R server serve -p $HGPORT -d --pid-file=hg1.pid -E error.log
  $ cat hg1.pid >> $DAEMON_PIDS
  $ hg clone http://localhost:$HGPORT/ http-clone-noext-abort
  requesting all changes
  remote: abort: this server requires the 'configexpress' extension
  abort: pull failed on remote
  [255]
  $ ${RUNTESTDIR}/killdaemons.py

#endif
