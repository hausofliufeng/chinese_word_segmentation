# chinese_word_segmentation
一些中文分词算法实现，NLP课的课后实践。

## 1 Model

### 1.1 RMM

```bash
python RMM.py 待分词文件 输出文件 词表
```

### 1.2 CRF

#### 1.2.1 模型训练

- 数据准备

  运行命令将数据转换为BMES格式

  ```bash
  python utils\sentence2crf.py -i data\training.txt -o data\training_crf.txt  -m 1
  ```

  ![image-20210422234908572](imgs/README/image-20210422234908572.png)

#### 1.2.2 预测

- 待分词文件转换格式

  ```bash
  python utils\sentence2crf.py -i data\test_combined.txt -o data\test_crf.txt  -m 2
  ```

  ![image-20210423002624118](imgs/README/image-20210423002624118.png)

- 进行预测

  ```bash
  crf_test -m model_file test_file>result_file
  ```

- 根据标签组合句子

  ```
  python utils\crf2sentence.py output\crf_raw.txt output\crf.txt
  ```

  ![image-20210423004141950](imgs/README/image-20210423004141950.png)

## 2 模型评价

```bash
perl scripts/score 词表 标准答案 分词预测>score.txt
```

## 3 踩过的坑

- 用perl命令进行打分前，记得核对下`答案.txt`和`预测值.txt`的句子总数是否相同，如果中间少预测一个句子，就会导致对不上，严重影响打分！