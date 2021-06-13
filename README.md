# MaProS
This project is the implementation of work from my Master thesis at UCLouvain.
This is still work in progress and is not a final version of the work.
The main goal is to show a proof of concept of a system that would allow a user to write a mathematical proof in a
close to natural language manner.
Such proof would then be translated in [Lean3](https://leanprover.github.io/) to be verified.

This repository contains the backend part of the system.
It uses the [Django framework](https://www.djangoproject.com/) with the library [DRF](https://www.django-rest-framework.org/).

Instructions are available for
* Installation : [installation.md](installation.md)
* User Guide : [user_guide.md](user_guide.md)

## External sources
* The proof for the sandiwch theorem available at this [link](http://wwwf.imperial.ac.uk/~buzzard/docs/lean/sandwich.html)
  is used as basis to include the sandwich theorem in the system.
  Its header is also used to include some tactics such as "By inequality properties".
* The majority of the content in leanclient is from the repository 
  [https://github.com/leanprover-community/lean-client-python](https://github.com/leanprover-community/lean-client-python).
