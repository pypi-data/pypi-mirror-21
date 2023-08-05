Fleaker
-------

Fleaker is a framework built on top of Flask that aims to make using Flask
easier and more productive, while promoting best practices.

Yes, it's BSD licensed.

Easier to Setup
`````````````

Save in an app.py:

.. code:: python

    import os

    from fleaker import App

    def create_app():
        app = App.create_app(__name__)
        settings_dict = {'DEBUG': True}
        app.configure('.settings', os.env, settings_dict)

        return app

    if __name__ == '__main__':
        create_app().run()

Just as Easy to Use
```````````````````

Run it:

.. code:: bash

    $ pip install fleaker
    $ python app.py
     * Running on http://localhost:5000/


