# GW2-DecoRBT
Simple python script that could be run to automatically edit Guild Wars 2 saved homestead layout files.   

This program reads two XML layout files ("RBT_origin", "RBT_shift") to generate the output layout.
> RBT_origin	= the decoration plus one new prop (point of reference)

> RBT_shift 	= the new prop (point of reference) moved to new location 

# How to Use
Copy the 'GW2 DecoRBT.py' from the 'source' folder to your own PC, and place the two XML files needed in the same folder as your code. Double click it and wait for it to generate the output XML. See the requirements below to be able to make use of the source code, otherwise you might want to look inside 'executable' folder and download the 'GW2 DecoRBT.exe' from there to run it without any requirements.

## Requirements
  - Python 3.8 or higher
  - NumPy (`pip install numpy`)
  - Pyinstaller (If you wish to make it portable exe, so that you can run it from 
