Implemented tests
=================

The following tests are currently implemented:

* *File testing*: The file tests simply check if files with appropriate filenames are produced by the executing program. It takes all files from the reference directory and looks if the output of the test namelist produce the same filenames. No content is checked!
* *MD5 checksum*: To check if the content of two files are similar, the `MD5 checksum <http://en.wikipedia.org/wiki/MD5>`_ is used. *Note, that this is not ensuring that the files are identical, but are very similar*. Problems with MD5 checksums can occur when comparing e.g. postscript files. These typically always differ in their header and therefore produce different checksums. The user can therefore exclude specific filetypes from the comparison.
* *Check filesize:* The size of two files is compared.
* *Check filesize > 0 bytes*: Check that all output files are at least greater than 0 bytes in size (non empty files)
* *Check file content:* compares the content of two files. This is currenlty supported for the following formats
 * *netcdf*
  - comparison of variable names
  - comparison of similarity of data fields

The following tests are planned for future implementations:

* *graphic file content*: It is planned to implement a test that compares the similarity between graphic files.
