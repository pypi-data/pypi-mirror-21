xlsform-converter (xlsconv)
===========================

xlsform-converter converts surveys defined via the `XLSForm
standard <http://xlsform.org/>`__ into `Django
models <https://docs.djangoproject.com/en/1.9/topics/db/models/>`__ and
HTML5 `Mustache templates <https://wq.io/docs/templates>`__. This makes
it possible to re-use the powerful form building tools provided by the
`Open Data Kit ecosystem <https://enketo.org/openrosa>`__, while
leveraging Django's robust support for relational databases like
`PostgreSQL <http://www.postgresql.org/>`__.

xlsform-converter is designed to facilitate the rapid development of
offline-capable data collection apps via the `wq
framework <https://wq.io/>`__. The ultimate goal is to provide full
compatibility with the form authoring tools provided by `ODK (and
Enketo, etc.) <https://enketo.org/openrosa>`__. Note that this is not
the same as full XForm compatibility: the client and server components
of wq (`wq.app <https://wq.io/wq.app>`__ and
`wq.db <https://wq.io/wq.db>`__) use a JSON-based `REST
API <https://wq.io/docs/url-structure>`__ to exchange data and are not
directly compatible with their ODK Analogues (ODK Collect and ODK
Aggregate, respectively).

For the database itself, the key distinction from other XLSForm tools
(including some powered by Django) is that xlsform-converter converts
the xlsform fields directly into a Django model definition, rather than
representing the entire XForm standard within Django. This means that
each row in an XLSForm "survey" tab is mapped to (usually) a single
column in a simple relational database table. Repeat questions are
handled by creating a second model with a ``ForeignKey`` to the parent
survey model.

xlsform-converter also supports a couple of additional "constraints"
that are not part of the XLSForm standard:

-  ``wq:ForeignKey('app.ModelName')``: Create a foreign key to an
   existing Django model (presumably not defined in the spreadsheet).
   This is effectively a more relational version of
   ``select_one_external``.
-  ``wq:initial(3)``: Very similar to ``repeat_count``, but only set for
   new records.
-  ``wq:length(5)``: Text field maximum length (similar to a
   ``string-length`` constraint)

|Latest PyPI Release| |Release Notes| |License| |GitHub Stars| |GitHub
Forks| |GitHub Issues|

|Travis Build Status| |Python Support|

Included Templates
~~~~~~~~~~~~~~~~~~

xlsform-converter uses the following templates to generate Django/wq
project files from a given XLSForm.

Django App Templates
^^^^^^^^^^^^^^^^^^^^

-  ```models.py`` <https://github.com/wq/xlsform-converter/blob/master/xlsconv/templates/models.py-tpl>`__
-  ```rest.py`` <https://github.com/wq/xlsform-converter/blob/master/xlsconv/templates/rest.py-tpl>`__
   (for use with ```wq.db.rest`` <https://wq.io/docs/about-rest>`__)
-  ```admin.py`` <https://github.com/wq/xlsform-converter/blob/master/xlsconv/templates/admin.py-tpl>`__
   (for use with
   ```django.contrib.admin`` <https://docs.djangoproject.com/en/1.10/ref/contrib/admin/>`__)
-  ```serializers.py`` <https://github.com/wq/xlsform-converter/blob/master/xlsconv/templates/serializers.py-tpl>`__
   (for use with ``wq.db.rest``)

Mustache Templates (for use with `wq <https://wq.io/docs/templates>`__)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ```edit.html`` <https://github.com/wq/xlsform-converter/blob/master/xlsconv/templates/edit.html>`__
-  ```detail.html`` <https://github.com/wq/xlsform-converter/blob/master/xlsconv/templates/detail.html>`__
-  ```list.html`` <https://github.com/wq/xlsform-converter/blob/master/xlsconv/templates/list.html>`__
-  ```popup.html`` <https://github.com/wq/xlsform-converter/blob/master/xlsconv/templates/popup.html>`__
   (for use with `wq/map.js <https://wq.io/docs/map-js>`__)

Usage
~~~~~

If you are using wq, you may be interested in
`wq.start <https://github.com/wq/wq-django-template>`__, which uses
xlsconv internally for the ``wq addform`` and ``wq maketemplates``
commands. Otherwise, you can use xlsconv directly with the following
command-line API:

.. code:: bash

    pip3 install xlsconv

    # Use the default models.py template
    xls2django my-odk-survey.xls > myapp/models.py

    # Use the rest.py template (or admin.py, or serializers.py)
    xls2django my-odk-survey.xls rest > myapp/models.py

    # Use a custom template
    xls2django my-odk-survey.xls my_templates/models.py > myapp/models.py

    # Use the default edit.html template
    xls2html my-odk-survey.xls > templates/survey_edit.html

    # Use the list.html template (or detail.html, or popup.html)
    xls2html my-odk-survey.xls list > templates/survey_list.html

    # Use a custom template
    xls2html my-odk-survey.xls my_templates/edit.html > templates/survey_edit.html

.. |Latest PyPI Release| image:: https://img.shields.io/pypi/v/xlsconv.svg
   :target: https://pypi.python.org/pypi/xlsconv
.. |Release Notes| image:: https://img.shields.io/github/release/wq/xlsform-converter.svg
   :target: https://github.com/wq/xlsform-converter/releases
.. |License| image:: https://img.shields.io/pypi/l/xlsconv.svg
   :target: https://github.com/wq/xlsform-converter/blob/master/LICENSE
.. |GitHub Stars| image:: https://img.shields.io/github/stars/wq/xlsform-converter.svg
   :target: https://github.com/wq/xlsform-converter/stargazers
.. |GitHub Forks| image:: https://img.shields.io/github/forks/wq/xlsform-converter.svg
   :target: https://github.com/wq/xlsform-converter/network
.. |GitHub Issues| image:: https://img.shields.io/github/issues/wq/xlsform-converter.svg
   :target: https://github.com/wq/xlsform-converter/issues
.. |Travis Build Status| image:: https://img.shields.io/travis/wq/xlsform-converter/master.svg
   :target: https://travis-ci.org/wq/xlsform-converter
.. |Python Support| image:: https://img.shields.io/pypi/pyversions/xlsconv.svg
   :target: https://pypi.python.org/pypi/xlsconv
