Installation instructions: Arch Linux
=====================================

*   Open a terminal and enter the following commands:

    .. code-block :: bash

        $ sudo pacman -S python2-numpy python2-scipy python2-matplotlib \
            python2-opengl python2-pip wxpython graphviz boost
        $ pip2 install fastcluster --user
        $ pip2 install mapper --user
        $ pip2 install cmappertools --user

*   Optional: Add the directory ``$HOME/.local/bin`` to the search path so that the Mapper GUI can be started more conventiently.

    To do so, open the file ``.bashrc`` in your home directory, eg. by

    .. code-block :: bash

        $ nano ~/.bashrc

    and insert the following lines at the end:

    .. code-block:: bash

        # set PATH so that it includes user's private bin if it exists
        if [ -d "$HOME/.local/bin" ] ; then
            PATH="${PATH+$PATH:}$HOME/.local/bin"
        fi

    Now save the file and type

    .. code-block:: bash

        $ source ~/.bashrc

    in the terminal window to read the modified file in.

*   Try Mapper out:

    .. code-block:: bash

        $ MapperGUI.py
