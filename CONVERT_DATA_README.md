# convert_data.py 运行说明

## 一、convert_data.py 会处理哪些数据集

脚本会**按顺序**处理以下 6 类数据（在 `convert_data.py` 里写死）：

- `synthetic_consensus`
- `synthetic_clustering`
- `synthetic_polarization`
- `twitter_BlackLivesMatter`
- `twitter_Abortion`
- `reddit_politics`

任一类型缺输入文件，该类型会报错，但不会影响其他类型（若希望只跑某几类，需要自己改 `datasets` 列表）。

---

## 二、每类数据需要的输入文件

### 1. 合成数据（synthetic_*）

| 数据类型 | 需要的文件 | 说明 |
|----------|------------|------|
| synthetic_consensus | `working/synthetic_consensus.csv` | 三列：user_id, opinion, time，无表头 |
| synthetic_clustering | `working/synthetic_clustering.csv` | 同上 |
| synthetic_polarization | `working/synthetic_polarization.csv` | 同上 |

**当前项目里：**  
- 有：`working/synthetic_interaction_*.csv`（交互数据，不是 convert_data 要的）。  
- **没有**：`working/synthetic_consensus.csv` 等三份「user_id, opinion, time」的 csv。

**如何获取：**  
先跑合成数据生成脚本，会写出上述 csv：

```bash
python simulate.py
```

会生成 `working/synthetic_consensus.csv`、`working/synthetic_clustering.csv`、`working/synthetic_polarization.csv`，然后再运行 `convert_data.py`。

---

### 2. 推特数据（twitter_Abortion / twitter_BlackLivesMatter）

| 数据类型 | 需要的文件 | 说明 |
|----------|------------|------|
| twitter_Abortion | `working/rated_twitter_with_ID/rated_twitter_Abortion_with_ID.tsv` | 人工标注：Sentiment Rating、Rater's ID 等 |
| twitter_Abortion | `working/posts_twitter_Abortion.tsv` | 原始推文：date, user, time, sentence（逗号分隔） |
| twitter_Abortion | `input/profiles_twitter_Abortion.tsv` | 用户档案：user, username, description, followers_count 等 |
| twitter_BlackLivesMatter | 同上结构，把 `twitter_Abortion` 换成 `twitter_BlackLivesMatter` | 同上 |

**当前项目里：**  
- **没有**：`working/rated_twitter_with_ID/` 目录及其中任何 `rated_*_with_ID.tsv`。  
- **没有**：`working/posts_twitter_Abortion.tsv`（只有 `posts_final_*`，是 convert_data 的**输出**，不是输入）。  
- **没有**：`input/profiles_twitter_Abortion.tsv`（只有 `input/hyperparameters_*.json`）。

**如何获取：**

1. **原始推文 + 用户档案（可选）**  
   - 用 Twitter API 爬推文：运行 `collect_twitter.py`，会按时间分段保存到 `input/twitter_Abortion_*.csv`。  
   - 需要再有人或脚本把这些合并/整理成 **`working/posts_twitter_Abortion.tsv`**（列：date, user, time, sentence，逗号分隔）。  
   - 用户档案：运行 `collect_twitter_user.py`（需先有 `working/posts_twitter_Abortion.tsv` 里的 user 列表），会生成 **`input/profiles_twitter_Abortion.tsv`**。

2. **人工标注文件（必须且无法自动生成）**  
   - **`working/rated_twitter_with_ID/rated_twitter_Abortion_with_ID.tsv`** 是论文作者方做的**情感/立场标注**（每条推文对应 Sentiment Rating、Rater's ID）。  
   - 仓库**未提供**该标注数据（隐私/版权原因）。  
   - 若你要“从零”复现 Twitter 实验，只能：  
     - 自己标注一部分推文，并做成与代码中一致的格式（含 Rater’s ID 等），或  
     - 联系论文作者询问是否可提供或购买标注数据。

因此：**在未拿到或自行制作 `rated_*_with_ID.tsv` 和对应 `posts_*.tsv` 前，无法通过 convert_data.py 重新生成 twitter_Abortion / twitter_BlackLivesMatter 的 `posts_final_*`。**

---

### 3. Reddit 数据（reddit_politics）

| 数据类型 | 需要的文件 | 说明 |
|----------|------------|------|
| reddit_politics | `working/posts_reddit_politics.tsv` | 列需含：date, user, time, sentence, opinion |

**当前项目里：**  
- **没有**：`working/posts_reddit_politics.tsv`。

**如何获取：**  
用仓库的 `collect_reddit.py` 等脚本采集 Reddit 数据，并整理成上述格式后放到 `working/`。

---

## 三、当前文件夹里“已有”和“缺失”汇总

| 数据类型 | 需要的输入 | 项目里是否有 |
|----------|------------|--------------|
| synthetic_* | `working/synthetic_consensus.csv` 等 3 个 csv | ❌ 无（需先运行 `simulate.py`） |
| twitter_Abortion | `working/rated_twitter_with_ID/rated_twitter_Abortion_with_ID.tsv` | ❌ 无 |
| twitter_Abortion | `working/posts_twitter_Abortion.tsv` | ❌ 无 |
| twitter_Abortion | `input/profiles_twitter_Abortion.tsv` | ❌ 无 |
| twitter_BlackLivesMatter | 同上，名称改为 BlackLivesMatter | ❌ 无 |
| reddit_politics | `working/posts_reddit_politics.tsv` | ❌ 无 |

你当前已有的 **`working/posts_final_sample_twitter_Abortion.tsv`** 和 **`working/initial_sample_twitter_Abortion.txt`** 是**之前某次运行 convert_data 或仓库自带的输出结果**，不是 convert_data 的输入；convert_data 不会读 `posts_final_*` 或 `initial_*`。

---

## 四、若只想“能跑通”convert_data.py（不关心 Twitter/Reddit）

只生成并转换合成数据即可：

1. 生成合成数据：
   ```bash
   python simulate.py
   ```
2. 再运行转换（仍会尝试处理 Twitter/Reddit 并报错，除非你改代码只保留 synthetic）：
   ```bash
   python convert_data.py
   ```

若希望**只处理 synthetic**，避免因缺少 Twitter/Reddit 文件而报错，需要修改 `convert_data.py` 顶部的 `datasets` 列表，只保留三个 synthetic 名称，例如：

```python
datasets = ["synthetic_consensus", "synthetic_clustering", "synthetic_polarization"]
```

---

## 五、总结

- **运行 convert_data.py 需要什么文件？**  
  - Synthetic：`working/synthetic_consensus.csv`、`synthetic_clustering.csv`、`synthetic_polarization.csv`。  
  - Twitter：`working/rated_twitter_with_ID/rated_*_with_ID.tsv`、`working/posts_*_twitter_*.tsv`、`input/profiles_*_twitter_*.tsv`。  
  - Reddit：`working/posts_reddit_politics.tsv`。

- **当前文件夹里有吗？**  
  - 上述输入文件在项目里**都没有**（只有 synthetic 的 interaction csv 和 final/initial 等**输出**）。

- **缺失数据怎么获取？**  
  - **Synthetic**：运行 `python simulate.py` 即可。  
  - **Twitter**：原始推文和用户档案可通过 `collect_twitter.py`、`collect_twitter_user.py` 及后续整理得到；**标注文件 `rated_*_with_ID.tsv` 需自行标注或向作者获取**。  
  - **Reddit**：通过 `collect_reddit.py` 等采集并整理成指定格式。

你已有 `posts_final_sample_twitter_Abortion.tsv` 时，**无需再跑 convert_data** 就能用 `main_sinn.py --dataset sample_twitter_Abortion` 做实验；只有在你需要“从原始推文重新生成 posts_final”时，才必须凑齐上述 Twitter 输入并运行 convert_data。
