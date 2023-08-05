takumi-ext
==========

.. image:: https://travis-ci.org/elemepi/takumi-ext.svg?branch=master
    :target: https://travis-ci.org/elemepi/takumi-ext

Simple extension system for extending Takumi framework.

Install
-------

.. code:: bash

    $ pip install takumi-ext


Example
-------

Here is an extension for running codes before app starts and after app exists.

.. code:: python

    app = AppRunner()
    app_runner_ext = ext['app-runner']

    if app_runner_ext:
        runner_ext = app_runner_ext(app)
        app.cfg.set('when_ready', lambda x: runner_ext.on_start())
        app.cfg.set('on_exit', lambda x: runner_ext.on_exit())
    app.run()

To implement this extension:

.. code:: python

    # package name runner_ext
    class RunnerExt(ExtBase):
        name = 'app-runner'

        def __init__(self, app):
            self.app = app

        def on_start(self):
            print('app starting...')

        def on_exit(self):
            print('app existing...')

Add the following config to *app.yml* to use the extension:

.. code:: yaml

    extensions:
        - runner_ext


