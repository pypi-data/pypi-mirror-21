=======
pls2upl
=======

pls2upl is a command-line script that will convert a PLS playlist to a UPL
playlist.


Quick start
-----------

You can install pls2upl with pip::

    pip install pls2upl

Or by cloning the repository and running::

    python setup.py install

You're done! Here's how to use the script::

    pls2upl myplaylist.pls myplaylist.upl

Currently, for best results it is recommended to tag your music with MusicBrainz
Picard before running this script, otherwise the MusicBrainz identifiers won't
be added (and those are the most important identifiers)!
