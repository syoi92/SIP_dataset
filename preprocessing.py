import os
import json
import numpy as np
from glob import glob
from tqdm import tqdm
import argparse

from utils import load_txt, load_class_config, normalize_class_name, restore_lidar_scan_order

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def resolve_split_path(root, src_split):
    """
    Default: use split.json next to this script if present, else <root>/split.json.
    If src_split: always use <root>/split.json.
    """
    input_split = os.path.join(root, "split.json")
    local_split = os.path.join(_SCRIPT_DIR, "split.json")

    if src_split:
        if not os.path.isfile(input_split):
            raise FileNotFoundError(f"split.json not found in input folder: {input_split}")
        return input_split

    if os.path.isfile(local_split):
        return local_split
    if os.path.isfile(input_split):
        return input_split
    raise FileNotFoundError(
        f"split.json not found. Tried:\n  {local_split}\n  {input_split}"
    )


def load_splits(split_path):
    with open(split_path, "r") as f:
        sp = json.load(f)

    splits = {}
    for scan_id, info in sp.items():
        split = (info.get("set") or info.get("split") or "").lower()
        if split in ["train", "val", "test"]:
            splits[scan_id] = split
    return splits


def process_scan(scan_dir, name_to_index, only_target=False):
    anno_dir = os.path.join(scan_dir, "Annotation")
    pts_list = []

    for anno_path in glob(os.path.join(anno_dir, "*.txt")):
        raw_name = os.path.splitext(os.path.basename(anno_path))[0]
        cls_name = normalize_class_name(raw_name)

        if only_target and (cls_name not in name_to_index):
            continue

        label = name_to_index[cls_name] if cls_name in name_to_index else -1
        print("name-label:", raw_name, "->", cls_name, label)
        pts = load_txt(anno_path)
        semantic = np.full((pts.shape[0], 1), label, dtype=np.int64)
        pts_list.append(np.hstack([pts, semantic]))

    if not pts_list:
        return None

    allpts = np.vstack(pts_list)
    allpts = restore_lidar_scan_order(allpts)

    data = {
        "coord":      allpts[:, 0:3].astype(np.float64),
        "rgb":        allpts[:, 3:6].astype(np.float64),
        "intensity":  allpts[:, 6:7].astype(np.float64),
        "normal":     allpts[:, 7:10].astype(np.float64),
        "semantic_gt": allpts[:, 10:11].astype(np.int64),
        "theta": np.array([0.0], dtype=np.float32),
    }
    
    data["index_valid_keys"] = [
        "coord",
        "color",
        "normal",
        "intensity",
        "segment"
    ]

    return data

def preprocess(root, out_root, split_path, ext="pth", only_target=False):
    ext = ext.lower().lstrip(".")
    if ext not in {"pth", "npz"}:
        raise ValueError(f'ext must be "pth" or "npz", got {ext!r}')
    if ext == "pth":
        import torch

    class_config, cfg_path = load_class_config(root)

    indexed_items = sorted(
        [(int(k), v["name"].lower()) for k, v in class_config.items() if v.get("indexed", False)],
        key=lambda x: x[0]
    )
    indexed_name_to_newid = {name: new_id for new_id, (_, name) in enumerate(indexed_items)}
    class_label_map = {
        v["name"].lower(): (indexed_name_to_newid[v["name"].lower()])
        for _, v in class_config.items() if v.get("indexed", False)
    }
    
    print(f"Loaded class_config from: {cfg_path}")
    print(f"class_label_map: {class_label_map}")   # Only indexed classes

    print(f"Using split file: {split_path}")
    splits = load_splits(split_path)

    os.makedirs(out_root, exist_ok=True)
    for s in ["train", "val", "test"]:
        os.makedirs(os.path.join(out_root, s), exist_ok=True)


    scan_dirs = [d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))]

    for scan_id in tqdm(scan_dirs):
        if scan_id not in splits:
            continue
        
        data = process_scan(os.path.join(root, scan_id), class_label_map, only_target=only_target)
        if data is None:
            continue

        split = splits[scan_id]
        out_path = os.path.join(out_root, split, f"{scan_id}.{ext}")
        if ext == "pth":
            torch.save(data, out_path)
        else:
            np.savez_compressed(out_path, **data)
        
    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=str, required=True,
                        help="Path to SIP-v1.0_Indoor or SIP-v1.0_Outdoor")
    parser.add_argument("--output", type=str, default=None,
                        help="Output folder (default: <root>_processed)")
    parser.add_argument("--only-target", action="store_true",
                        help="Drop annotations not listed as indexed/target classes (default: keep them as label -1).")
    parser.add_argument(
        "--ext",
        type=str,
        choices=["pth", "npz"],
        default="pth",
        help='Output format: "pth" (torch.save) or "npz" (numpy).',
    )
    parser.add_argument(
        "--src-split",
        action="store_true",
        dest="src_split",
        help="Use split.json from the input folder (--root) only (ignore split next to this script).",
    )
    args = parser.parse_args()

    root = os.path.abspath(os.path.expanduser(args.root))
    out_root = args.output or (root + "_processed")
    split_path = resolve_split_path(root, args.src_split)

    print("========== Preprocessing ====================")
    print(f"Input folder    : {root}")
    print(f"Output folder   : {out_root}")
    print(f"Split file      : {split_path}")
    print(f"Output ext      : {args.ext}")
    print(f"Only target     : {args.only_target}")
    print(f"src_split       : {args.src_split}")
    print("=============================================\n")

    preprocess(root, out_root, split_path=split_path, ext=args.ext, only_target=args.only_target)