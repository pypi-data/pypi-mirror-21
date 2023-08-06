Ionization Cross Sections
=========================

Installation
------------

Requirements
~~~~~~~~~~~~

If you are on Unix then all dependencies are installed automatically upon installation. If you are
using Windows then the ``numpy`` and ``scipy`` dependencies can't be installed automatically as
they require precompiled binaries for the specific operating system. Scipy doesn't support
binaries for Windows officially. Please consider the scipy installation instructions about
`scientific Python distributions`_ and `inofficial binaries`_.

.. _scientific Python distributions: https://www.scipy.org/install.html#scientific-python-distributions
.. _inofficial binaries: https://www.scipy.org/install.html#windows-packages

The GUI uses PyQt4_ which must be installed separately. You can use the package of course without
the GUI in your scripts by simply importing it. However if you want to use the GUI please consider
the following resources:

* **Unix** - You can downloaded the latest release from `here
  <https://www.riverbankcomputing.com/software/pyqt/download>`_. Please follow the installation
  instructions on this website. Usually you have to build it from source which is fairly simple though.

* **Windows** - Download the correct PyQt4 version from `here <http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4>`_;
   make sure that you match your Python and OS version. Then open Powershell (press the Windows key
   and type "Powershell" in the search field; we recommend to use the x86 version) and navigate to
   the folder where you downloaded the ``.whl`` file to (usually ``Downloads``). Then install the
   package via ``pip install <version>.whl`` where you replace ``<version>.whl`` with the name of
   the file you downloaded (you can use tab completion in Powershell).

.. _PyQt4: https://www.riverbankcomputing.com/software/pyqt/intro

The GUI also uses ``matplotlib``; please visit their `website <https://matplotlib.org/users/installing.html>`_
for the installation instructions.


Installing the package
~~~~~~~~~~~~~~~~~~~~~~

You can install the package from pip by running ``pip install ionics``.

**Note:** If you are using Windows then Python must have been added to your path in order for the
above command to succeed.


Usage
-----

The GUI
~~~~~~~

To use the graphical user interface navigate to the directory where the package has been installed.
You can find it by running ``python -c "import ionics; print ionics.__file__"``. Within that
directory just run ``python start_gui.py``.

Browsing cross section
``````````````````````

On the left side you find a file browser exposing the cross section files that are contained by
the ``ionics`` package. You can get a list of available cross sections by either clicking
on a directory (all cross section within that directory) or a module itself (all cross sections
within that module). The cross sections are shown in the window below the file browser.
By clicking on a cross section you can obtain information about them.

Plotting cross sections
```````````````````````

To plot a specific cross section drag and drop it onto a plot canvas on the right side.
You are prompted to enter the cross section's specific parameters as well as the plot range.
You can also specify the scale for which the data should be generated (*linear* means the data is
evenly distributed, *log* means the data is exponentially distributed so it will be evenly
distributed when using a log-scale).

Also:

* You can stack multiple single-differential cross sections by dropping them onto the same canvas.
* You can add a new canvas by clicking on the "add" button on the very right.
* You can change the scale for each axis at the bottom of the corresponding plot.


Usage within your applications
``````````````````````````````

This package contains various ionization cross sections as well as related auxiliary functions
(such as random sampling). Two kinds of ionization cross sections are provided:

* Single differential ionization cross sections (SDCS); see ``ionics.ddcs``.
* Double differential ionization cross sections (DDCS); see ``ionics.sdcs``.

Required parameters for cross sections must be specified in their ``__init__`` methods. A cross
section can be evaluated by calling it (via ``__call__``) (for the signature see the help text of
one of the cross sections). SDCS require the kinetic energy of the ionized particle as an argument
while DDCS also require the polar scattering angle (in addition).

Random sampling is available for double differential cross sections. Two general methods are available
which are meant to work with any two-dimensional distribution:

* Inverse transform sampling
* Rejection sampling

Please consider ``ionics.ddcs.random_sampling`` for more information.


Examples
--------

Using a double differential cross section::

    >>> from ionics.ddcs.voitkiv import VoitkivDDCS
    >>> ddcs = VoitkivDDCS(4.0e12, 1, 'H')  # 4 TeV protons on Hydrogen.
    >>> ddcs(10, pi/2)  # Kinetic energy 10eV, transverse scattering.
    0.00043127346990368256



