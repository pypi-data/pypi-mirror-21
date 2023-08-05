====================================
Testing head checking code: Case A-6
====================================

Mercurial checks for the introduction of multiple heads on push. Evolution
comes into play to detect if existing heads on the server are being replaced by
some of the new heads we push.

This test file is part of a series of tests checking this behavior.

Category A: checking simple case invoving a branch being superceeded by another.
TestCase 6: multi-changeset branch, split on multiple other, (base on its own branch)

.. old-state:
..
.. * 2 branch (1 changeset, and 2 changesets)
..
.. new-state:
..
.. * 1 new branch superceeding the base of the old-2-changesets-branch,
.. * 1 new changesets on the old-1-changeset-branch superceeding the head of the other
..
.. expected-result:
..
.. * push allowed
..
.. graph-summary:
..
.. B'◔⇢ø B
..   | |
.. A | ø⇠◔ A'
..   | |/
.. C ● |
..    \|
..     ●

  $ . $TESTDIR/testlib/checkheads-util.sh

Test setup
----------

  $ setuprepos
  creating basic server and client repo
  updating to branch default
  2 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ cd server
  $ mkcommit B0
  $ hg up 0
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ mkcommit C0
  created new head
  $ cd ../client
  $ hg pull
  pulling from $TESTTMP/server
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 2 changesets with 2 changes to 2 files (+1 heads)
  (run 'hg heads' to see heads, 'hg merge' to merge)
  $ hg up 0
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ mkcommit A1
  created new head
  $ hg up 'desc(C0)'
  1 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ mkcommit B1
  $ hg debugobsolete `getid "desc(A0)" ` `getid "desc(A1)"`
  $ hg debugobsolete `getid "desc(B0)" ` `getid "desc(B1)"`
  $ hg log -G --hidden
  @  d70a1f75a020 (draft): B1
  |
  | o  f6082bc4ffef (draft): A1
  | |
  o |  0f88766e02d6 (draft): C0
  |/
  | x  d73caddc5533 (draft): B0
  | |
  | x  8aaa48160adc (draft): A0
  |/
  o  1e4be0697311 (public): root
  


Actual testing
--------------

  $ hg push
  pushing to $TESTTMP/server
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 2 changesets with 2 changes to 2 files (+1 heads)
  2 new obsolescence markers
