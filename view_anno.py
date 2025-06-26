import os
import sys
import json
import numpy as np
from utils import load_txt, save_txt


def main(scan_dir, output_dir):
    ## sample
    # scan_dir = "./sip-indoor/0a92e569-daf9-4d7a-8505-8fd0e6302379"
    # output_dir = "./"
    
    # Load class config json
    try:
        class_config_path = os.path.join(os.path.dirname(scan_dir), 'class_config.json')
        with open(class_config_path, 'r') as f:
            class_config = json.load(f)
    except FileNotFoundError:
        # Try fallback path: current working directory
        try:
            class_config_path = './class_config.json'
            with open(class_config_path, 'r') as f:
                class_config = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("class_config.json not found in either parent of scan_dir or current directory.")

    view_anno(scan_dir, output_dir, class_config)
    

def view_anno(scan_dir, output_dir, class_config):
    scan_id = os.path.basename(scan_dir.strip("/"))
    anno_dir = os.path.join(scan_dir, 'Annotation')
    print(f"Color coding for {scan_id}")

    colored_points = []
    for filename in os.listdir(anno_dir):
        if filename.endswith('.txt'):
            itr_class = os.path.splitext(filename)[0].lower()
            itr_color = None

            for _, class_info in class_config.items():
                class_name = class_info["name"].lower()
                if itr_class.startswith(class_name) or class_name in itr_class:
                    itr_color = class_info["color"]  
                    break
            
            if itr_color is None:
                print(f"Warning: Could not resolve class for {filename}")
                continue

            points = load_txt(os.path.join(anno_dir, filename))  # xyzrgbI
            rgb = np.tile(np.array(itr_color), (points.shape[0], 1))  # assign class color
            merged = np.concatenate([points[:, :3], rgb, points[:, 6:7]], axis=1)  # xyz + class color + I
            colored_points.append(merged)

    # Merge and save
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    merged_points = np.vstack(colored_points)
    output_path = os.path.join(output_dir, scan_id + '_annotated.txt')
    save_txt(output_path, merged_points)

    print(f"Saved colorized annotation to {output_path}")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python view_anno.py [scan_folder] [output_folder]")
        sys.exit(1)

    scan_folder = sys.argv[1]
    output_folder = sys.argv[2]
    print(f"Scan_dir: {scan_folder} && output_dir: {output_folder}")
    main(scan_folder, output_folder)
