import copy
import numpy as np
import xml.etree.ElementTree as ET

# ----------- Utility Functions -----------
def get_prop_signature(prop):
    return (
        f"{prop.get('id', '')}|{prop.get('name', '')}|{prop.get('pos', '')}|{prop.get('rot', '')}|{prop.get('scl', '')}"
    )

def indent(elem, level=0, spaces_per_level=4):
    current_indent = "\n" + (" " * (level * spaces_per_level))
    child_indent = "\n" + (" " * ((level + 1) * spaces_per_level))

    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = child_indent

        for i, child in enumerate(elem):
            indent(child, level + 1, spaces_per_level)
            if not child.tail or not child.tail.strip():
                if i < len(elem) - 1:
                    child.tail = child_indent
                else:
                    child.tail = current_indent
    else:
        if not elem.tail or not elem.tail.strip():
            elem.tail = current_indent

# ----------- Math Functions -----------
def parse_vec(s):
    return np.array([float(v) for v in s.split()])

def fmt_vec(v):
    return f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}"
    
def euler_to_matrix(rx, ry, rz, flip_z=False): 
    # Intrinsic YXZ / Extrinsic ZXY convention -> following the game system
    if flip_z:
        rz = -rz
    cx, sx = np.cos(rx), np.sin(rx)
    cy, sy = np.cos(ry), np.sin(ry)
    cz, sz = np.cos(rz), np.sin(rz)
    
    Rx = np.array([[1,0,0],[0,cx,sx],[0,-sx,cx]])
    Ry = np.array([[cy,0,-sy],[0,1,0],[sy,0,cy]])
    Rz = np.array([[cz,sz,0],[-sz,cz,0],[0,0,1]])
    
    return Ry @ Rx @ Rz

def matrix_to_euler(R, flip_z=False):
    EPS = 1e-8
    rx = np.arcsin(np.clip(R[1, 2], -1.0, 1.0))

    # Check for gimbal lock: cos(rx) ≈ 0
    if abs(np.cos(rx)) < EPS:
        # Gimbal lock: X rotation is ±90° -> Y and Z become coupled
        ry = 0.0
        rz_prime = np.arctan2(R[0, 1], R[0, 0])
    else:
        # Normal case
        ry = np.arctan2(-R[0, 2], R[2, 2])
        rz_prime = np.arctan2(-R[1, 0], R[1, 1])

    rz = -rz_prime if flip_z else rz_prime

    return np.array([rx, ry, rz])

# ----------- Core Function -----------
def apply_changes(file_origin, file_shift, file_output):
    tree_origin, tree_shift = ET.parse(file_origin), ET.parse(file_shift)
    root_origin, root_shift = tree_origin.getroot(), tree_shift.getroot()
    origin_props, shift_props = root_origin.findall("prop"), root_shift.findall("prop")

    if not origin_props or not shift_props:
        raise Exception("Both XMLs must contain at least one <prop> element.")
    
    # Last prop as parent
    origin_parent = origin_props[-1]
    shift_parent = shift_props[-1]

    # Pick _origin and _shift parent's position and rotation
    pos_origin, rot_origin = parse_vec(origin_parent.get("pos")), parse_vec(origin_parent.get("rot"))
    pos_shift, rot_shift = parse_vec(shift_parent.get("pos")), parse_vec(shift_parent.get("rot"))
    
    R_origin = euler_to_matrix(*rot_origin)
    R_shift = euler_to_matrix(*rot_shift)
    
    R_delta = R_shift @ R_origin.T
    
    # Create new XML root for the output -> take header data from _shift, enabling map change
    new_root = ET.Element("Decorations", root_shift.attrib)
    
    # Copy all props in _shift
    for prop in shift_props:
        saved_prop = copy.deepcopy(prop)
        
        # If it is parent, skip
        if prop is shift_parent:
            continue
            
        new_root.append(saved_prop)

    # Apply transformation to all props in _origin
    for prop in origin_props:
        new_prop = copy.deepcopy(prop)

        # If it is the parent 
        if prop is origin_parent:
            # Use the one from _shift
            new_root.append(copy.deepcopy(shift_parent))
            continue

        # --- Position ---
        pos = parse_vec(prop.get("pos"))
        rel = pos - pos_origin
        new_pos = pos_shift + rel @ R_delta.T
        
        new_prop.set("pos", fmt_vec(new_pos))

        # --- Rotation ---
        rot = parse_vec(prop.get("rot"))
        R_child_old = euler_to_matrix(*rot)
        R_child_new = R_delta @ R_child_old
        new_rot = matrix_to_euler(R_child_new)
        new_rot = new_rot % (2 * np.pi)
        
        new_prop.set("rot", fmt_vec(new_rot))

        new_root.append(new_prop)
    
    # Insert white-spaces to beautify the format
    indent(new_root)

    # Write XML output
    with open(file_output, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(ET.tostring(new_root, encoding="unicode"))

    print(f"New XML written to: {file_output}")

# ---------------- Usage ----------------
if __name__ == "__main__":
    try:
        apply_changes("RBT_origin.xml", "RBT_shift.xml", "RBT_transformed.xml")
    except Exception as e:
        print(f"An unnexpected error occurred: {e}")