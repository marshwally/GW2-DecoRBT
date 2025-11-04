# GW2 DecoRBT
Python script that could be run to move Guild Wars 2 homestead decoration to any coordinates/orientation you want.   

## Description
This program will reads two layout files, specifically named `RBT_origin` and `RBT_shift` to generate the output. The output is a layout file with a combined `<props>` from both.

`RBT_origin`	= the decoration you want to move, and one new prop (point of reference)

`RBT_shift` 	= the new prop (point of reference) inside the destination layout

**This program will move every single `<prop>` inside `RBT_origin`.**

## How to Use
1. Load a layout of any decoration that you want to move inside the game (**must be an isolated decoration**).
2. Spawn a new `<prop>` and place it in a good anchor position.
3. Save the layout as `RBT_origin`.
4. Load your destination layout where you want your decoration to be.
5. Spawn the same `<prop>` you use previously, and place it somewhere you see fit.
6. Save the layout as `RBT_shift`.
7. Move `RBT_origin` and `RBT_shift` to the same folder as your own `GW2 DecoRBT.py` or `GW2 DecoRBT.exe`.
8. Run the program.

For a demonstration, refer to: `https://youtube.com/shorts/j0plucAdZ1w?si=HBVfZ2hBtxycaYuV`

## How to get the program for yourself
You have two options to choose from:
1. If you have no problem downloading some requirements, you can head to the `source` folder and copy the `GW2 DecoRBT.py` to your PC.
2. If you don't want any requirements, look inside `executable` folder and download the `GW2 DecoRBT.exe` into your PC.
