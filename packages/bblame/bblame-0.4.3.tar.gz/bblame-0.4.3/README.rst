bblame
======
``bblame`` is an interactive ncurses git blame viewer. Allowing you to explore the git history of a file. 

Features
--------
- Browse forwards and backwards through file history a commit at a time 
- Select a line and drill into the history past the commit that changed that line most recently
- Display the git ``show`` for the commit of any selected line
- Browse file history across file renames
- Search and colour support

Usage
-----
``bblame`` is a curses application. Usage will be displayed when called with no arguments or ``-h`` ``--help``::

	usage: __main__.py [-h] [--revision {revision}] [--debug] [--version]
					   filename [+{line_num} or +/{search_pattern}]

	positional arguments:
	  filename              Name or path to file to blame
	  +{line_num} or +/{search_pattern}
							The line number or search pattern the cursor will be positioned on (this arg will put bblame in visual mode)

	optional arguments:
	  -h, --help            show this help message and exit
	  --revision {revision}, -r {revision}
							The revision to initialize the blame file to
	  --debug               Increase logging and show tracebacks
	  --version             show program's version number and exit

To show available commands while running ``bblame`` use the ``h`` key, which will display the key to action mappings as below::

	KEYS: ACTION - DESCRIPTION
	--------------------------
	 q:   Quit
		Quit the application

	 /:   Search
		Search downward through the current blame or commit

	 n:   Next Search Match
		Jump to the next search match (in the downward direction)

	 N:   Prev Search Match
		Jump to the prev search match (in the upward direction)

	 v, s:   Visual Select Mode
		Enter visual select mode (only from normal mode)

	 o:   Show/View Commit
		Show a commit selected by the visual mode cursor

	 O:   Show/View file Commit
		Show the current revision commit

	 ESC:   Normal Mode
		Return to Normal mode

	 ENTER, d:   Drill Down
		Drill down past the commit highlighted in visual mode. Opens a new git blame

	 <, ,:   Parent blame
		Open a new git blame to the parent of the current commit

	 >, .:   Ancestor blame
		Open a new git blame to the ancestor of the current commit

	 BACKSPACE, DC, f:   Pop Back
		Pop back to previous git object

	 G, END:   Jump to Bottom
		Jump to the bottom of the screen

	 h:   Help
		Display the help message

	 H:   Jump to HEAD
		Jump to a blame of the most recent commit for the file

	 T:   Jump to TAIL
		Jump to a blame of the first commit for the file

 

Installation
------------
::

     sudo -H pip install bblame

or ::

    python setup.py install

Issue
-----
Issue tracker can be found `here`__

__ https://bitbucket.org/niko333/betterblame/issues?status=new&status=open


Development:
------------
Pull requests welcome

Git repo can be found `here`__

__ https://bitbucket.org/niko333/betterblame

Dependencies you'll need to install with your package manager for dev and test:

- ``pip``/``pip3`` (bblame supports both 2.7.X and 3+ versions of python)
- ``tmux`` (a dependency of the curses unit test library, hecate)
- ``make``

The rest of the dependencies can be installed with:

- ``make py_env``

Useful Dev Notes:

- run ``make check`` to execute static analysis and unittests
- run ``python -m betterblame <args>`` in root of ``betterblame.git`` to run an
  instance of ``bblame`` with your changes
- You can use the test files in ``tests/testfiles/`` for manual testing.
