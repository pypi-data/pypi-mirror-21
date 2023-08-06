pytictoc contains a class TicToc which replicates the functionality of MATLAB's tic and toc for easily timing sections of code. Under the hood, pytictoc uses the default_timer function from Python's timeit module.


=============
INSTALLATION
=============

pytictoc can be installed and updated via conda or pip.

**pip**

::

 pip install pytictoc
 pip install pytictoc --upgrade

**conda**

::

 conda install pytictoc -c ecf
 conda update pytictoc -c ecf


==========
USAGE
==========

::

 >> from pytictoc import TicToc

 >> t = TicToc() #create instance of class

 >> t.tic() #Start timer
 >> t.toc() #Time elapsed since t.tic()
 Elapsed time is 2.612231 seconds.

 >> t.toc('It has been') #alternative message
 It has been 16.494467 seconds.

 >> t.toc(restart=True) #restart timer after reporting time
 Elapsed time is 36.986837 seconds.
 >>t.toc()
 Elapsed time is 2.393425 seconds.

 >>spam = t.tocvalue() #return elapsed time instead of printing
 >>spam
 20.156261717544602

