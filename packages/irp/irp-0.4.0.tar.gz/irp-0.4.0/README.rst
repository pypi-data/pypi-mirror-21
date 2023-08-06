IRP
===

AIRPort city name resolver. And back.

This is how you use it:

::

    $ pip install irp
    $ export IATACODES_API_KEY="..."  # Get it for free at iatacodes.org
    $ ipython

    In [1]: from irp import get_airports, get_name

    In [2]: list(get_airports('Portland'))
    Out[2]: [('PDX', 'US'), ('PTJ', 'AU'), ('PWM', 'US')]

    In [3]: list(get_airports('Portland, US'))
    Out[3]: [('PDX', 'US'), ('PWM', 'US')]

    In [4]: list(get_airports('PDX'))
    Out[4]: [('PDX', 'US')]

    In [5]: list(get_airports('Isiro'))
    Out[5]: [('IRP', 'CD')]

    In [6]: get_name('IRP')
    Out[6]: 'Isiro'

**NOTE** We're ATM bypassing iatacodes.org SSL verification. If you don't want
this, patch it, it's probably easy but we needed a hotfix.
