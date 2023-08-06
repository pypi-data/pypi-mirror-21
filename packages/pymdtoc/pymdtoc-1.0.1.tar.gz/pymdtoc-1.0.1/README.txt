.. raw:: html

   <!-- starttoc -->

Table of contents
=================

-  `mdTOC <#mdtoc>`__

   -  `Installation <#installation>`__
   -  `Usage <#usage>`__

      -  `Generate TOC <#generate-toc>`__
      -  `Generate and update file <#generate-and-update-file>`__

   -  `Via python <#via-python>`__

      -  `Optional arguments <#optional-arguments>`__

.. raw:: html

   <!-- endtoc -->

mdTOC
=====

Create Table of contents for markdown files

Installation
------------

.. code:: shell

    pip install pymdtoc

Usage
-----

Generate TOC
~~~~~~~~~~~~

.. code:: shell

    mdtoc generate filename.md

Generate and update file
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: shell

    mdtoc inplace filname.md

Via python
----------

.. code:: python

    from pymdtoc import TOC
    toc = TOC(file="filename.md")
    print(toc.toc)
    print(toc.content)

Optional arguments
~~~~~~~~~~~~~~~~~~

-  ``toc_heading`` - Table of contents heading (str)
-  ``anchor_function`` - Ability to provide custom anchor tag generator
