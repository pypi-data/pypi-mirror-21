.. _Tutorial: https://kur.deepgram.com/tutorial.html

******************************
Kur: Descriptive Deep Learning
******************************

Introduction
============

Welcome to Kur! You've found the future of deep learning!

- Install Kur easily with ``pip install kur``.
- Design, train, and evaluate models *without ever needing to code*.
- Describe your model with easily understandable concepts.
- Quickly explore better versions of your model with the power of the `Jinja2
  <http://jinja.pocoo.org>`_ templating engine.
- Supports Theano, TensorFlow, and PyTorch, and supports **multi-GPU**
  out-of-the-box.
- **COMING SOON**: Share your models with the community, making it incredibly
  easy to collaborate on sophisticated models.

Go ahead and give it a whirl: `Get the Code`_ and then jump into
the `Examples`_! Then build your own model in our Tutorial_. Remember to check
out our `homepage <https://kur.deepgram.com>`_ for complete documentation and
the newest news.

What is Kur?
------------

Kur is a system for quickly building and applying state-of-the-art deep
learning models to new and exciting problems. Kur was designed to appeal to the
entire machine learning community, from novices to veterans. It uses
specification files that are simple to read and author, meaning that you can
get started building sophisticated models *without ever needing to code*. Even
so, Kur exposes a friendly and extensible API to support advanced deep learning
architectures or workflows. Excited? Jump straight into the `Examples`_.

.. _get_the_code:

Get the Code
============

Kur is really easy to install! You can pick either one of these two options for
installing Kur.

**NOTE**: Kur requires **Python 3.4** or greater. Take a look at our
`installation guide <https://kur.deepgram.com/installing.html>`_ for
step-by-step instructions for installing Kur and setting up a `virtual
environment <https://virtualenv.pypa.io/>`_.

Latest Pip Release
------------------

If you know what you are doing, then this is easy:

.. code-block:: bash

	pip install kur

Latest Development Release
--------------------------

Just check it out and run the setup script:

.. code-block:: bash

	git clone https://github.com/deepgram/kur
	cd kur
	pip install .

**Quick Start**: Or, if you already have `Python 3 installed
<https://kur.deepgram.com/installing.html>`_, then here's a few quick-start
lines to get you training your first model:

**Quick Start For Using pip:**

.. code-block:: bash

	pip install virtualenv                      # Make sure virtualenv is present
	virtualenv -p $(which python3) ~/kur-env    # Create a Python 3 environment for Kur
	. ~/kur-env/bin/activate                    # Activate the Kur environment
	pip install kur                             # Install Kur
	kur --version                               # Check that everything works
	git clone https://github.com/deepgram/kur   # Get the examples
	cd kur/examples                             # Change directories
	kur train mnist.yml                         # Start training!

**Quick Start For Using git:**

.. code-block:: bash

	pip install virtualenv                      # Make sure virtualenv is present
	virtualenv -p $(which python3) ~/kur-env    # Create a Python 3 environment for Kur
	. ~/kur-env/bin/activate                    # Activate the Kur environment
	git clone https://github.com/deepgram/kur   # Check out the latest code
	cd kur                                      # Change directories
	pip install .                               # Install Kur
	kur --version                               # Check that everything works
	cd examples                                 # Change directories
	kur train mnist.yml                         # Start training!

Usage
-----

If everything has gone well, you shoud be able to use Kur:

.. code-block:: bash

	kur --version

You'll typically be using Kur in commands like ``kur train model.yml`` or ``kur
test model.yml``. You'll see these in the `Examples`_, which is
where you should head to next!

Troubleshooting
---------------

If you run into any problems installing or using Kur, please check out our
`troubleshooting <https://kur.deepgram.com/troubleshooting.html>`_ page for
lots of useful help. And if you want more detailed installation instructions,
with help on setting up your environment, before sure to see our `installation
<https://kur.deepgram.com/installing.html>`_ page.

