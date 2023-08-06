django-padlock
==============

Middleware for django 1.7 - 1.10

Modo de trabajo:

-  Se crea 5 piezas en base a una llave (string de 32 caracteres)
-  Se guarda un copia de la llave en la sesión
-  Cuando se hace un POST este llama al cerrajero arma las piezas y las
   compara con la llave original guardada en la sesión
-  Una vez comparadas se pasa el proceso del request y response de
   manera natural
-  Cuando cuando el Usuario esta autenticado y este tiene una llave
   erronea (sessionid robada) el middleware puede cerrar la sesión o
   eliminar las cockies existentes. segun se desee.

::

    Instalar vía pypi:
    pip install django-padlock==0.1.7.12

    Añadir el middleware a la configuración:
    MIDDLEWARE = [
        ...
        'padlock.middleware.PadLockMiddleware'
    ]


    Estableces las siguientes variables en la configuración:

    # Lista los paths a omitir, ['*'] omite todos los paths
    PADLOCK_SKIP_PATHS = []

    # Establece el tiempo de vida de la cookies (el valor recomendable es >= 120)
    PADLOCK_COOKIE_AGE = 3600*12

    # Boolean que indica cerrar sesión en caso de intento de romper seguridad
    PADLOCK_AUTHBROKEN_LOGOUT = False

    # URL de redirecionamiento luego de cerrar sesión
    # Note que si empieza con '/' o ' http' se usa como string
    # de caso contrario se usa como un pattern name
    PADLOCK_LOGOUT_REDIRECT_TO = '/'

    # Define el nombre de las cockies
    PADLOCK_PREFIX = 'padlock_tester'

