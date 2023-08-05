Webpack filter for webassets
-------------------------------

.. image:: https://travis-ci.org/suryakencana/webassets-webpack.svg?branch=master
    :target: https://travis-ci.org/suryakencana/webassets-webpack


Filter for for compiling assets using `Webpack <https://webpack.js.org>`_ and
`webassets <http://webassets.readthedocs.org>`_.

Basic usage
```````````

.. code:: python

    from webassets.filter import register_filter
    from webassets_browserify import Webpack

    register_filter(Webpack)


Usage with Django
`````````````````

This requires `django-assets <http://django-assets.readthedocs.org>`_.

.. code:: python

    from django_assets import Bundle, register
    from webassets.filter import register_filter
    from webassets_webpack import Webpack

    register_filter(Webpack)

    js = Bundle('js/main.js', filters='webpack', output='bundle.js',
                depends='js/**/*.js')
    register('js_all', js)



