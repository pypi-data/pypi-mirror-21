=====
Usage
=====

A ``topshape`` program consists of creating a ``TopShape`` object by calling ``TopShape.create_app()`` and then calling ``run()``.

.. code:: python

    from topshape import TopShape

    # define arguments for create_app here
    # ...

    app = TopShape.create_app(...)
    app.run()


Checkout `here <https://topshape.readthedocs.io/en/latest/topshape.html#topshape.topshape.TopShape.create_app>`_ for the arguments to pass to ``create_app()``.

***********************
Exiting the application
***********************
To exit the application, simply call ``exit()`` on the ``TopShape`` object.

**************
Sorting column
**************
The rows in the body of the ``topshape`` application are sorted by a sorting column (defaults to the leftmost column and can be overridden by passing an arg to ``create_app()``).

While in the main loop, the current column used for sorting can be moved left or right by calling the ``TopShape`` object's ``move_sort_left()`` and ``move_sort_right()`` methods.

*****************
Keypress handling
*****************
You can define what ``topshape`` does when certain keys are pressed by passing a dict as the arg ``key_mapping`` to ``create_app()``.

``key_mapping``'s keys are the physical keys that get pressed and the values are the functions that get called when the keys get pressed.
The values can also be tuples (or lists) where each tuple is ``(handler_function, question)``. The question will be displayed as the bottom line in the header while waiting for input from the user. Once the enter key is pressed, the ``handler_function`` is called and passed the TopShape app object and the answer to the question typed in the bottom line of the header.

The key `h` is not overridable. It always displays the help output. Any override for this key in ``key_mapping`` is ignored.

The key `q` defaults to causing topshape to exit however it can be overriden.


***************************
Displaying help to the user
***************************
While the application is running, pressing ``h`` will show the help screen. The help text is the string that was passed as the
``help_text`` argument to ``create_app()``.
