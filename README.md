# SIP_dataset
Sites in Pieces: A SIP dataset of disaggregated 3D scans for construction-phase segmentation.

<p align="center">
<img src="imgs/sip-dataset.png" alt="" width="100%">
<img src="imgs/characteristics.png" alt="" width="100%">
</p>

- A unit of individual scans
- Scenes captured during construction through FARO lidar, including structure components and temporary construction objects

## Instructions

### Download: SIP-Indoor 

```
wget [URLURLURL] -O sip-indoor.zip
unzip sip-indoor.zip && rm sip-indoor.zip
cd sip-indoor
```
Or using `curl`:
```
curl -L "[URLURLURL]" -o sip-indoor.zip
unzip sip-indoor.zip && rm sip-indoor.zip
```

### Download: SIP-Outdoor (extension) 
```
wget [URLURLURL] -O sip-outdoor.zip
```

### Directory Structure
```
SIP-Indoor/
  │ class_info.json
  │ splits.json
  └─Scans/
    │ scan.txt [xyzrgbI] - original scan (pre-annotation)
    └─Annotation/
        │ class1.txt [xyzrgbI]
        │ class2.txt
        │ ⋮ 
        └─classN.txt
```

- **class_info.json** — Defines class labels and RGB colors for visualization. The `indexed` flag indicates classes intended for training and evaluation, which can be adjusted as needed.

- **splits.json** — Maps each scan to a dataset split (train or test), following the convention used.







## Class List
**Indexed Classes** (used for SIP-indoor evaluation):  
**0: wall, 1: ceiling, 2: floor, 3: pipes, 4: column, 5: ladder, 6: stair** 

**Non-Indexed** (auxiliary / context only):  
**7: frame, 8: lift, 9: mtrl**, 10: guardrails, 11: door, 12: ground, 13: vehicle, 14: tree, 15: fence, 16: scaffolding, 17: portajohn, 18: container, 19: monument, 20: girder, 21: awning, 22: clutter


> *Only the bolded classes appear in SIP-Indoor scenes.*



## 📄 License

This repository contains two types of content with separate licenses:

- 📦 **Dataset**: Licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).  
  You are free to share and adapt the dataset for non-commercial purposes with proper attribution.

- 🧑‍💻 **Code**: Licensed under the [MIT License](./LICENSE.md).