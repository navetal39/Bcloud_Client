## INFO:
## This file is needed to convert from .py to .exe.
## In order to do so you need to install 'py2exe' in the computer in which you want to make the conversion.
## After that, all you need to do is to open CMD in the folder in which the 'Bcloud.py' and 'setup.py' (this file) files are in and write the next line (in CMD):
## python setup.py py2exe
## Now some things will be done by the program and after they will be finished, the .exe file will be in the folder called 'dist' in the folder of 'Bcloud.py' (same folder from above).
## IMPORTANT: The .exe file needs all the files in 'dist' in order to run! It can not run by it's own!
## Worth mentioning: The .py file to be converted to .exe needs to run immediately; that means it cannot be a script that after you run him in IDLE, you need to invoke the "run()" method manually (as it is currently in most of our files).
## In addition worth mentioning: It is best if in the end of the .py file to be converted there will be a 'raw_input()' method - this prevents the .exe file from closing when it ends its work, but it is not necessary at all.
######################


from distutils.core import setup
import py2exe

setup(console=['Bcloud.py'])
