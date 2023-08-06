=======
Logging
=======

configdeck uses its own loggers to allow library users to define the desired
verbosity.

Existing loggers exposed by configdeck are:

  * configdeck.parser

To enable logging you need to configure the system like
::

    logging.dictConfig({
        'loggers': {
            'configdeck.parser': {
                'handlers': ['console'],
                'level': 'WARNING',
                },
            },
        'handlers': {
            'console': {
                'formatter': 'simple',
                'class': 'logging.handlers.StreamHandler',
                'level': 'WARNING'
                'args': (sys.stdout,)
                },
            },
        'formatters': {
            'simple': {
                'format': '%(levelname)s %(message)s'
                }
            },
        })
