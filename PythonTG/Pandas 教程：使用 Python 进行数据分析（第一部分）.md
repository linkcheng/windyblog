## Pandas 教程：使用 Python 进行数据分析（第一部分）

Python 是进行数据分析的绝佳语言，主要原因是以数据为中心的 Python 包的奇妙的生态系统。 Pandas 就是其中之一，它使得导入和分析数据更容易。 Pandas 以 [NumPy](http://www.numpy.org/) 和 [matplotlib](http://matplotlib.org/) 包为底层驱动，为您提供更方便的接口用来完成大多数数据分析和可视化工作。

在这篇教程中，我们将使用 Pandas 来分析 [IGN](https://www.kaggle.com/egrinstein)（一个热门的视频游戏评论网站）的视频游戏评论数据。 数据收集在 [Eric Grinstein](https://www.kaggle.com/egrinstein) ，可以在[这里](https://www.kaggle.com/egrinstein/20-years-of-games)找到。 在我们分析视频游戏评论的过程，将学习 Pandas 关键的概念，例如索引等。

![1](https://www.dataquest.io/blog/images/pandas/witcher.jpg)

######  像 “巫师 3” 这样的游戏在 PS4 上会比在 Xbox One 上获得更好的评价吗？ 这个数据集可以帮助我们找出答案。



首先做一下声明，以下我们将使用 [Python 3.5](https://www.python.org/downloads/release/python-350/) 和 [Jupyter Notebook](http://jupyter.org/) 来做我们的分析。

> 译者注：brew install python3; pip3 install jupyter; pip3 install pandas  (MacOS)。[jupyter教程](http://codingpy.com/article/getting-started-with-jupyter-notebook-part-1/)

### 使用 pandas 导入数据

我们将采取的第一步是读取数据。数据存储为用[逗号分隔](https://en.wikipedia.org/wiki/Comma-separated_values)类型的文件，如 csv 文件，它们一行代表一条记录，列与列之间用逗号（`，`）分开 。 下面是 `ign.csv` 文件的前几行：

```csv
,score_phrase,title,url,platform,score,genre,editors_choice,release_year,release_month,release_day
0,Amazing,LittleBigPlanet PS Vita,/games/littlebigplanet-vita/vita-98907,PlayStation Vita,9.0,Platformer,Y,2012,9,12
1,Amazing,LittleBigPlanet PS Vita -- Marvel Super Hero Edition,/games/littlebigplanet-ps-vita-marvel-super-hero-edition/vita-20027059,PlayStation Vita,9.0,Platformer,Y,2012,9,12
2,Great,Splice: Tree of Life,/games/splice/ipad-141070,iPad,8.5,Puzzle,N,2012,9,12
3,Great,NHL 13,/games/nhl-13/xbox-360-128182,Xbox 360,8.5,Sports,N,2012,9,11
```

如上所示，数据中的每一行代表一个由 IGN 审查的游戏。 列包含有关该游戏的信息：

* score_phrase - IGN 用一个词描述该游戏。 这与得到的分数相关联。
* title - 游戏的名称。
* url - 可以在其中查看完整评价的网址。
* platform - 游戏评论的平台（PC，PS4等）。
* score - 游戏的分数，从1.0到10.0。
* genre - 游戏的流派。
* editors_choice - `N` 代表游戏不是编辑的选择，`Y` 代表是。 这与得分相关。
* release_year - 游戏发布的年份。
* release_month - 游戏发布的月份。
* release_day - 游戏发布的天。

还有一个包含行索引值的引导列。 现在我们可以忽略此列，但随后我们将深入索引值的意义。 为了能够使用 Python中 的数据，我们需要将 csv 文件读入 [Pandas DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html)。 DataFrame （数据帧）是一种表示和处理表格数据的方法。 表格数据具有行和列，就像我们的 csv 文件一样。

为了读入数据，我们需要使用 pandas.read_csv 函数。 此函数将接收一个 csv 文件并返回一个 DataFrame。 下面的代码将：

* 导入 `pandas` 库。 我们将它重命名为 `pd`，这样后续写起来更方便。
* 把 `ign.csv` 文件内容读到 DataFrame 中，并将它起名字叫 `review`。

```python
import pandas as pd 
reviews = pd.read_csv("ign.csv")
```

一旦我们把数据读入到 DataFrame 中，Pandas 提供两个方法让我们快速打印出数据。 这两个函数是：

* [pandas.DataFrame.head](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.head.html) - 打印 DataFrame 的第 N 行。 默认值 5。
* [pandas.DataFrame.tail](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.tail.html) - 打印 DataFrame 的最后 N 行。 默认值 5。

我们用 `head` 方法看下 `review` 中到底是些什么：

```python
reviews.head()
```

|       | Unnamed: 0 | score_phrase | title                                    | url                                      | platform         | score | genre      | editors_choice | release_year | release_month | release_day |
| ----- | :--------- | ------------ | ---------------------------------------- | ---------------------------------------- | ---------------- | ----- | ---------- | -------------- | ------------ | ------------- | ----------- |
| **0** | 0          | Amazing      | LittleBigPlanet PS Vita                  | /games/littlebigplanet-vita/vita-98907   | PlayStation Vita | 9.0   | Platformer | Y              | 2012         | 9             | 12          |
| **1** | 1          | Amazing      | LittleBigPlanet PS Vita -- Marvel Super Hero E... | /games/littlebigplanet-ps-vita-marvel-super-he... | PlayStation Vita | 9.0   | Platformer | Y              | 2012         | 9             | 12          |
| **2** | 2          | Great        | Splice: Tree of Life                     | /games/splice/ipad-141070                | iPad             | 8.5   | Puzzle     | N              | 2012         | 9             | 12          |
| **3** | 3          | Great        | NHL 13                                   | /games/nhl-13/xbox-360-128182            | Xbox 360         | 8.5   | Sports     | N              | 2012         | 9             | 11          |
| **4** | 4          | Great        | NHL 13                                   | /games/nhl-13/ps3-128181                 | PlayStation 3    | 8.5   | Sports     | N              | 2012         | 9             | 11          |

我们还可以通过 [pandas.DataFrame.shape](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.shape.html) 属性查看 `reviews` 有多少行列：

```python
reviews.shape
```

```
(18625,11)
```

如上所示，一切都已正确读取，我们有 18625 行 11 列。

在 Pandas vs NumPy 中，Pandas 的一个很大的优点是允许你有不同数据类型的列。 `reviews` 具有 float 类型的列，如 `score`，string 类型，如 `score_phrase`和 integer 类型，如 release_year。

现在我们已经正确读取了数据，让我们从 `reviews` 中检索我们想要的行和列。

### 使用 Pandas 进行 DataFrame（数据帧）检索

之前，我们使用 `head` 方法打印前 `5` 行的 `reviews`。 我们可以使用 [pandas.DataFrame.iloc](http://pandas.pydata.org/pandas-docs/version/0.17.0/generated/pandas.DataFrame.iloc.html) 方法完成同样的事情。 `iloc` 方法允许我们按位置检索行和列。 为了做到这一点，我们需要指定我们想要的行的位置，以及我们想要的列的位置。

以下代码与 `reviews.head(5)` 效果相同：

```python
reviews.iloc[0:5,:]
```

|       | Unnamed: 0 | score_phrase | title                                    | url                                      | platform         | score | genre      | editors_choice | release_year | release_month | release_day |
| ----- | :--------- | ------------ | ---------------------------------------- | ---------------------------------------- | ---------------- | ----- | ---------- | -------------- | ------------ | ------------- | ----------- |
| **0** | 0          | Amazing      | LittleBigPlanet PS Vita                  | /games/littlebigplanet-vita/vita-98907   | PlayStation Vita | 9.0   | Platformer | Y              | 2012         | 9             | 12          |
| **1** | 1          | Amazing      | LittleBigPlanet PS Vita -- Marvel Super Hero E... | /games/littlebigplanet-ps-vita-marvel-super-he... | PlayStation Vita | 9.0   | Platformer | Y              | 2012         | 9             | 12          |
| **2** | 2          | Great        | Splice: Tree of Life                     | /games/splice/ipad-141070                | iPad             | 8.5   | Puzzle     | N              | 2012         | 9             | 12          |
| **3** | 3          | Great        | NHL 13                                   | /games/nhl-13/xbox-360-128182            | Xbox 360         | 8.5   | Sports     | N              | 2012         | 9             | 11          |
| **4** | 4          | Great        | NHL 13                                   | /games/nhl-13/ps3-128181                 | PlayStation 3    | 8.5   | Sports     | N              | 2012         | 9             | 11          |

正如你看到的那样，我们指定了我们想要的行 `0:5`。 这意味着我们取 0 到 5 行的数据，但不包括第 5 行。第一行被认为是在位置 0。这时我们获取了第 `0,1,2,3` 和 `4` 行的数据。

如果我们缺失第一个位置的值，如`：5`，这个地方的默认值就是 0 。如果我们缺失最后一个位置额值，如 `0 :`，它默认到 DataFrame 中的最后一行或列。

我们想要所有的列，所以我们只指定一个冒号（:)，没有任何位置。 这给了我们从0到最后一列的列。

以下是一些关于索引使用的例子，以及对结果的解释：

* `reviews.iloc[:5,:]` – 前 `5` 行, 及其全部列数据。

- `reviews.iloc[:,:]` – 所有行所有列的数据。
- `reviews.iloc[5:,5:]` – 从第  `5` 行开始到最后一行, 及第  `5` 列开始到最后一列的数据。
- `reviews.iloc[:,0]` – 所有行的第一列数据。
- `reviews.iloc[9,:]` – 第十行的所有列数据。

这种使用索引的方法与 [NumPy](http://www.numpy.org/) 的索引用起来很类似。如果你想详细了解，点击[这里](http://www.dataquest.io/blog/numpy-tutorial-python/)可以获取更多关于 Numpy 的教程。

现在我们知道了怎么通过位置来检索数据，那么让我们除去无用的第一列信息。

```python
reviews = reviews.iloc[:,1:]
reviews.head()
```

| score_phrase | title   | url                                      | platform                                 | score            | genre | editors_choice | release_year | release_month | release_day |      |
| ------------ | ------- | ---------------------------------------- | ---------------------------------------- | ---------------- | ----- | -------------- | ------------ | ------------- | ----------- | ---- |
| **0**        | Amazing | LittleBigPlanet PS Vita                  | /games/littlebigplanet-vita/vita-98907   | PlayStation Vita | 9.0   | Platformer     | Y            | 2012          | 9           | 12   |
| **1**        | Amazing | LittleBigPlanet PS Vita -- Marvel Super Hero E... | /games/littlebigplanet-ps-vita-marvel-super-he... | PlayStation Vita | 9.0   | Platformer     | Y            | 2012          | 9           | 12   |
| **2**        | Great   | Splice: Tree of Life                     | /games/splice/ipad-141070                | iPad             | 8.5   | Puzzle         | N            | 2012          | 9           | 12   |
| **3**        | Great   | NHL 13                                   | /games/nhl-13/xbox-360-128182            | Xbox 360         | 8.5   | Sports         | N            | 2012          | 9           | 11   |
| **4**        | Great   | NHL 13                                   | /games/nhl-13/ps3-128181                 | PlayStation 3    | 8.5   | Sports         | N            | 2012          | 9           | 11   |

### 使用 Pandas 中的标签检索

现在我们知道如何按位置检索行和列，而通过标签检索行和列是另一种值得研究的使用数据帧的方式。

Pandas 比 NumPy 的主要优点是每一列和行都有一个标签。 尽管使用列位置也可以做一些操作，但却很难跟踪哪个数字对应于哪个列。

我们可以使用 [pandas.DataFrame.loc](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.loc.html) 方法处理标签，它允许我们使用标签而不是位置进行索引。

我们可以使用 `loc` 方法显示前五行 `reviews`，如下所示：

```python
reviews.loc[0:5,:]
```

|       | score_phrase | title                                    | url                                      | platform         | score | genre      | editors_choice | release_year | release_month | release_day |
| ----- | ------------ | ---------------------------------------- | ---------------------------------------- | ---------------- | ----- | ---------- | -------------- | ------------ | ------------- | ----------- |
| **0** | Amazing      | LittleBigPlanet PS Vita                  | /games/littlebigplanet-vita/vita-98907   | PlayStation Vita | 9.0   | Platformer | Y              | 2012         | 9             | 12          |
| **1** | Amazing      | LittleBigPlanet PS Vita -- Marvel Super Hero E... | /games/littlebigplanet-ps-vita-marvel-super-he... | PlayStation Vita | 9.0   | Platformer | Y              | 2012         | 9             | 12          |
| **2** | Great        | Splice: Tree of Life                     | /games/splice/ipad-141070                | iPad             | 8.5   | Puzzle     | N              | 2012         | 9             | 12          |
| **3** | Great        | NHL 13                                   | /games/nhl-13/xbox-360-128182            | Xbox 360         | 8.5   | Sports     | N              | 2012         | 9             | 11          |
| **4** | Great        | NHL 13                                   | /games/nhl-13/ps3-128181                 | PlayStation 3    | 8.5   | Sports     | N              | 2012         | 9             | 11          |
| **5** | Good         | Total War Battles: Shogun                | /games/total-war-battles-shogun/mac-142565 | Macintosh        | 7.0   | Strategy   | N              | 2012         | 9             | 11          |

以上结果与 `reviews.iloc[0:5,:]` 的结果并没有太大不同。这是因为行标签可以使用任意类型的值，使得行标签是准确匹配位置。你可以在上面的表格的左侧看到行标签(加粗部分)。当然也可以通过访问数据帧的 [index](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) 属性，以下将会展示 `reviews` 的行索引属性：

```python
reviews.index
```

```
Int64Index([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, ...], dtype='int64')
```

不过索引并不总是与位置匹配。 在下面的代码块中，我们将：

* 获取第 `10`行到第 `20` 行的 `reviews`，并且赋值给 `some_reviews`。
* 展示 `some_reviews` 的前 `5` 行内容。

```python
some_reviews = reviews.iloc[10:20,]
some_reviews.head()
```

| score_phrase | title   | url                     | platform                                 | score         | genre | editors_choice    | release_year | release_month | release_day |      |
| ------------ | ------- | ----------------------- | ---------------------------------------- | ------------- | ----- | ----------------- | ------------ | ------------- | ----------- | ---- |
| **10**       | Good    | Tekken Tag Tournament 2 | /games/tekken-tag-tournament-2/ps3-124584 | PlayStation 3 | 7.5   | Fighting          | N            | 2012          | 9           | 11   |
| **11**       | Good    | Tekken Tag Tournament 2 | /games/tekken-tag-tournament-2/xbox-360-124581 | Xbox 360      | 7.5   | Fighting          | N            | 2012          | 9           | 11   |
| **12**       | Good    | Wild Blood              | /games/wild-blood/iphone-139363          | iPhone        | 7.0   | NaN               | N            | 2012          | 9           | 10   |
| **13**       | Amazing | Mark of the Ninja       | /games/mark-of-the-ninja-135615/xbox-360-129276 | Xbox 360      | 9.0   | Action, Adventure | Y            | 2012          | 9           | 7    |
| **14**       | Amazing | Mark of the Ninja       | /games/mark-of-the-ninja-135615/pc-143761 | PC            | 9.0   | Action, Adventure | Y            | 2012          | 9           | 7    |

如上所示，`some_reviews` 的索引是从 `10` 到 `20`。这样以来，尝试给`loc`出入小于 `10` 或者大于  `20` 的值时，就会有以下错误：

```python
some_reviews.loc[9:21,:]
```

```python
---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
<ipython-input-76-5378b774c9a7> in <module>()
----> 1 some_reviews.loc[9:21,:]

/Users/vik/python_envs/dsserver/lib/python3.4/site-packages/pandas/core/indexing.py in __getitem__(self, key)
   1198     def __getitem__(self, key):
   1199         if type(key) is tuple:
-> 1200             return self._getitem_tuple(key)
   1201         else:
   1202             return self._getitem_axis(key, axis=0)

/Users/vik/python_envs/dsserver/lib/python3.4/site-packages/pandas/core/indexing.py in _getitem_tuple(self, tup)
    702 
    703         # no multi-index, so validate all of the indexers
--> 704         self._has_valid_tuple(tup)
    705 
    706         # ugly hack for GH #836

/Users/vik/python_envs/dsserver/lib/python3.4/site-packages/pandas/core/indexing.py in _has_valid_tuple(self, key)
    129             if i >= self.obj.ndim:
    130                 raise IndexingError('Too many indexers')
--> 131             if not self._has_valid_type(k, i):
    132                 raise ValueError("Location based indexing can only have [%s] "
    133                                  "types" % self._valid_types)

/Users/vik/python_envs/dsserver/lib/python3.4/site-packages/pandas/core/indexing.py in _has_valid_type(self, key, axis)
   1258                         raise KeyError(
   1259                             "start bound [%s] is not the [%s]" %
-> 1260                             (key.start, self.obj._get_axis_name(axis))
   1261                         )
   1262                 if key.stop is not None:

KeyError: 'start bound [9] is not the [index]'
```

> 译者注：在本地运行 some_reviews.loc[9:21,:] 时并不报错，而是以下信息，这可能与版本有关。

| score_phrase | title    | url                             | platform                                 | score         | genre | editors_choice    | release_year | release_month | release_day |      |
| ------------ | -------- | ------------------------------- | ---------------------------------------- | ------------- | ----- | ----------------- | ------------ | ------------- | ----------- | ---- |
| **10**       | Good     | Tekken Tag Tournament 2         | /games/tekken-tag-tournament-2/ps3-124584 | PlayStation 3 | 7.5   | Fighting          | N            | 2012          | 9           | 11   |
| **11**       | Good     | Tekken Tag Tournament 2         | /games/tekken-tag-tournament-2/xbox-360-124581 | Xbox 360      | 7.5   | Fighting          | N            | 2012          | 9           | 11   |
| **12**       | Good     | Wild Blood                      | /games/wild-blood/iphone-139363          | iPhone        | 7.0   | NaN               | N            | 2012          | 9           | 10   |
| **13**       | Amazing  | Mark of the Ninja               | /games/mark-of-the-ninja-135615/xbox-360-129276 | Xbox 360      | 9.0   | Action, Adventure | Y            | 2012          | 9           | 7    |
| **14**       | Amazing  | Mark of the Ninja               | /games/mark-of-the-ninja-135615/pc-143761 | PC            | 9.0   | Action, Adventure | Y            | 2012          | 9           | 7    |
| **15**       | Okay     | Home: A Unique Horror Adventure | /games/home-a-unique-horror-adventure/mac-2001... | Macintosh     | 6.5   | Adventure         | N            | 2012          | 9           | 6    |
| **16**       | Okay     | Home: A Unique Horror Adventure | /games/home-a-unique-horror-adventure/pc-137135 | PC            | 6.5   | Adventure         | N            | 2012          | 9           | 6    |
| **17**       | Great    | Avengers Initiative             | /games/avengers-initiative/iphone-141579 | iPhone        | 8.0   | Action            | N            | 2012          | 9           | 5    |
| **18**       | Mediocre | Way of the Samurai 4            | /games/way-of-the-samurai-4/ps3-23516    | PlayStation 3 | 5.5   | Action, Adventure | N            | 2012          | 9           | 3    |
| **19**       | Good     | JoJo's Bizarre Adventure HD     | /games/jojos-bizarre-adventure/xbox-360-137717 | Xbox 360      | 7.0   | Fighting          | N            | 2012          | 9           | 3    |
| **20**       | Good     | JoJo's Bizarre Adventure HD     | /games/jojos-bizarre-adventure/ps3-137896 | PlayStation 3 | 7.0   | Fighting          | N            | 2012          | 9           | 3    |

正如我们前面提到的，处理数据时，使用列标签操作起来更方便。 我们可以在 `loc` 方法中指定列标签，按标签名检索列而不是按位置检索列。

```	
reviews.loc[:5, "score"]
```

```
0    9.0
1    9.0
2    8.5
3    8.5
4    8.5
5    7.0
Name: score, dtype: float64
```

我们也可以通过列表的方式一次列举多列数据。

```
reviews.loc[:5, ["score", "release_year"]]
```

| score | release_year |      |
| ----- | ------------ | ---- |
| 0     | 9.0          | 2012 |
| 1     | 9.0          | 2012 |
| 2     | 8.5          | 2012 |
| 3     | 8.5          | 2012 |
| 4     | 8.5          | 2012 |
| 5     | 7.0          | 2012 |

### Pandas Series（序列）对象

我们可以通过 Pandas 不同方法来检索一个单个列。到目前为止，我们已经两种类型的语法：

* `reviews.iloc[:,1]` - 检索第二列
* `reviews.loc[:," core_phrase"]` - 同样也是第二列

还有第三种，甚至更容易的方式检索整个列。 我们可以在方括号中指定列名，就像字典一样：

```
reviews["score"]
```

```
0         9.0
1         9.0
2         8.5
3         8.5
4         8.5
5         7.0
6         3.0
7         9.0
8         3.0
9         7.0
10        7.5
11        7.5
12        7.0
13        9.0
14        9.0
15        6.5
16        6.5
17        8.0
18        5.5
19        7.0
20        7.0
21        7.5
22        7.5
23        7.5
24        9.0
25        7.0
26        9.0
27        7.5
28        8.0
29        6.5
         ... 
18595     4.4
18596     6.5
18597     4.9
18598     6.8
18599     7.0
18600     7.4
18601     7.4
18602     7.4
18603     7.8
18604     8.6
18605     6.0
18606     6.4
18607     7.0
18608     5.4
18609     8.0
18610     6.0
18611     5.8
18612     7.8
18613     8.0
18614     9.2
18615     9.2
18616     7.5
18617     8.4
18618     9.1
18619     7.9
18620     7.6
18621     9.0
18622     5.8
18623    10.0
18624    10.0
Name: score, dtype: float64		
```

我们依然可以使用列表的方式：

``` 
reviews[["score", "release_year"]]
```

| score | release_year |      |
| ----- | ------------ | ---- |
| 0     | 9.0          | 2012 |
| 1     | 9.0          | 2012 |
| 2     | 8.5          | 2012 |
| 3     | 8.5          | 2012 |
| 4     | 8.5          | 2012 |
| 5     | 7.0          | 2012 |
| 6     | 3.0          | 2012 |
| 7     | 9.0          | 2012 |
| 8     | 3.0          | 2012 |
| 9     | 7.0          | 2012 |
| 10    | 7.5          | 2012 |
| 11    | 7.5          | 2012 |
| 12    | 7.0          | 2012 |
| 13    | 9.0          | 2012 |
| 14    | 9.0          | 2012 |
| 15    | 6.5          | 2012 |
| 16    | 6.5          | 2012 |
| 17    | 8.0          | 2012 |
| 18    | 5.5          | 2012 |
| 19    | 7.0          | 2012 |
| 20    | 7.0          | 2012 |
| 21    | 7.5          | 2012 |
| 22    | 7.5          | 2012 |
| 23    | 7.5          | 2012 |
| 24    | 9.0          | 2012 |
| 25    | 7.0          | 2012 |
| 26    | 9.0          | 2012 |
| 27    | 7.5          | 2012 |
| 28    | 8.0          | 2012 |
| 29    | 6.5          | 2012 |
| ...   | ...          | ...  |
| 18595 | 4.4          | 2016 |
| 18596 | 6.5          | 2016 |
| 18597 | 4.9          | 2016 |
| 18598 | 6.8          | 2016 |
| 18599 | 7.0          | 2016 |
| 18600 | 7.4          | 2016 |
| 18601 | 7.4          | 2016 |
| 18602 | 7.4          | 2016 |
| 18603 | 7.8          | 2016 |
| 18604 | 8.6          | 2016 |
| 18605 | 6.0          | 2016 |
| 18606 | 6.4          | 2016 |
| 18607 | 7.0          | 2016 |
| 18608 | 5.4          | 2016 |
| 18609 | 8.0          | 2016 |
| 18610 | 6.0          | 2016 |
| 18611 | 5.8          | 2016 |
| 18612 | 7.8          | 2016 |
| 18613 | 8.0          | 2016 |
| 18614 | 9.2          | 2016 |
| 18615 | 9.2          | 2016 |
| 18616 | 7.5          | 2016 |
| 18617 | 8.4          | 2016 |
| 18618 | 9.1          | 2016 |
| 18619 | 7.9          | 2016 |
| 18620 | 7.6          | 2016 |
| 18621 | 9.0          | 2016 |
| 18622 | 5.8          | 2016 |
| 18623 | 10.0         | 2016 |
| 18624 | 10.0         | 2016 |

18625 rows × 2 columns

当我们检索单个列时，我们实际上检索了一个 Pandas Series 对象。 DataFrame 存储表格数据，但是 Series 存储单个数据列或行。

我们可以验证单个列是否为系列：

``` 
type(reviews["score"])
```

```
pandas.core.series.Series
```

我们可以手动创建一个 Series，以更好地了解它是如何工作的。 创建一个 Series，当我们实例化它时，我们需要将一个 list 类型或 NumPy 数组传递给 Series 对象：

```python
s1 = pd.Series([1, 2])
s1
```

```
0    1
1    2
dtype: int64
```

Serise 可以包含任何类型的数据，包括混合类型。 在这里，我们创建一个包含字符串对象的 Serise：

```python
s2 = pd.Series(["Boris Yeltsin", "Mikhail Gorbachev"])
s2
```

```
0        Boris Yeltsin
1    Mikhail Gorbachev
dtype: object
```

### 通过 Pandas 创建 数据帧 DataFrame

我们可以通过将多个 Series 对象传递给 DataFrame 类来创建一个 DataFrame。 在这里，我们传入我们刚刚创建的两个 Series 对象，`s1` 作为第一行，`s2` 作为第二行：

```python
pd.DataFrame([s1, s2])
```

|       | 0             | 1                 |
| ----- | ------------- | ----------------- |
| **0** | 1             | 2                 |
| **1** | Boris Yeltsin | Mikhail Gorbachev |

我们也可以通过传递成员为列表的列表来完成同样的事情。 每个内部列表在结果 DataFrame 中被视为一行：

```python
pd.DataFrame(
    [
        [1,2],
        ["Boris Yeltsin", "Mikhail Gorbachev"]
    ]
)
```

|       | 0             | 1                 |
| ----- | ------------- | ----------------- |
| **0** | 1             | 2                 |
| **1** | Boris Yeltsin | Mikhail Gorbachev |

我们可以在创建 DataFrame 时指定列标签：

```python
pd.DataFrame(
    [
        [1,2],
        ["Boris Yeltsin", "Mikhail Gorbachev"]
    ],
    columns=["column1", "column2"]
)
```

|       | column1       | column2           |
| ----- | ------------- | ----------------- |
| **0** | 1             | 2                 |
| **1** | Boris Yeltsin | Mikhail Gorbachev |

同样可以指定行标签（即索引 index ）：

```python
frame = pd.DataFrame(
    [
        [1, 2],
        ["Boris Yeltsin", "Mikhail Gorbachev"]
    ],
    index=["row1", "row2"],
    columns=["column1", "column2"]
)
frame
```

|          | column1       | column2           |
| -------- | ------------- | ----------------- |
| **row1** | 1             | 2                 |
| **row2** | Boris Yeltsin | Mikhail Gorbachev |

然后，我们可以使用以下标签对DataFrame建立索引：

```python
frame.loc["row1":"row2", "column1"]
```

```
row1                1
row2    Boris Yeltsin
Name: column1, dtype: object
```

如果我们将字典传递给 DataFrame 的构造函数，那么我们可以跳过指定 `column` 关键字参数。 这将会自动为列设置名称：

```python
frame = pd.DataFrame(
    {
        "column1": [1, 2],
        "column2": ["Boris Yeltsin", "Mikhail Gorbachev"]
    }
)
frame
```

|       | column1 | column2           |
| ----- | ------- | ----------------- |
| **0** | 1       | Boris Yeltsin     |
| **1** | 2       | Mikhail Gorbachev |

### Pandas DataFrame 方法

正如之前我们提到的，DataFrame 的每一个列都是一个 Series 对象

```python
type(reviews["title"])
```

```
pandas.core.series.Series
```

那些对 DataFrame 适用的方法大多同样也适用于 Series 对象，包括 `head`：

```python
reviews["title"].head()
```

```
0                              LittleBigPlanet PS Vita
1    LittleBigPlanet PS Vita -- Marvel Super Hero E...
2                                 Splice: Tree of Life
3                                               NHL 13
4                                               NHL 13
Name: title, dtype: object
```

Pandas Series 和 DataFrames 中也有其他方法，使计算更简单。 例如，我们可以使用 [pandas.Series.mean](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.mean.html) 方法来查找一个 Series 的平均值：

```python
reviews['score'].mean()
```

```
6.950459060402685
```

我们也可以调用类似的 pandas.DataFrame.mean 方法，它将在默认情况下找到 DataFrame 中每个数字列的平均值：

```python
reviews.mean()
```

```
score               6.950459
release_year     2006.515329
release_month       7.138470
release_day        15.603866
dtype: float64
```

我们可以通过给 `mean` 方法添加 `axis `关键字参数，用来计算每行或者每列的平均值。`axis` 的缺省值为 0 ，并计算每一列的平均值。也可以设置为 1 来计算每一行的平均值。请注意，这只会计算每一行中类型为数值的平均值：

```python
reviews.mean(axis=1)
```

```
0        510.500
1        510.500
2        510.375
3        510.125
4        510.125
5        509.750
6        508.750
7        510.250
8        508.750
9        509.750
10       509.875
11       509.875
12       509.500
13       509.250
14       509.250
15       508.375
16       508.375
17       508.500
18       507.375
19       507.750
20       507.750
21       514.625
22       514.625
23       514.625
24       515.000
25       514.250
26       514.750
27       514.125
28       514.250
29       513.625
          ...   
18595    510.850
18596    510.875
18597    510.225
18598    510.700
18599    510.750
18600    512.600
18601    512.600
18602    512.600
18603    512.450
18604    512.400
18605    511.500
18606    508.600
18607    510.750
18608    510.350
18609    510.750
18610    510.250
18611    508.700
18612    509.200
18613    508.000
18614    515.050
18615    515.050
18616    508.375
18617    508.600
18618    515.025
18619    514.725
18620    514.650
18621    515.000
18622    513.950
18623    515.000
18624    515.000
dtype: float64
```

在 Series 和 DataFrames 上有很多方法，它们的行为类似于 `mean`。 这里有一些常见的：

- [pandas.DataFrame.corr](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.corr.html) – 查找 DataFrame 中列之间的相关性。
- [pandas.DataFrame.count](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.count.html) – 计算每个 DataFrame 列中的非空值的数量。
- [pandas.DataFrame.max](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.max.html) – 查找每个列中的最大值。
- [pandas.DataFrame.min](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.min.html) – 查找每个列中的最小值。
- [pandas.DataFrame.median](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.median.html) – 查找每列的中位数。
- [pandas.DataFrame.std](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.std.html) – 查找每列的标准差。

我们可以使用 `corr` 方法来查看是否有任何列与 score 相关。 例如，通过这种方式我们可以得到，最近发布的游戏是否获得了更高的评价（release_year），或者是否年底发布的游戏得分更好（release_month）：

```python
reviews.corr()
```

|                   | score    | release_year | release_month | release_day |
| ----------------- | -------- | ------------ | ------------- | ----------- |
| **score**         | 1.000000 | 0.062716     | 0.007632      | 0.020079    |
| **release_year**  | 0.062716 | 1.000000     | -0.115515     | 0.016867    |
| **release_month** | 0.007632 | -0.115515    | 1.000000      | -0.067964   |
| **release_day**   | 0.020079 | 0.016867     | -0.067964     | 1.000000    |

如上所述，我们的数字列都不与 `score` 相关，这意味着发布时间与审核分数没有线性关系。