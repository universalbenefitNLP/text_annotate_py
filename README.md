# 文本复原

## 背景

语言表达中会出现特定构造词，可能跟已有词语含义一致，但因为使用频率极少，会降低读者的情绪感知与内容理解能力——[参考资料](https://finance.ifeng.com/news/special/beiyoucai3_1/index.shtml)。这种现象通常出现在事件调查报告、媒体公关或某些特定领域。

本项目通过添加注释的方式，帮助读者理解原有含义。

> e.g 中方跟美方就韩春雨团队\[非主观造假\]\(造假\)事件\[充分交换了意见\]\(双方无法达成协议，吵得厉害\)



## 依赖包


> pip install -r requirements.txt



## 使用说明

匹配词与原意词位于```./data/synonym```文档中，根据```匹配词:::原意词```的形式更新保存。

初次使用或者更新```synonym```文档后，运行构建程序。

> python ./annotate/ac_build.py

启动 rest api 接口服务

> python run.py



调用rest api 接口

```python
from requests import put, get

put('http://localhost:5000/annotation', data={'text': '中方跟美方就韩春雨团队非主观造假事件充分交换了意见'}).json()

{'annotated': '中方跟美方就韩春雨团队[非主观造假](造假)事件[充分交换了意见](双方无法达成协议，吵得厉害)'}
```



## 规划

- [ ] 语料充分后会增加文本分类预处理
- [ ] 构建匹配词与原意词的对应数据集



如果想补充语料，可登陆[问卷](https://wj.qq.com/s2/5170542/a685)进行提交



# Text Restoration

## Introduction

```Decay language is designed to make lies sound truthful and murder respectable, and to give an appearance of solidity to pure wind. ```see [Politics and the English Language](https://en.wikipedia.org/wiki/Politics_and_the_English_Language).

To recover decay language, this project append annotations after them, which can help readers better understand original meaning.



## Requirements

> pip install -r requirements.txt



## Usage

Pattern word and origin word is located in ```./data/synonym```

The first time you run this program or every time you update ```synonym```, run build function.

> python ./annotate/ac_build.py

Start rest api by

>  python run.py

Use rest api by

```python
from requests import put, get

put('http://localhost:5000/annotation', data={'text': '中方跟美方就韩春雨团队非主观造假事件充分交换了意见'}).json()

{'annotated': '中方跟美方就韩春雨团队[非主观造假](造假)事件[充分交换了意见](双方无法达成协议，吵得厉害)'}
```



## To do list

- [ ] Add text classification preprocessing after enouge corpus is acquired
- [ ] Construct pattern word and origin word corpus

