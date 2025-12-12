import os
import sys
import json
import numpy as np
import argparse

from utils import load_txt, save_txt, load_class_config


def view_anno(scan_dir, output_dir, class_colormap):
    scan_id = os.path.basename(scan_dir.strip("/"))
    anno_dir = os.path.join(scan_dir, 'Annotation')

    if not os.path.isdir(anno_dir):
        raise FileNotFoundError(f"Annotation directory not found: {anno_dir}")

    print(f"Color coding for {scan_id}")

    colored_points = []
    for filename in os.listdir(anno_dir):
        if not filename.endswith(".txt"):
            continue
 
        cls_stem = os.path.splitext(filename)[0].lower()
        color = None

        for class_name, class_color in class_colormap.items():
            if cls_stem.startswith(class_name) or class_name in cls_stem:
                color = class_color
                break

        if color is None:
            print(f"Warning: Could not resolve class for {filename}")
            continue


        points = load_txt(os.path.join(anno_dir, filename))  # xyzrgbI
        if points.shape[1] < 7:
            raise ValueError(f"{filename} has {points.shape[1]} columns, expected ≥ 7.")

        rgb = np.tile(color, (points.shape[0], 1))
        merged = np.concatenate([points[:, :3], rgb, points[:, 6:7]], axis=1)
        colored_points.append(merged)

    if not colored_points:
        raise RuntimeError(f"No valid annotated points found in {anno_dir}.")

    # Merge and save
    os.makedirs(output_dir, exist_ok=True)

    merged_points = np.vstack(colored_points)
    output_path = os.path.join(output_dir, scan_id + '_annotated.txt')
    save_txt(output_path, merged_points)

    print(f"Saved colorized annotation to {output_path}")



def main(scan_dir, output_dir):

    class_config, cfg_path = load_class_config(scan_dir)
    print(f"Loaded class_config from: {cfg_path}")

    class_colormap = {
        v["name"].lower(): np.array(v["color"], dtype=np.float32)
        for v in class_config.values()
    }

    view_anno(scan_dir, output_dir, class_colormap)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--scan-dir", type=str, required=True,
                        help="Path to a single scan folder (e.g., SIP-v1.0_Indoor/0a92e569-...).",)
    parser.add_argument("--output", type=str, required=True,
                        help="Output folder to save the merged colorized txt.",)
    args = parser.parse_args()

    scan_folder = args.scan_dir
    output_folder = args.output

    print("========== Annotation Visualization ==========")
    print(f"Scan dir   : {scan_folder}")
    print(f"Output dir : {output_folder}")
    print("=============================================\n")

    main(scan_folder, output_folder)