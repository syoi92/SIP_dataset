# SIP_dataset
Sites in Pieces: A SIP dataset of disaggregated 3D scans for construction-phase segmentation (formerly CnstPCIM dataset)

<figure style="text-align: center;">
  <img src="imgs/sip-dataset.png" alt="SIP dataset overview" width="100%">
  <table>
    <tr>
      <td><img src="imgs/e1-a.png" alt="RGB"></td>
      <td><img src="imgs/e1-b.png" alt="Intensity"></td>
      <td><img src="imgs/e1-c.png" alt="Normal"></td>
      <td><img src="imgs/e1-d.png" alt="Annotation"></td>
    </tr>
    <tr>
      <td align="center">RGB</td>
      <td align="center">Lidar Intensity</td>
      <td align="center">Surface Normal</td>
      <td align="center">Annotation</td>
    </tr>
  </table>
</figure>

- **Single-scan FARO LiDAR scenes** that retain real-world occlusion, density imbalance, and restricted visibility—conditions that multi-scan registration often removes. **Uniform-ratio sampled** to match a 0.03 m voxel-equivalent density while preserving the essential geometric characteristics of the original single scans.

- **Collected throughout construction phases**, capturing both permanent structural components and temporary construction objects integral to on-site operations.
<figure style="text-align: center;">
  <img src="imgs/characteristics.png" alt="Dataset characteristics" width="70%">
</figure>

<!-- ## Overview

- [Instructions](#instructions)
- [Class List](#class-list)
- [Visualization](#visualization)
- [License](#license) -->


## Class Taxonomy
We organize SIP classes into three semantic groups reflecting their role on the jobsite:

- **A. Built Environment Elements** – Permanent or in-progress components of the built structure.  
  - *A1. Permanent Structural Components* – wall, ceiling, floor, column, stair, girder  
  - *A2. In-Progress Built Components* – pipes, frame, window, door, awning  

- **B. Construction Operations Elements** – Elements that support construction activities, on-site operations, and the handling or movement of equipment and materials.  
  - *B1. Works & Access Structures* – guardrails, fence, scaffolding  
  - *B2. Operational Equipment* – ladder, lift  
  - *B3. Site Logistics* – mtrl, portajohn, container  

- **C. Environmental Objects** – Natural or site-context elements that are not part of the constructed facility.  
  - ground, tree, monument, vehicle


## Directory Structure
```
sip-indoor/
  │ class_config.json
  │ splits.json
  └─scans/
    │ scan.txt [xyzrgbINor] - original scan (Before annotation)
    └─Annotation/
        │ class1.txt [xyzrgbINor]
        │ class2.txt
        │ ⋮ 
        └─classN.txt

sip-outdoor/
  │ ⋮ 
  └─
```


- *class_info.json* — Defines class labels and their color codes for visualization. The `indexed` flag specifies which classes are intended for benchmarking. 

- *splits.json* — Contains dataset split info (train / test / val), adjustable via configuration flags.


### Recommended Benchmark Configuration
We provide a recommended subset of indexed classes—those most consistently represented in indoor construction scenes and suitable for stable benchmarking. The remaining classes can be optionally included as **[auxiliary/context categories]** for extended experiments.

```
Indexed (recommended for SIP-Indoor benchmarking):
0: wall, 1: ceiling, 2: floor, 3: pipes, 4: column, 5: ladder, 6: stair 
```

<!-- #### **Non-Indexed** (auxiliary / context only):  
**7: frame, 8: lift, 9: mtrl, 10:window**, 11: guardrails, 12: door, 13: ground, 14: vehicle, 15: tree, 16: fence, 17: scaffolding, 18: portajohn, 19: container, 20: monument, 21: girder, 22: awning -->






## Instructions

### Download: SIP-Indoor 

```bash
wget "https://dl.dropboxusercontent.com/scl/fi/8kgdy1wiz6g1qj7oe79uh/SIP-indoor.zip?rlkey=oue0m4sruc0bkx2p2784tnbu7&st=9raoybx" -O sip-indoor.zip
unzip sip-indoor.zip && rm sip-indoor.zip
cd sip-indoor
```
Or using `curl`:
```bash
curl -L "https://dl.dropboxusercontent.com/scl/fi/8kgdy1wiz6g1qj7oe79uh/SIP-indoor.zip?rlkey=oue0m4sruc0bkx2p2784tnbu7&st=9raoybx" -o sip-indoor.zip
unzip sip-indoor.zip && rm sip-indoor.zip
```

### Download: SIP-Outdoor (extension) 
```bash
wget "https://dl.dropboxusercontent.com/scl/fi/pee418sp18krug56nkc7z/SIP-outdoor.zip?rlkey=ivrd2cwc5ps8z8tpi5mo4pq87&st=jxm0l0wl" -O sip-outdoor.zip
```
<!-- 
### Class Configuration for 3D Benchmark


### Evaluation -->

## Visualization

To visualize annotations, use the `view_anno.py` script. It loads a scan and its class-wise annotations, applies colors from `class_config.json`, and outputs a merged, colorized `.txt` file. This files can be opened directly in 3D tools such as [CloudCompare](https://www.danielgm.net/cc/).

```bash
python view_anno.py sip-indoor/scans/[scan_id] [output_folder]
```
- [scan_id]: folder containing scan.txt and its Annotation/ directory
- [output_folder]: destination for the merged, colorized .txt file  




## License

- **Dataset**: Licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/); **Code**: Licensed under the [MIT License](./LICENSE.md).  

*You are free to share and adapt the dataset for non-commercial purposes with proper attribution.*