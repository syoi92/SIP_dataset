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
def downsample(cloud, resolution):
    voxel_set = set()
    output_cloud = []
    voxels = [tuple(k) for k in np.round(cloud[:, :3]/resolution).astype(int)]
    for i in range(len(voxels)):
        if not voxels[i] in voxel_set:
            output_cloud.append(cloud[i])
            voxel_set.add(voxels[i])
    return np.array(output_cloud) 
