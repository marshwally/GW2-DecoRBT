import os
import sys
import copy
import numpy as np
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# ============================================================
#  RESOURCE PATH HANDLING (works in PyInstaller and normal run)
# ============================================================
if getattr(sys, 'frozen', False):
    APP_DIR = sys._MEIPASS
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))

WORK_DIR = os.getcwd()  # where user keeps the XML files


# ============================================================
#  UTILITY FUNCTIONS
# ============================================================
def indent(elem, level=0, spaces_per_level=4):
    current_indent = "\n" + (" " * (level * spaces_per_level))
    child_indent = "\n" + (" " * ((level + 1) * spaces_per_level))

    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = child_indent

        for i, child in enumerate(elem):
            indent(child, level + 1, spaces_per_level)
            if not child.tail or not child.tail.strip():
                child.tail = child_indent if i < len(elem) - 1 else current_indent
    else:
        if not elem.tail or not elem.tail.strip():
            elem.tail = current_indent

def parse_vec(s):
    return np.array([float(v) for v in s.split()])

def fmt_vec(v):
    return f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}"


# ============================================================
#  MATRIX / ROTATION MATH
# ============================================================
def euler_to_matrix(rx, ry, rz, flip_z=False):
    if flip_z:
        rz = -rz
    cx, sx = np.cos(rx), np.sin(rx)
    cy, sy = np.cos(ry), np.sin(ry)
    cz, sz = np.cos(rz), np.sin(rz)

    Rx = np.array([[1, 0, 0], [0, cx, sx], [0, -sx, cx]])
    Ry = np.array([[cy, 0, -sy], [0, 1, 0], [sy, 0, cy]])
    Rz = np.array([[cz, sz, 0], [-sz, cz, 0], [0, 0, 1]])

    return Ry @ Rx @ Rz


def matrix_to_euler(R, flip_z=False):
    EPS = 1e-8
    rx = np.arcsin(np.clip(R[1, 2], -1.0, 1.0))

    if abs(np.cos(rx)) < EPS:
        ry = 0.0
        rz_prime = np.arctan2(R[0, 1], R[0, 0])
    else:
        ry = np.arctan2(-R[0, 2], R[2, 2])
        rz_prime = np.arctan2(-R[1, 0], R[1, 1])

    rz = -rz_prime if flip_z else rz_prime
    return np.array([rx, ry, rz])


# ============================================================
#  CORE TRANSFORMATION FUNCTION
# ============================================================
def apply_changes(file_origin, file_shift):
    tree_origin, tree_shift = ET.parse(file_origin), ET.parse(file_shift)
    root_origin, root_shift = tree_origin.getroot(), tree_shift.getroot()

    origin_props = root_origin.findall("prop")
    shift_props = root_shift.findall("prop")

    if not origin_props or not shift_props:
        raise Exception("Both XMLs must contain at least one <prop> element.")

    origin_parent = origin_props[-1]
    shift_parent = shift_props[-1]

    pos_origin, rot_origin = parse_vec(origin_parent.get("pos")), parse_vec(origin_parent.get("rot"))
    pos_shift, rot_shift = parse_vec(shift_parent.get("pos")), parse_vec(shift_parent.get("rot"))

    R_origin = euler_to_matrix(*rot_origin)
    R_shift = euler_to_matrix(*rot_shift)
    R_delta = R_shift @ R_origin.T

    new_root = ET.Element("Decorations", root_shift.attrib)

    for prop in shift_props:
        if prop is shift_parent:
            continue
        new_root.append(copy.deepcopy(prop))

    for prop in origin_props:
        new_prop = copy.deepcopy(prop)

        if prop is origin_parent:
            new_root.append(copy.deepcopy(shift_parent))
            continue

        pos = parse_vec(prop.get("pos"))
        rel = pos - pos_origin
        pos_new = pos_shift + rel @ R_delta.T
        new_prop.set("pos", fmt_vec(pos_new))

        rot = parse_vec(prop.get("rot"))
        R_child_old = euler_to_matrix(*rot)
        R_child_new = R_delta @ R_child_old
        new_rot = matrix_to_euler(R_child_new) % (2 * np.pi)
        new_prop.set("rot", fmt_vec(new_rot))

        new_root.append(new_prop)

    indent(new_root)

    origin_name = os.path.splitext(os.path.basename(file_origin))[0]
    output_path = os.path.join(WORK_DIR, f"{origin_name}_transformed.xml")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(ET.tostring(new_root, encoding="unicode"))

    return output_path


# ============================================================
#  GUI
# ============================================================
def start_gui():
    root = tk.Tk()
    root.title("GW2 DecoRBT")

    # Icon loading
    try:
        root.iconbitmap(os.path.join(APP_DIR, "GW2 DecoRBT logo.ico"))
    except:
        try:
            icon = tk.PhotoImage(file=os.path.join(APP_DIR, "GW2 DecoRBT logo.png"))
            root.iconphoto(True, icon)
        except:
            pass

    root.geometry("520x220")
    root.resizable(False, False)

    style = ttk.Style(root)
    style.theme_use("clam")

    root.option_add("*TLabel.Font", "SegoeUI 11")
    root.option_add("*TButton.Font", "SegoeUI 10")
    root.option_add("*TEntry.Font", "SegoeUI 10")

    frame = ttk.Frame(root, padding=15)
    frame.pack(fill="both", expand=True)

    # --- TEXT PLACEHOLDER ---
    def add_placeholder(entry, text):
        entry.insert(0, text)
        entry.config(foreground="gray")
        
        def on_focus_in(event):
            if entry.get() == text:
                entry.delete(0, tk.END)
                entry.config(foreground="black")

        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, text)
                entry.config(foreground="gray")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    # --- ENTRY ROW CREATOR ---
    def make_row(label_text, browse_cmd):
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=6)

        ttk.Label(row, text=label_text, width=20).pack(side="left")

        entry = ttk.Entry(row, width=22, foreground="#777")
        entry.pack(side="left", padx=6)
        placeholder_text = label_text.replace('Choose your ', '')
        add_placeholder(entry, f"(e.g. RBT_{placeholder_text.replace(' file:', '')}.xml)")

        ttk.Button(row, text="Browse", command=browse_cmd).pack(side="right")

        return entry

    # ------------ BROWSE FUNCTIONS ------------
    def select_origin():
        f = filedialog.askopenfilename(initialdir=WORK_DIR, filetypes=[("XML Files", "*.xml")])
        if f:
            entry_origin.delete(0, tk.END)
            entry_origin.config(foreground="black")
            entry_origin.insert(0, os.path.basename(f))
            entry_origin.fullpath = f

    def select_shift():
        f = filedialog.askopenfilename(initialdir=WORK_DIR, filetypes=[("XML Files", "*.xml")])
        if f:
            entry_shift.delete(0, tk.END)
            entry_shift.config(foreground="black")
            entry_shift.insert(0, os.path.basename(f))
            entry_shift.fullpath = f

    # ---------------- CREATE ENTRY FIELDS ----------------
    entry_origin = make_row("Choose your origin file:", select_origin)
    entry_shift = make_row("Choose your shift file:", select_shift)

    entry_origin.fullpath = None
    entry_shift.fullpath = None

    # ---------------- RUN BUTTON ----------------
    def run_gui_transform():
        try:
            if not entry_origin.fullpath:
                raise Exception("Please select the Origin XML file.")
            if not entry_shift.fullpath:
                raise Exception("Please select the Shift XML file.")

            output = apply_changes(entry_origin.fullpath, entry_shift.fullpath)
            messagebox.showinfo("Success", f"Output created:\n{output}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    ttk.Button(root, text="Run Transformation", command=run_gui_transform).pack(pady=10)

    root.mainloop()


# ============================================================
#  AUTO-MODE OR GUI
# ============================================================
DEFAULT_ORIGIN = os.path.join(WORK_DIR, "RBT_origin.xml")
DEFAULT_SHIFT = os.path.join(WORK_DIR, "RBT_shift.xml")

if os.path.isfile(DEFAULT_ORIGIN) and os.path.isfile(DEFAULT_SHIFT):
    try:
        output_path = apply_changes(DEFAULT_ORIGIN, DEFAULT_SHIFT)
        print(f"Transformation complete: {output_path}")
        sys.exit(0)
    except Exception as e:
        print("Error:", e)

# If not both XMLs exist → show GUI
start_gui()
