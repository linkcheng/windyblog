# Pandas 笔记

1. 使用模块

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

2. Numpy

   * ndarray 一个具有矢量算术运算和复杂广播能力的快速且节省空间的多维数组

   ```python
   data=np.array([[0.9526, -0.246, -0.8856],
        [0.5639, 0.2379, 0.9104]], dtype=np.float64)
   ```

   data

   ```
   array([[ 0.9526, -0.246 , -0.8856],
          [ 0.5639,  0.2379,  0.9104]])
   ```

   data.shape

   ```
   (2, 3)
   ```

   data.dtype

   ```
   dtype('float64')
   ```

   ```python
   np.zeros((3, 2))  # 返回全零数组
   np.ones(5)  # 全一数组
   np.empty((2, 3, 2))  # 创建一个没有具体值得数组
   np.arange(10)  # Python 内置函数 range 的数组版，返回 ndarray 类型
   np.asarray()  # 将输入装换为 ndarray，如果输入本身就是一个 ndarray 就不进行复制
   arr.astype(np.float64) # arr = np.array(range(10)), 将 arr 整型转换为浮点型；
   # 调用 astype 无论如何都会创建出一个新的数组(原始数组的一份拷贝)，即使 dtype 跟老数组移植
   ```

   ```
   array([[ 0.,  0.],
          [ 0.,  0.],
          [ 0.,  0.]])

   array([ 1.,  1.,  1.,  1.,  1.])

   array([[[ -0.00000000e+000,   3.11108119e+231],
           [  2.18497312e-314,   2.18500092e-314],
           [  2.18500073e-314,   2.18500067e-314]],

          [[  2.18500079e-314,   2.18500070e-314],
           [  2.18500076e-314,   2.18500051e-314],
           [  2.18500084e-314,   8.34404882e-309]]])
   array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
   ```

   * Numpy 数据类型

   int8 uint8: i1 u1 ：8 位整型

   int16 int32 int64  uint16 uint32 uint64: i2 i4 i8  u2 u4 u8

   float16: f2 ：半精度浮点数

   float32  float64 float128：f4(f) f8(d) f16(g)

   complex64 complex128 complex256: c8 c16 c32 ：分别用 32 位、64 位或 128 位浮点数表示的复数

   bool：？：存储 True 和 False 的布尔类型

   object：O ：Python 对象类型

   string_:  S : 固定长度的字符串类型，每个字符一个字节，长度为 10 的字符集，应使用 S10

   unicode_ : U : 固定长度的 unicode 类型，字节由平台决定，U10 等

   * 大小相等的数组之间的任何算术运算都会将运算应用到元素级；数组与标量的算术运算也会将那个标量值传播到各个元素；不同大小的数组之间的运算叫做广播。

   ​