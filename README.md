# kubos-research

Fork: https://sourceforge.net/p/kubos/ in Python 3

## Install development environment

Need to setup:

1. [Anaconda][1] (Download **3** version )
2. [PyCharm Community][2]
3. [PythonOCC][3]
4. Need to setup PyQT4

Command prompt for anaconda.

#### Create the environment

>conda create -n py35_qt4 python=3.5 anaconda


#### Activate the new environment

>activate py35_qt4


#### Install the PyQt4 package in the new environment

>conda uninstall pyqt

>conda install -c anaconda qt=4.8.7

Use path C:\Anaconda3\envs\py35_qt4\python.exe to your IDE.

>conda install -c dlr-sc -c oce -c pythonocc pythonocc-core

>conda install -y -c conda-forge freetype=2.7

maybe:

>conda install -c conda-forge -c dlr-sc -c pythonocc -c oce pythonocc-core==0.17

### Tested environment:

- Python 3.5
- PyQt4
- PythonOCC 0.17


### Install optional

- [GitHub Desktop][4] 


**Do you like this project? Support it by donating**

- Yandex.Money: [Donate](https://money.yandex.ru/to/410015409987387)
- ![btc](https://camo.githubusercontent.com/4bc31b03fc4026aa2f14e09c25c09b81e06d5e71/687474703a2f2f7777772e6d6f6e747265616c626974636f696e2e636f6d2f696d672f66617669636f6e2e69636f) Bitcoin: 35e1VKWeH5BHzboseYjraa7xWq76sung1v


[1]: https://www.continuum.io/downloads/  "Anaconda
  is a freemium open source distribution of the Python and R programming languages for large-scale data processing, predictive analytics, and scientific computing, that aims to simplify package management and deployment"
[2]:https://www.jetbrains.com/pycharm/download "PyCharm"
[3]: http://www.pythonocc.org/download/ "pythonOCC, 3D CAD/CAE/PLM development framework for the Python programming language"
[4]: https://desktop.github.com/ "GitHub Desktop"
