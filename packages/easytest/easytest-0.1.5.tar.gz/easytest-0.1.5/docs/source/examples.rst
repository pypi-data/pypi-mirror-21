Examples
========

The following examples illustrate how to use `easytest`

Comparison of directory contents
--------------------------------

The following code compares the content of two directories. The reference directory is passed recursively and it is checked if all files that exist in the reference directory are also present in the target directory:

.. code:: python

  import sys
  from easytest import EasyTest

  # as we choose here the source and data directory to be the same all checks suceed!
  rdir = '/some/reference/directory'
  tdir = '/some/target/directory'

  T = EasyTest(None, refdirectory=rdir, output_directory=tdir)
  T.run_tests(files='all', checksum_files='all')

Two kind of tests are performed in this example:
 a) check for file existence
 b) check for file content using MD5 checksums for all files
