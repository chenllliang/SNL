# SNL编译原理实验

## 词法分析器 Tokenizer.py
*CL*

- program.snl ： 源代码
- program.snl.tmp : 预处理后的代码
- program.snl.tok : 生成的token序列

Tokenizer.py 使用：
```shell
python Tokenizer.py program.snl
```

## 语法分析器
- 使用Tokeniezer.Token 的unserilze方法将字符串恢复成Token对象

### 递归下降法 RecursiveParser.py
*CL*


### 非递归法 
*XWK*

## 语义分析器