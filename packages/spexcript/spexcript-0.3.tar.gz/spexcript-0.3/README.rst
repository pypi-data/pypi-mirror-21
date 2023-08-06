SpeXcript -- makes your spex script beautiful
=============================================

SpeXcript is a markup and layout system for scripts of theater plays or 
musicals etc. I originally made it for Fyysikkospeksi, a spex made every
other year by mostly Engineering Physics undergraduate and graduate students 
at Aalto University. For now, it has only been for our internal use, but I 
am now (2015) releasing it for free and as open source. 
It would make me happy if someone else finds this useful.

Any feedback or suggestions are very welcome: koos.zevenhoven@aalto.fi.

Getting Started
===============

Requirements
------------

* Python 3.4 (May work with older versions, but no official support)

Installation
------------

spexcript can be installed with ``pip`` (make sure you have it installed):

.. code-block:: bash

    $ pip install spexcript


or directly from the source code:

.. code-block:: bash

    $ git clone https://github.com/k7hoven/spexcript.git
    $ cd spexcript
    $ python setup.py install 

Basic Usage
===========

The documentation for the markup language itself is on its way, but if you
have a spexcript file, say ``myspex.sxt``, you can lay it out as pdf from the
command line as  follows:

.. code-block:: bash

    $ python -m spexcript myspex.sxt

The interface and documentation will be further improved in the future.

