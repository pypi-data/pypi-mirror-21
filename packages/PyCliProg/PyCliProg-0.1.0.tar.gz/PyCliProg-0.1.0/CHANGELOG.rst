Change Log For PyCliProg
========================


PyCliProg 0.1.0 - 2017-03-30
----------------------------

``0.1.0`` is the first public pre-release.

- Added names that are considered public

  - the ``Prog`` class
  - the ``ExitFailure`` exception class

  You won't be prevented from importing any other names,
  but the aforementioned two are the most useful ones.

- Methods that are considered public and should be overridden

  - ``Prog.main``
  - ``Prog.add_args``

  Other methods are considered advanced,
  but not reserved nor internal.
