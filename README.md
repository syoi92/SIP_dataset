# SIP_dataset
Sites in Pieces: A SIP dataset of disaggregated 3D scans for construction-phase segmentation


## SIP dataset
We introduce SIP dataset

### Key Characteristics
- A unit of individual scans
- Scenes captured during construction through FARO lidar, including structure components and temporary construction objects

### Class List
`Indexed Classes (used for SIP-indoor evaluation):`  
**0: wall, 1: ceiling, 2: floor, 3: pipes, 4: column, 5: ladder, 6: stair** 

`Non-Indexed (auxiliary / context only):`  
**7: frame, 8: lift, 9: mtrl**, 10: guardrails, 11: door, 12: ground, 13: vehicle, 14: tree, 15: fence, 16: scaffolding, 17: portajohn, 18: container, 19: monument, 20: girder, 21: awning, 22: clutter


*Only the bolded classes appear in SIP-Indoor scenes.*


### Structure
```
SIP-Indoor/
  │ class_info.json
  │ splits.json
  └─Scans/
    │ scan.txt [xyzrgbI]
    └─Annotation/
        │ class1.txt [xyzrgbI]
        │ class2.txt
        │ ⋮ 
        └─classN.txt
```


## Download Instructions

SIP-Indoor

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

SIP-Outdoor (extension) 
```
wget [URLURLURL] -O sip-outdoor.zip
```

## 📄 License

This repository contains two types of content with separate licenses:

- 📦 **Dataset**: Licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).  
  You are free to share and adapt the dataset for non-commercial purposes with proper attribution.

- 🧑‍💻 **Code**: Licensed under the [MIT License](./LICENSE.md).