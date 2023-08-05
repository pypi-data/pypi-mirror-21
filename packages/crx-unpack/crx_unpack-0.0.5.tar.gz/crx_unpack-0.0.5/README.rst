====================
CRX Unpack in Python
====================

.. image:: https://img.shields.io/pypi/v/crx_unpack.svg
    :target: https://pypi.python.org/pypi/crx_unpack

.. image:: https://img.shields.io/pypi/pyversions/crx_unpack.svg
    :target: https://pypi.python.org/pypi/crx_unpack

.. image:: https://img.shields.io/pypi/l/crx_unpack.svg
    :target: https://pypi.python.org/pypi/crx_unpack

.. image:: https://img.shields.io/pypi/dm/crx_unpack.svg
    :target: https://pypi.python.org/pypi/crx_unpack

crx_unpack is a Python library for extracting the contents of a Chrome
extension file (``.crx``).

Structure of CRX Package Format
-------------------------------

*As explained at* `<https://developer.chrome.com/extensions/crx>`_

Package Header
--------------

The header contains the author's public key and the extension's signature. The signature is generated from the ZIP file
using SHA-1 with the author's private key. The header requires a little-endian byte ordering with 4-byte alignment. The
following table describes the fields of the ``.crx`` header in order:

===================  ============  ===============  =================  ===========
Field                Type          Length           Value              Description
===================  ============  ===============  =================  ===========
*magic number*       char[]        32 bits          Cr24               Chrome requires this constant at the beginning of every ``.crx`` package.
*version*            unsigned int  32 bits          2                  The version of the ``*.crx`` file format used (currently 2).
*public key length*  unsigned int  32 bits          *pubkey.length*    The length of the RSA public key in *bytes*.
*signature length*   unsigned int  32 bits          *sig.length*       The length of the signature in *bytes*.
*public key*         byte[]        *pubkey.length*  *pubkey.contents*  The contents of the author's RSA public key formatted as an X509 SubjectPublicKeyInfo block.
*signature*          byte[]        *sig.length*     *sig.contents*     The signature of the ZIP content using the author's private key. The signature is created using the RSA algorithm with the SHA-1 hash function.
===================  ============  ===============  =================  ===========

Extension Contents
------------------

The extension's ZIP file is appended to the ``*.crx`` package after the header. This should be the same ZIP file that
the signature in the header was generated from.
