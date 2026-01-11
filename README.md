# Useful Manual Data Annotation
## Prerequisites

首先运行，
```
git clone git@github.com:ChuAn7One/Useful-Manual-Data-Annotation.git
```

下载仓库后，应当在标注前安装相关依赖，可在终端内运行：

```
pip install natsort
pip install argparse
pip install opencv-python
```

## Guide
在运行前，需要熟悉一下文件的架构，总文件示例架构如下：

```
.
├── group_01
├── group_02
├── group_03
├── group_04
├── auto_annotation.py
├── metas_create.py
└── README.md
```

其中，
```
├── group_01 # 数据
├── group_02
├── group_03
├── group_04
```
为数据集，替换成个人数据即可。

而下述文件树，
```
├── auto_annotation.py # 主脚本
├── metas_create.py # 编写的python模块
└── README.md # 使用说明
```
为主脚本，必要模块和使用说明。

## Directly Run

安装了依赖且了解了使用方法后，可直接运行，
```
python3 auto_annotation.py --dataset_path ./group_**/ --start *
```
或
```
python auto_annotation.py --dataset_path ./group_**/ --start *
```

其中，
`--dataset_path`代表数据集路径，每次只能输入一个文件夹；`--start`代表从第`*`张开始标注，这里的`*`是以`1`起始的正整数，而非数组索引计数。

### Example
```
python3 auto_annotation.py --dataset_path ./group_01/ --start 1
```
上述代码块代表，在`group_01`文件夹下创建`Metas.json`，从第`1`张图片开始标注，所以**标注完成时，一定要记住标注到哪一张，避免之后标注时仍然从第一张开始（默认从第一张开始标注）**。

### Note
``
--start
``
默认值为`1`，故建议按照**Directly Run**中的方式运行。

``
├── group_**
``
数据集中最好不创建**Metas.json**，脚本可自动创建。
