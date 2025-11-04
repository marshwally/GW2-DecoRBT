# GW2-DecoRBT
Simple python script that could be run to automatically edit Guild Wars 2 saved homestead layout files.   

## Description
This program will reads two XML layout files, specifically named `RBT_origin` and `RBT_shift` to generate the output. The output XML is a Guild Wars 2 layout file with a combined `<props>` from both files.
> RBT_origin	= the decoration you want to move, and one new prop (point of reference)

> RBT_shift 	= the new prop (point of reference) inside the destination layout

## How to Use
1. Load any decoration layout that you want to move inside the game (**must be an isolated decoration**).
2. Spawn a new `<prop>` and place it in a good anchor position.
3. Save the layout as `RBT_origin`.
4. Load your destination layout where you want to use your decoration.
5. Spawn the same `<prop>` you use previously, and place it somewhere you want your decoration to be.
6. Save the layout as `RBT_shift`.
7. Move `RBT_origin` and `RBT_shift` to the same folder as your own `GW2 DecoRBT.py` or `GW2 DecoRBT.exe`.
8. Run the program.

For a demonstration, refer to: `https://youtube.com/shorts/j0plucAdZ1w?si=HBVfZ2hBtxycaYuV`

## How to get the program for yourself:
1. If you have no problem downloading some requirements, you can head to the `source` folder and copy the `GW2 DecoRBT.py` to your own PC.
2. If you don't want any requirements, look inside `executable` folder and download the `GW2 DecoRBT.exe` into your PC.
