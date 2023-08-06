python-purple - Python bindings for libpurple
---------------------------------------------

Original copyright:
Copyright (c) 2008 INdT - Instituto Nokia de Tecnologia

This project is attempt to revive python-purple, convert to python3 and
make it more palatible for integration with other projects.

Installation:

```
apt-get install libpython3.4-dev gcc build-essential libglib2.0-dev libpurple-dev
pip3 install python-purple
```

If you wish to recompile `purple.c` with Cython (not required) use:

```
setup.py build --with-cython
setup.py install
```

Andrey Petrov (andrey.petrov@gmail.com)

