`Jaeum Modifier`_
=================

.. image:: https://readthedocs.org/projects/jaeum-modifier/badge/?version=latest
    :target: http://jaeum-modifier.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


A simple module that injects a JJ(u'ㅉ') or BB(u'ㅃ') to the given Korean word or sentence.

For example:

.. code-block:: python

    from jaeum_modifier import set_by_index
    message = u'안녕하세요'
    print(set_by_index(message, index=1)) # 안쪙하세요


Installation
------------
Jaeum Modifier can be installed via ``pip``:

.. code-block:: console

    $ pip install jaeum_modifier

You can also install from `Github repository`__:

.. code-block:: console

    $ git clone git@github.com:hyunchel/jaeum_modifier.git
    $ cd jaeum_modifier/
    $ python setup.py install
      
.. _Jaeum Modifier: https://github.com/hyunchel/jaeum_modifier
__ https://github.com/hyunchel/jaeum_modifier
     

Documentation
-------------
Lastest Version
    https://jaeum-modifier.readthedocs.io
