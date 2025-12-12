import numpy as np
import open3d as o3d
import json


import os
import json

def load_class_config(start_path="."):
    """
    Load class_config.json by searching from a given path.

    Search order:
      1) start_path/class_config.json (if start_path is a dir)
      2) parent of start_path
      3) ./class_config.json

    Returns:
      class_config (dict), config_path (str)
    """
    candidates = []

    # If start_path is a directory, check inside it
    if os.path.isdir(start_path):
        candidates.append(os.path.join(start_path, "class_config.json"))

    # Parent folder of start_path
    parent = os.path.dirname(start_path)
    if parent:
        candidates.append(os.path.join(parent, "class_config.json"))

    # Fallback: current working directory
    candidates.append(os.path.join(".", "class_config.json"))

    for path in candidates:
        if os.path.isfile(path):
            with open(path, "r") as f:
                cfg = json.load(f)
            return cfg, path

    raise FileNotFoundError(
        "class_config.json not found. Tried:\n" + "\n".join(candidates)
    )


def load_txt(filepath):
    data = np.loadtxt(filepath, dtype=np.float32)
    if data.ndim == 1:
        data = data[None, :]
    return data[:, :10]   # xyzrgbINor


def save_txt(filepath, points):
    """Save point cloud data to a .txt file."""
    np.savetxt(filepath, points, fmt='%.6f')


def readPLY(filepath):
    pcd = o3d.io.read_point_cloud(filepath)
    pcd = np.hstack([pcd.points, pcd.colors]).astype(np.float32)
    return pcd


def txt_to_ply(txt_path, ply_path):
    pcd = load_txt(txt_path)
    output_cloud = o3d.geometry.PointCloud()
    output_cloud.points = o3d.utility.Vector3dVector(pcd[:, :3])
    output_cloud.colors = o3d.utility.Vector3dVector(pcd[:, 3:6])
    o3d.io.write_point_cloud(ply_path, output_cloud)
    print('Saved',len(pcd),'points to',ply_path)



def align_to_manhattan(pcd):
    """
    Align the point cloud to the dominant horizontal axis (Manhattan World).
    Returns:
        rotated_pcd  : (N, C) rotated point cloud
        theta_deg    : rotation angle in degrees (for restoration or downstream use)
    """
    xy = pcd[:, :2]
    mean_xy = xy.mean(axis=0)
    xy_centered = xy - mean_xy

    # PCA: get principal axis via SVD & Compute angle to rotate
    _, _, vh = np.linalg.svd(xy_centered, full_matrices=False)
    principal_dir = vh[0]  # dominant direction
    theta = np.arctan2(principal_dir[1], principal_dir[0])  # radians
    theta_deg = np.degrees(theta)

    # Rotate by -theta to align principal direction to x-axis
    cos_t, sin_t = np.cos(-theta), np.sin(-theta)
    R = np.array([[cos_t, -sin_t],
                  [sin_t,  cos_t]])

    rotated_xy = (R @ xy_centered.T).T + mean_xy
    rotated_points = np.hstack([rotated_xy, pcd[:, 2:]])

    return rotated_points, theta_deg


def restore_lidar_scan_order(pcd):
    """
    Reorder points to approximate the LiDAR scanning sequence
    using azimuth-elevation quantization and lexicographic sorting.
    """

    x, y, z = pcd[:, 0], pcd[:, 1], pcd[:, 2]
    azimuth = np.arctan2(y, x)      # horizontal angle
    elevation = np.arcsin(z / (np.linalg.norm(pcd[:,0:3], axis=1) + 1e-6))

    az_deg = np.rad2deg(azimuth) % 360
    el_deg = np.rad2deg(elevation)

    # Quantize steps (10 deg steps)
    steps = 0.5
    az_step = np.round(az_deg / steps).astype(int)
    el_step = np.round(el_deg / steps).astype(int)

    # print(np.lexsort((el_step, az_step)))
    sort_idx = np.lexsort((el_step, az_step))

    # Sort first by elevation, then azimuth (like a vertical spinning LiDAR)
    return pcd[sort_idx]
