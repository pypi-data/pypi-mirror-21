``subtoml``: Sed for TOML
=========================

``subtoml`` is a small CLI utility that substitutes parts of a TOML file.

.. code-block:: console

   $ cat sample.toml
   [database]
   url = "postgresql://localhost/sample"
   [web]
   debug = true
   $ subtoml database.url 'postgresql://localhost/test' < sample.toml
   [database]
   url = "postgresql://localhost/test"
   [web]
   debug = true

Distributed under GPLv3_ or later.

.. _GPLv3: http://www.gnu.org/licenses/gpl-3.0.html
