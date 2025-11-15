# GW2 DecoRBT
Python script that could be run to move group of Guild Wars 2 homestead/guild hall decoration to any coordinates/orientation.   

## Description
This program will automatically reads two layout files named `RBT_origin.xml` and `RBT_shift.xml`.

`RBT_origin.xml`	= the decoration you want to move and point of reference prop

`RBT_shift.xml` 	= the point of reference prop relocated inside the destination layout

**This program will move every single `<prop>` inside `RBT_origin.xml` to `RBT_shift.xml` based on your point of reference.**

## General Use
1. Load a layout of any decoration that you want to move inside the game (**must be an isolated decoration**).
2. Spawn a new `<prop>` in a good anchor position, and save the layout as `RBT_origin`.
3. Load your destination layout, place the same `<prop>` you use previously anywhere you see fit, and save the layout as `RBT_shift`.
4. Move `RBT_origin` and `RBT_shift` to the same directory as your `GW2 DecoRBT.py` or `GW2 DecoRBT.exe`.
5. Run the program.

For demonstration, refer to: `https://youtube.com/shorts/j0plucAdZ1w?si=HBVfZ2hBtxycaYuV`

## Get It for Yourself
If you have no problem downloading some requirements and prefer the bare (no GUI) script, you can head to the `source` folder and copy the `GW2 DecoRBT.py`.
