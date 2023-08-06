.. vim: set fileencoding=utf-8 :
.. Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
.. Thu 02 Feb 2016 14:03:40 CET

============
Installation
============

Our input for the competition uses the signal-processing and machine learning toolbox called `Bob <https://www.idiap.ch/software/bob/>`_.
Follow bellow the instructions to, first, install Bob and then install our competition software.

1 - Installing bob
##################

Bob is a signal-processing and machine learning toolbox originally developed by the Biometrics Group at Idiap, in Switzerland.

We offer pre-compiled binary installations of Bob (v2) using conda for Linux and MacOSX. 
The sequence of commands below will get you started and will install all required dependencies.

.. code-block:: shell

  # for linux
  wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh

  # for mac
  wget https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O ~/miniconda.sh

  bash ~/miniconda.sh
  # Make sure you follow instructions and modify your
  # $PATH variable according to the installation instructions.
  mv ~/.condarc ~/.condarc.bak
  # remove any conda configuration that might interfere.
  # We don't use conda-forge for distributing bob anymore and bob packages 
  # are not compatible with conda-forge packages. So don't mix them!
  conda update -n root conda

  # Adding some the defaults and the bob.conda channels
  conda config --set show_channel_urls True
  conda config --add channels defaults
  conda config --add channels https://www.idiap.ch/software/bob/conda
  
  # Creating the conda env
  conda create -n bob_env_py27 python=2.7 gcc=4
  source activate bob_env_py27

  #Install depedendencies
  conda install scikit-image
  conda install -c bob

  # A small test to see if things are working
  python -c 'import bob.io.base'


2 - Competition software installation
#####################################

Once Bob is installed, you can install our competition input either via `pip` or via `zc.buildout`.

The installation via `zc.buildout` is easier to debug and since this submission is intermediate, we will describe only the installation via this `zc.buildout`.
Follow bellow the steps to install it.

.. code-block:: shell

  # Be sure that you have the conda-env that you created in the last step activated 
  source activate bob_env_py27

  # Cloning the repo
  git clone https://gitlab.idiap.ch/bob/bob.bio.pericrosseye_competition/
  cd bob.bio.pericrosseye_competition
  
  # Checking out the last tag
  git checkout -b v1.0.2 tags/v1.0.2
  
  # Installation
  python bootstrap-buildout.py
  ./bin/buildout
  
  # Most important step. THE UNIT TESTS
  ./bin/nosetests -sv bob.bio.pericrosseye_competition



===================
Competition scripts
===================

This section describes how to run the competition scripts.
Implementation and fine tunning details are described `here <tunning.html#background>`_.

We provide two periocular recognition systems.
The first one is based on Intersession Variability Modelling [FRE16]_ and the second one is based on Geodesic Flow Kernel with gabor jets.

Intersession Variability Modelling
##################################


Description
-----------

Built on top of Gaussian Mixture Models (GMM), Intersession Variability Modelling (ISV) proposes to explicitly model the variations
between different modalities by learning a linear subspace in the GMM supervector space.
These variations are compensated during the enrolment and testing time.
For this input, the periocular images are resized to 90 x 90 pixels and sampled in patches of 12 × 12 pixels moving the sampled window in one pixel.
Then each patch is mean and variance normalized and the first 45 DCT coefficients are extracted.
The Universe Background Model (:math:`UBM`) is modelled with 512 gaussians and the dimension of the session varibility matrix (:math:`U`) is 160.
Implementation details of this input can be found in [FRE16]_.


Scripts
-------


The script ``perienroll_idiap.py``, enrolls a client given an image using this system.
Follow bellow the help message of the script.

.. code-block:: shell

  ./bin/perienroll_idiap.py --help

  Enroll a client using Intersession Variability Modelling

  Usage:
    perienroll_idiap.py <image_file> <template_file> <output_file> [-v]
    perienroll_idiap.py -h | --help
  Options:
    -h --help           Show this screen.
    -v                  Verbosity level


.. warning::
  The `<template_file>` argument must have the extension `.hdf5` (example: template_client_001.hdf5).
  


The scoring script is carryed out using the script ``perimatch_idiap.py``.

.. code-block:: shell

  ./bin/perimatch_idiap.py --help
  Do the matching using Intersession Variability Modelling
  Usage:
    perimatch_idiap.py <image_file> <template_file> <output_file> [-v]
    perimatch_idiap.py -h | --help
  Options:
    -h --help           Show this screen.
    -v                  Verbosity level


.. warning::
  The `<template_file>` argument must have the extension `.hdf5` (example: template_client_001.hdf5).


Geodesic Flow Kernel on Gabor Graphs
####################################


Description
-----------


The Geodesic Flow Kernel (GFK) models the source domain and the target domain with d-dimensional linear subspaces and embeds them onto a Grassmann manifold.
Then a Geodesic Flow [Gong12]_ between these two subspaces (:math:`G`) is built and an infinite number of subspaces is integrated along the flow.
A grid of gabor jets along the periocular image are as features.
A comparison between two grids of gabor jets from visible light and near infra-red respectivelly :math:`S_n` and :math:`T_n` can be done as:
:math:`\frac{\sum_{n=1}^{N} S_n \cdotp G  \cdotp T_n}{N}`.


Scripts first setup
-------------------


The script ``perienroll_idiap_gfk.py``, enrolls a client given an image using this system.
Follow bellow the help message of the script.

.. code-block:: shell

  ./bin/perienroll_idiap_gfk.py

  Enroll a client using the Gabor Graph with Geodesic Flow Kernel

  Usage:
    perienroll_idiap_gfk.py <template_file_A> <template_file_B> <output_file> [-v]
    perienroll_idiap_gfk.py -h | --help
  Options:
    -h --help           Show this screen.
    -v                  Verbosity level

.. warning::
  The `<template_file>` argument must have the extension `.hdf5` (example: template_client_001.hdf5).


The scoring script is carryed out using the script ``perimatch_idiap_gfk.py``.

.. code-block:: shell

  ./bin/perimatch_idiap_gfk.py --help

  Do the matching using the Gabor Graph with Geodesic Flow Kernel

  Usage:
    perimatch_idiap_gfk.py <template_file_A> <template_file_B> <output_file> [-v]
    perimatch_idiap_gfk.py -h | --help
  Options:
    -h --help           Show this screen.
    -v                  Verbosity level

.. warning::
  The `<template_file>` argument must have the extension `.hdf5` (example: template_client_001.hdf5).



Scripts second setup
--------------------

This system is the same as the one above, but with a different setup.

The script ``perienroll_idiap_gfk_10d.py``, enrolls a client given an image using this system.
Follow bellow the help message of the script.

.. code-block:: shell

  ./bin/perienroll_idiap_gfk.py

  Enroll a client using the Gabor Graph with Geodesic Flow Kernel

  Usage:
    perienroll_idiap_gfk_10d.py <template_file_A> <template_file_B> <output_file> [-v]
    perienroll_idiap_gfk_10d.py -h | --help
  Options:
    -h --help           Show this screen.
    -v                  Verbosity level

.. warning::
  The `<template_file>` argument must have the extension `.hdf5` (example: template_client_001.hdf5).


The scoring script is carryed out using the script ``perimatch_idiap_gfk_10d.py``.

.. code-block:: shell

  ./bin/perimatch_idiap_gfk_10d.py --help

  Do the matching using the Gabor Graph with Geodesic Flow Kernel

  Usage:
    perimatch_idiap_gfk_10d.py <template_file_A> <template_file_B> <output_file> [-v]
    perimatch_idiap_gfk_10d.py -h | --help
  Options:
    -h --help           Show this screen.
    -v                  Verbosity level

.. warning::
  The `<template_file>` argument must have the extension `.hdf5` (example: template_client_001.hdf5).

