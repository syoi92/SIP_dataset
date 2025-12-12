import os
import json
import numpy as np
from glob import glob
from tqdm import tqdm
import argparse

from utils import load_txt, load_class_config, restore_lidar_scan_order, align_to_manhattan


def load_splits(split_path):
    with open(split_path, "r") as f:
        sp = json.load(f)

    splits = {}
    for scan_id, info in sp.items():
        split = (info.get("set") or info.get("split") or "").lower()
        if split in ["train", "val", "test"]:
            splits[scan_id] = split
    return splits


def process_scan(scan_dir, name_to_index, apply_manhattan=False):
    anno_dir = os.path.join(scan_dir, "Annotation")
    pts_list = []

    for anno_path in glob(os.path.join(anno_dir, "*.txt")):
        cls_name = os.path.splitext(os.path.basename(anno_path))[0].lower()
        if cls_name not in name_to_index:
            continue
        
        label = name_to_index[cls_name]
        pts = load_txt(anno_path)
        semantic = np.full((pts.shape[0], 1), label, dtype=np.int64)
        pts_list.append(np.hstack([pts, semantic]))

    if not pts_list:
        return None

    allpts = np.vstack(pts_list)
    allpts = restore_lidar_scan_order(allpts)

    if apply_manhattan:
        allpts, theta = align_to_manhattan(allpts)
    else:
        theta = 0.0

    return {
        "coord":      allpts[:, 0:3],
        "rgb":        allpts[:, 3:6],
        "intensity":  allpts[:, 6:7],
        "normal":     allpts[:, 7:10],
        "semantic_gt": allpts[:, 10:11],
        "theta": np.array([theta], dtype=np.float32),
    }

def preprocess(root, out_root, apply_manhattan=False):

    class_config, cfg_path = load_class_config(root)
    
    class_label_map = {
        v["name"].lower(): int(k)
        for k, v in class_config.items()
        if v.get("indexed", False)
    }

    print(f"Loaded class_config from: {cfg_path}")
    print(f"Indexed classes: {list(class_label_map.keys())}")   # Only indexed classes

    splits = load_splits(os.path.join(root, "split.json"))

    os.makedirs(out_root, exist_ok=True)
    for s in ["train", "val", "test"]:
        os.makedirs(os.path.join(out_root, s), exist_ok=True)


    scan_dirs = [d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))]

    for scan_id in tqdm(scan_dirs):
        if scan_id not in splits:
            continue
        
        data = process_scan(os.path.join(root, scan_id), class_label_map, apply_manhattan=apply_manhattan)
        if data is None:
            continue

        split = splits[scan_id]
        out_path = os.path.join(out_root, split, f"{scan_id}.npz")
        np.savez_compressed(out_path, **data)

        # import torch
        # out_path = os.path.join(out_root, split, f"{scan_id}.pth")
        # torch.save(data, out_path)
        
    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=str, required=True,
                        help="Path to SIP-v1.0_Indoor or SIP-v1.0_Outdoor")
    parser.add_argument("--output", type=str, default=None,
                        help="Output folder (default: <root>_processed)")
    parser.add_argument("--align-manhattan", action="store_true",
                        help="Align point clouds to Manhattan World (principal axis).")
    args = parser.parse_args()

    root = os.path.abspath(args.root)
    out_root = args.output or (root + "_processed")

    print("========== Preprocessing ====================")
    print(f"Input folder    : {root}")
    print(f"Output folder   : {out_root}")
    print(f"Align Manhattan : {args.align_manhattan}")
    print("=============================================\n")


    preprocess(root, out_root, args.align_manhattan)