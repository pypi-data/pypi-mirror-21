serialstruct
############

Implements a StructuredPacket for pySerial's ``serial.threaded`` module

Installation
============

.. code-block:: bash

        $ pip install serialstruct


Motivation
==========
When sending a structured binary packet over Serial, the only way (that I'm aware
of) to guarantee packet alignment with arbitrary data is to send a header that's
larger than any of the elements and add padding between each element. Here's an
example:

