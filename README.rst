=====
Kubos
=====

Kubos is a simple CAD application for Windows and Linux.
It is based on OpenCASCADE, Qt and Python.

Installing on Windows
=====================

Kubos requires the following components to work:

1) Python 2.6.6 (Download: http://www.python.org/ftp/python/2.6.6/python-2.6.6.msi)
2) PyQt 4.9.5 (Download: http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.9.5/PyQt-Py2.6-x86-gpl-4.9.5-1.exe)
3) pythonOCC 0.5 (Download: http://pythonocc.googlecode.com/files/pythonOCC-0.5-win32-all-in-one-py26.exe)

Download and install them from the given links.

Kubos itself can be downloaded from https://sourceforge.net/projects/kubos/files/ . In order to install it extract the contents of the zip archive into a folder on your hard drive. Kubos can be started by double-clicking on the file "run_kubos_windows.bat" in the "bin" folder.

Installing on Debian 7
======================

Install the package "python-qt4" from your package manager.

Download and install the following packages: 

1) liboce (64 bit download: https://launchpad.net/~hmeyer/+archive/3d/+build/2914113/+files/liboce1_0.6.0-0ubuntu15_amd64.deb , 32 bit download: https://launchpad.net/~hmeyer/+archive/3d/+build/2914113/+files/liboce1_0.6.0-0ubuntu15_i386.deb)

2) python-occ (64 bit download: https://launchpad.net/~hmeyer/+archive/3d/+build/3026060/+files/python-occ_0.6-0ubuntu2_amd64.deb , 32 bit download: https://launchpad.net/~hmeyer/+archive/3d/+build/2914114/+files/liboce1_0.6.0-0ubuntu15_i386.deb)

Download Kubos from https://sourceforge.net/projects/kubos/files/ and extract the contents of the zip archive into a folder on your hard drive. Kubos can be started by executing the file "run_kubos_linux.sh" in the "bin" folder.

As Debian does not have a "python2" binary one small modification is neccessary in order to avoid problems when opening multiple files: Change the first line of "kubos/__main__.pyw" from "#!/usr/bin/python2" to "#!/usr/bin/python" (drop the trailing number 2)

Other operating systems
=======================

The required components should work on most other operating systems as well. If you can provide installation instructions for other operating systems, please share them on the Kubos discussion forums.
