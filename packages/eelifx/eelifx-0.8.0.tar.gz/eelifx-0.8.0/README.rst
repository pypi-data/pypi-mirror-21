EELifx
======

`Source <https://github.com/cgspeck/eelifx>`_

Automatically set your `Lifx globes <https://www.lifx.com/>`_ according
to player ship game state in
`EmptyEpsilon <http://daid.github.io/EmptyEpsilon/>`_. It uses the
`Lifx LAN Protocol <https://lan.developer.lifx.com/>`_ and may control
any lights that are on the same network as EELifx.

Installation
------------

With Python 3.6+, run ``pip install eelifx``
(`Virtualenv <http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/>`_
recommended).

Quick Start
-----------

1. Start EmptyEpsilon in another console with the httpserver switch:
   ``EmptyEpsilon httpserver=8080``

2. Turn on your Lifx lights, make sure they are conn

3. Run EELifx and point it at your server, e.g.
   ``eelifx run 192.168.1.10`` or ``eelifx run localhost``

Advanced Usage
--------------

The full range of commands are avaliable by running help:

::

    $ eelifx
    Usage: eelifx [OPTIONS] COMMAND [ARGS]...

      EELifx Copyright (C) 2017 Chris Speck

    Options:
      --loglevel TEXT  E.g. "DEBUG" or "INFO"
      --help           Show this message and exit.

    Commands:
      grouptest   Execute each rule in succession.
      queryship   Query EE and set parameters if given.
      reset       Reset lights to base state.
      run         Poll and set lights according to game state.
      showconfig  Print default config to standard out.

Custom Configs
--------------

Your can pass the path to a custom config to the ``run`` and
``grouptest`` commands with ``--config <FILE>``.

You can find example configs in `the
repo <https://github.com/cgspeck/eelifx/tree/master/configs>`_ or by
running ``eelifx showconfig``

Rules and Groups
----------------

Groups represent Lifx Groups, and have a match regex defined within the
configuration which tell EELifx which bulbs to apply the groups' rules
to. The default pattern is ``.*`` (i.e. all groups).

This tool peroidically polls EmptyEpsilon, parses the game state into a
ship object, and evaluates rule statements in the order in which they
are defined within each group. If the rule statement returns true then
its effect is applied, with the following notes:

-  lights are always initially set to their base\_state
-  ``set_power`` latches to False, that is, any call to False will
   override any other call to True within that iteration
-  ``set_colour`` accepts any colour which the
   `colour <https://pypi.python.org/pypi/colour/>`_ package supports
-  the last call to ``set_colour`` overrides any earlier call
-  ``set_luminance`` accepts a float in range 0 - 1
-  the last call to ``set_luminance`` overrides any earlier call
-  the last call to ``set_waveform`` overrides any earlier call
-  the luminance of any colour set through ``set_colour`` or
   ``set_waveform`` will be clipped to that group's ``max_luminance``
-  the luminance of any colour will be multiplied by any value set by
   ``set_luminance``

Waveform Support
----------------

This doesn't seem to be documented particulararly well, but the source
of the
`lifx-gem <https://github.com/LIFX/lifx-gem/blob/master/lib/lifx/protocol/light.rb>`_
shows that the following waveforms are supported:

::

    SAW = 0
    SINE = 1
    HALF_SINE = 2
    TRIANGLE = 3
    PULSE = 4

``set_waveform`` takes a dictionary with the following keys: \* ``hz``
as an integer \* ``waveform`` as a string, being one of those named
above \* an optinal ``alt_colour``, being the same format as that given
to ``set_colour``

LifxCommander
-------------

The methods ``set_colour``, ``set_power``, ``set_waveform`` and
``set_luminance`` are the only methods on lifx\_commander which you
should call in your config. See example configs for details.

Ship object
-----------

The ship object exposes the following properties:

-  ship.hull - float in range 0 - 1
-  ship.energy - float in range 0 - 1
-  ship.alert\_level - string, 'normal', 'YELLOW ALERT' or 'RED ALERT'

Licensed under the GPLv3
