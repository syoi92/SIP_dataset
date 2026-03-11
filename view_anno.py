import os
import sys
import json
import numpy as np
import argparse

from utils import load_txt, save_txt, load_class_config, normalize_class_name


def save_ply_open3d(output_path, points_xyzrgb):
    """
    Save point cloud as PLY using Open3D.
    points_xyzrgb: Nx6 array [x y z r g b], RGB in 0-1
    """
    import open3d as o3d

    xyz = points_xyzrgb[:, :3].astype(np.float64)
    rgb = points_xyzrgb[:, 3:6].astype(np.float64)

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz)
    pcd.colors = o3d.utility.Vector3dVector(rgb)

    o3d.io.write_point_cloud(output_path, pcd)
    print(f"Saved colorized annotation to {output_path}")


def load_original_scan_xyzrgb(scan_dir, scan_id):
    """
    Load original scan file from scans/<scan_id>.txt
    Returns Nx6 array [x y z r g b], RGB normalized to 0-1.
    """
    scan_path = os.path.join(scan_dir, scan_id + ".txt")
    if not os.path.isfile(scan_path):
        raise FileNotFoundError(f"Original scan file not found: {scan_path}")

    points = load_txt(scan_path)
    if points.ndim == 1:
        points = points[None, :]

    if points.shape[1] < 6:
        raise ValueError(f"Original scan file has {points.shape[1]} columns, expected ≥ 6.")

    xyz = points[:, :3]
    rgb = points[:, 3:6].astype(np.float32)

    # Convert to 0-1 only if stored as 0-255
    if rgb.max() > 1.0:
        rgb = rgb / 255.0

    return np.concatenate([xyz, rgb], axis=1)


def build_annotated_xyzrgb(scan_dir, class_colormap):
    """
    Build merged annotated point cloud.
    Returns Nx7 array [x y z r g b intensity], where RGB is normalized to 0-1.
    """
    scan_id = os.path.basename(scan_dir.strip("/"))
    anno_dir = os.path.join(scan_dir, "Annotation")

    if not os.path.isdir(anno_dir):
        raise FileNotFoundError(f"Annotation directory not found: {anno_dir}")

    print(f"Color coding for {scan_id}")

    colored_points = []
    for filename in sorted(os.listdir(anno_dir)):
        if not filename.endswith(".txt"):
            continue

        cls_stem = os.path.splitext(filename)[0]
        cls_norm = normalize_class_name(cls_stem)

        color = None
        if cls_norm in class_colormap:
            color = class_colormap[cls_norm]
        else:
            for class_name, class_color in class_colormap.items():
                class_norm = normalize_class_name(class_name)
                if cls_norm == class_norm:
                    color = class_color
                    break

        if color is None:
            print(f"Warning: Could not resolve class for {filename}")
            print(cls_norm)
            continue

        points = load_txt(os.path.join(anno_dir, filename))  # xyzrgbI
        if points.ndim == 1:
            points = points[None, :]

        if points.shape[1] < 7:
            raise ValueError(f"{filename} has {points.shape[1]} columns, expected ≥ 7.")

        rgb = np.tile(color, (points.shape[0], 1))
        merged = np.concatenate([points[:, :3], rgb, points[:, 6:7]], axis=1)
        colored_points.append(merged)

    if not colored_points:
        raise RuntimeError(f"No valid annotated points found in {anno_dir}.")

    return np.vstack(colored_points)


def view_anno(scan_dir, output_dir, class_colormap, export_ply=False):
    scan_id = os.path.basename(scan_dir.strip("/"))
    os.makedirs(output_dir, exist_ok=True)

    merged_points = build_annotated_xyzrgb(scan_dir, class_colormap)

    if export_ply:
        annotated_ply = os.path.join(output_dir, scan_id + "_annotated.ply")
        original_ply = os.path.join(output_dir, scan_id + "_original.ply")

        save_ply_open3d(annotated_ply, merged_points[:, :6])

        original_xyzrgb = load_original_scan_xyzrgb(scan_dir, scan_id)
        save_ply_open3d(original_ply, original_xyzrgb)

    else:
        output_path = os.path.join(output_dir, scan_id + "_annotated.txt")
        save_txt(output_path, merged_points)
        print(f"Saved colorized annotation to {output_path}")


def main(scan_dir, output_dir, export_ply=False):
    class_config, cfg_path = load_class_config(scan_dir)
    print(f"Loaded class_config from: {cfg_path}")

    class_colormap = {
        normalize_class_name(v["name"]): np.array(v["color"], dtype=np.float32)
        for v in class_config.values()
    }

    view_anno(scan_dir, output_dir, class_colormap, export_ply=export_ply)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--scan-dir", type=str, required=True,
                        help="Path to a single scan folder (e.g., SIP-v1.0_Indoor/0a92e569-...).",)
    parser.add_argument("--output", type=str, required=True,
                        help="Output folder to save the merged colorized txt.",)
    parser.add_argument("--ply", action="store_true",
                        help="Also export the merged colorized annotation as a PLY file using Open3D.",)
    args = parser.parse_args()

    scan_folder = args.scan_dir
    output_folder = args.output

    print("========== Annotation Visualization ==========")
    print(f"Scan dir   : {scan_folder}")
    print(f"Output dir : {output_folder}")
    print("=============================================\n")

    main(scan_folder, output_folder, export_ply=args.ply)