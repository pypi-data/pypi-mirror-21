npy4chan
========

Very simple, minimalistic wrapper for 4chan's API.

To create an instance of the wrapper::

    api = npy4chan.load()

Attributes and methods::

    api.boards # dictionary of board identifiers and title (i.e; {"b": "Random"})
    api.getPosts(board, page=1) # Get list of thread on page <page> of <board>
    api.getThread(board,threadno) # Get posts from <board>'s thread <threadno>

