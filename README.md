# SIP_dataset
Sites in Pieces: A SIP dataset of disaggregated 3D scans for construction-phase segmentation.

<figure style="text-align: center;">
  <img src="imgs/sip-dataset.png" alt="SIP dataset overview" width="100%">
  <img src="imgs/characteristics.png" alt="Dataset characteristics" width="90%">
</figure>

- A unit of individual scans
- Scenes captured during construction through FARO lidar, including structure components and temporary construction objects



## Class List
### **Indexed Classes** (used for SIP-indoor evaluation):  
**0: wall, 1: ceiling, 2: floor, 3: pipes, 4: column, 5: ladder, 6: stair** 

### **Non-Indexed** (auxiliary / context only):  
**7: frame, 8: lift, 9: mtrl**, 10: guardrails, 11: door, 12: ground, 13: vehicle, 14: tree, 15: fence, 16: scaffolding, 17: portajohn, 18: container, 19: monument, 20: girder, 21: awning, 22: clutter


> *Only the bolded classes appear in SIP-Indoor scenes.*


## Instructions

### Download: SIP-Indoor 

```bash
wget [URLURLURL] -O sip-indoor.zip
unzip sip-indoor.zip && rm sip-indoor.zip
cd sip-indoor
```
Or using `curl`:
```bash
curl -L "[URLURLURL]" -o sip-indoor.zip
unzip sip-indoor.zip && rm sip-indoor.zip
```

### Download: SIP-Outdoor (extension) 
```bash
wget [URLURLURL] -O sip-outdoor.zip
```

### Directory Structure
```
sip-indoor/
  │ class_config.json
  │ splits.json
  └─scans/
    │ scan.txt [xyzrgbI] - original scan (pre-annotation)
    └─Annotation/
        │ class1.txt [xyzrgbI]
        │ class2.txt
        │ ⋮ 
        └─classN.txt
```

- **class_info.json** — Defines class labels and RGB colors for visualization. The `indexed` flag indicates classes intended for training and evaluation, which can be adjusted as needed.

- **splits.json** — Maps each scan to a dataset split (train or test), following the convention used.


## Visulization

To visualize annotations, use the `view_anno.py` script. It reads a scan and its class-wise annotations, applies color mappings from `class_config.json`, and generates a merged colorized `.txt` file.



```bash
python view_anno.py sip-indoor/scans/[scan_id] [output_folder]
```
- [scan_id]: folder containing scan.txt and its Annotation/ directory
- [output_folder]: destination for the merged, colorized .txt file  

*Replace items in [brackets] with your own values.*

### Viewing with CloudCompare
The `.txt` files can be directly loaded into [CloudCompare](https://www.danielgm.net/cc/). If needed, you can convert `.txt` to `.ply` using the provided `utils.py` script.



## 📄 License

- **Dataset**: Licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/); **Code**: Licensed under the [MIT License](./LICENSE.md).  

*You are free to share and adapt the dataset for non-commercial purposes with proper attribution.*