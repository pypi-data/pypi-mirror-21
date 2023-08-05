finesm |Build Status| |Coverage Status|
=======================================

Installation
------------

``pip install finesm``

Usage
-----

.. code:: python

    from finesm import State, StateMachine

    class MyStateMachine(StateMachine):
        stop = State(default=True)
        go = State()

        @stop.on_message('switch')
        def stop_switch(self):
            self.set_state(go)

        @stop.on_exit
        def stop_exit(self):
            print('exiting stop state')

        @go.on_enter
        def go_enter(self):
            print('entering go state')

        @go.on_update
        def go_update(self):
            print('tick')


    sm = MyStateMachine()
    sm.state  # stop
    sm.update()  #
    sm.send_message('switch')  # exiting stop state
                               # entering go state
    sm.update()  # tick

.. |Build Status| image:: https://travis-ci.org/wesleyks/finesm.svg?branch=master
   :target: https://travis-ci.org/wesleyks/finesm
.. |Coverage Status| image:: https://coveralls.io/repos/github/wesleyks/finesm/badge.svg?branch=master
   :target: https://coveralls.io/github/wesleyks/finesm?branch=master


