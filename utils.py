import numpy as np
import open3d as o3d

import os

def load_txt(filepath):
    """Load a .txt file with xyzrgbI or similar format."""
    return np.loadtxt(filepath)

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


# function to downsample a point cloud
def downsample(pcd, resolution=0.01, decimal_preserved=True):
    cloud = pcd.copy()
    voxel_set = set()
    output_cloud = []

    idx = np.round(cloud[:, :3]/resolution).astype(int)
    voxels = [tuple(k) for k in idx]
    
    if not decimal_preserved:
        cloud[:, :3] = idx * resolution

    for i in range(len(voxels)):
        if not voxels[i] in voxel_set:
            output_cloud.append(cloud[i])
            voxel_set.add(voxels[i])
    return np.array(output_cloud) 


def align_to_manhattan_grid(pcd):

    # Step 1: Use only x and y
    xy = pcd[:, :2]
    
    # Step 2: Center the points
    mean_xy = xy.mean(axis=0)
    xy_centered = xy - mean_xy

    # Step 3: PCA: get principal axis via SVD
    _, _, vh = np.linalg.svd(xy_centered, full_matrices=False)
    principal_dir = vh[0]  # dominant direction

    # Step 4: Compute angle to rotate this direction to x-axis
    theta = np.arctan2(principal_dir[1], principal_dir[0])  # radians
    theta_deg = np.degrees(theta)

    # Step 5: Rotate by -theta to align principal direction to x-axis
    cos_t, sin_t = np.cos(-theta), np.sin(-theta)
    R = np.array([[cos_t, -sin_t],
                  [sin_t,  cos_t]])

    # Apply rotation to xy part
    rotated_xy = (R @ xy_centered.T).T + mean_xy

    # Step 6: Compose rotated point cloud
    rotated_points = np.hstack([rotated_xy, pcd[:, 2:]])

    return rotated_points, theta_deg


def point_reorder(pcd):
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
