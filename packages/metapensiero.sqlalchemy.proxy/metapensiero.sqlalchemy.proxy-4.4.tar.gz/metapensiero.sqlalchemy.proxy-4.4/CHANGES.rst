Changes
-------

4.4 (2017-04-01)
~~~~~~~~~~~~~~~~

* Rename filter operator ``CONTAINED`` to ``CONTAINS``, and reimplement it to cover different
  data types, in particular PostgreSQL's ranges


4.3 (2017-03-22)
~~~~~~~~~~~~~~~~

* Minor tweak, no externally visible changes


4.2 (2017-03-10)
~~~~~~~~~~~~~~~~

* Reduce clutter, generating a simpler representation of Operator and Direction enums


4.1 (2017-02-13)
~~~~~~~~~~~~~~~~

* Fix an oversight in Filter tuple slots positions, to simplify Filter.make() implementation


4.0 (2017-02-13)
~~~~~~~~~~~~~~~~

* From now on, a Python3-only package

* Backward incompatible sorters and filters refactor, to make interaction easier for code using
  the library

* Drop obsolete Pylons extension


3.6 (2017-01-11)
~~~~~~~~~~~~~~~~

* New Sphinx documentation

* Field's metadata now carries also information about foreign keys

* Handle literal columns in core queries


3.5 (2016-12-29)
~~~~~~~~~~~~~~~~

* Fix incompatibility issue with SQLAlchemy 1.1.x when using ORM


3.4 (2016-03-12)
~~~~~~~~~~~~~~~~

* Better recognition of boolean argument values, coming from say an HTTP channel as string
  literals

* Use tox to run the tests


3.3 (2016-02-23)
~~~~~~~~~~~~~~~~

* Handle the case when the column type cannot be determined


3.2 (2016-02-19)
~~~~~~~~~~~~~~~~

* Fix corner case with queries ordered by a subselect


3.1 (2016-02-07)
~~~~~~~~~~~~~~~~

* Fix metadata extraction of labelled columns on joined tables

* Adjust size of time fields and align them to the right


3.0 (2016-02-03)
~~~~~~~~~~~~~~~~

* Internal, backward incompatible code reorganization, splitting the main module into smaller
  pieces

* Handle corner cases with joined queries involving aliased tables


Previous changes are here__.

__ https://bitbucket.org/lele/metapensiero.sqlalchemy.proxy/src/master/OLDERCHANGES.rst
