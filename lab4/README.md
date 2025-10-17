# hg38_tool.sh 使用说明

该脚本是一个 **FASTA 文件处理工具**，主要针对人类基因组参考序列 `hg38.fa`，提供了文件检查、N 碱基统计、染色体长度计算、子序列提取等功能。

---

## 环境要求
- Linux/Unix 环境，支持Bash
- 系统需有以下常用命令：`grep`, `awk`, `wc`, `head`, `du`, `tr`, `column`, `bc`

将脚本下载并赋予可执行权限：
```bash
chmod +x hg38_tool.sh
```

## 使用方法

```
./hg38_tool.sh -a ACTION [其他参数]
```

参数说明:
  -a ACTION    (必需) 指定功能
      check       : 检查 hg38.fa 文件基本信息
      Ns          : 统计 N 碱基 (全基因组 或 单条染色体)
      NsAll       : 输出所有染色体的 N 碱基数量表格
      length      : 计算某条染色体长度、N 数量和 %Ns
      lengthAll   : 输出所有染色体长度、N 数量和 %Ns 表格
      maxNs       : 找出 %Ns 最高的染色体
      subseq      : 提取子序列

  -c CHROM    指定染色体名称 (如 chr1, chr2)
  -s START    提取子序列起始位置 (1-based)
  -e END      提取子序列终止位置
  -O OUTPUT   输出文件名 (可选, 默认 chrX_start_end.fa)


## 使用示例

### 1.文件检查
```
./hg38_tool.sh -a check
```

输出：
```
File name: hg38.fa
File size: 3.1G
Number of lines: 64186394
First 5 lines:
>chr1
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
```

### 2. 统计 N 碱基
#### 全基因组：
```
./hg38_tool.sh -a Ns
```
输出：
```
Total N bases: 159970322
```

#### 指定染色体：
```
./hg38_tool.sh -a Ns -c chr1
```
输出：
```
Chromosome: chr1
Action: Ns
Result: 18475410
```
#### 所有染色体：
```
./hg38_tool.sh -a NsAll
```
输出：
```
Chromosome      N_count
chrUn_KI270528v1         0
chr20_GL383577v2_alt     0
chr15_GL383555v2_alt     0
…
```

### 3.染色体长度与 %Ns
#### 单条染色体：
```
./hg38_tool.sh -a length -c chr2
```
输出：
```
Chromosome: chr2
Action: length
Total bases: 242193529
N count: 1645301
% Ns: 0.68
```

#### 所有染色体表格：
```
./hg38_tool.sh -a lengthAll
```
输出：
```
Chromosome      Length  N_count %Ns
…
chrX                     156040895  1147866   0.7356
chrY                     57227415   30812372  53.8420
chrY_KI270740v1_random   37240      0         0.0000
```
#### 找出 %Ns 最高的染色体：
```
./hg38_tool.sh -a maxNs
```
输出：
```
Chromosome      Length  N_count %Ns
…
chrX                     156040895  1147866   0.7356
chrY                     57227415   30812372  53.8420
chrY_KI270740v1_random   37240      0         0.0000
Chromosome               with       highest   %Ns:     chrUn_KI270317v1  (90.3847  %)
```

#### 4.提取子序列
```
./hg38_tool.sh -a subseq -c chr3 -s 1000 -e 1100 -O chr3_region.fa
```
输出：
```
First 10 bases:
>chr3:1000-1100
NNNNNNNNNN...
```
生成的 chr3_region.fa 文件内容：
```
>chr3:1000-1100
NNNNNNNNNN……
```

## 注意事项
### 1. 确保 `hg38.fa` 文件存在  
运行脚本前，请确认参考基因组文件 **hg38.fa** 已放置在脚本所在目录，否则脚本会直接报错并退出。

### 2.Invalid Index 报错机制

在使用 `-a subseq` 提取子序列时，脚本会检测输入的区间是否合法：

- 起始位置 (`-s START`) 必须 **≥ 1**  
- 终止位置 (`-e END`) 必须 **大于起始位置**  

否则会报错并退出，例如：
```
./hg38_tool.sh -a subseq -c chr1 -s 200 -e 100
```
