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

### Dataframe Math with Pandas

我们还可以对 Series 或 DataFrame 对象执行数学运算。 例如，我们可以将核心列中的每个值除以 `2`，将比例从 `0-10` 切换到 `0-5`：

```
reviews["score"] / 2
```

```
0        4.50
1        4.50
2        4.25
3        4.25
4        4.25
5        3.50
6        1.50
7        4.50
8        1.50
9        3.50
10       3.75
11       3.75
12       3.50
13       4.50
14       4.50
15       3.25
16       3.25
17       4.00
18       2.75
19       3.50
20       3.50
21       3.75
22       3.75
23       3.75
24       4.50
25       3.50
26       4.50
27       3.75
28       4.00
29       3.25
         ... 
18595    2.20
18596    3.25
18597    2.45
18598    3.40
18599    3.50
18600    3.70
18601    3.70
18602    3.70
18603    3.90
18604    4.30
18605    3.00
18606    3.20
18607    3.50
18608    2.70
18609    4.00
18610    3.00
18611    2.90
18612    3.90
18613    4.00
18614    4.60
18615    4.60
18616    3.75
18617    4.20
18618    4.55
18619    3.95
18620    3.80
18621    4.50
18622    2.90
18623    5.00
18624    5.00
Name: score, dtype: float64
```

在 Python 中所有常见数学运算符（如 `+`，` -` ，`*`，`/` 和 `^ `）对于 DataFrame 或 Series 都起作用，并且对其中的每个元素也都适用。

### Boolean Indexing in Pandas

如上所述，`reviews` 的 `score` 列中的所有值的平均值大约为 7。 我们如何找到所有得分超过这个平均分的游戏呢？ 通长开始我们会做比较，将 Series 中的每个值与指定值进行比较，然后生成一个布尔类型的 Series，用来表示比较的状态。 例如，我们可以看到哪些行的 `score` 值大于 7：

```
score_filter = reviews["score"] > 7  
score_filter
```

```
0         True
1         True
2         True
3         True
4         True
5        False
6        False
7         True
8        False
9        False
10        True
11        True
12       False
13        True
14        True
15       False
16       False
17        True
18       False
19       False
20       False
21        True
22        True
23        True
24        True
25       False
26        True
27        True
28        True
29       False
         ...  
18595    False
18596    False
18597    False
18598    False
18599    False
18600     True
18601     True
18602     True
18603     True
18604     True
18605    False
18606    False
18607    False
18608    False
18609     True
18610    False
18611    False
18612     True
18613     True
18614     True
18615     True
18616     True
18617     True
18618     True
18619     True
18620     True
18621     True
18622    False
18623     True
18624     True
Name: score, dtype: bool
```

一旦我们有一个 Boolean Series，我们可以使用它只选择 DataFrame 中的 Series 值 为 True 行。 因此，我们可以从 `reviews` 中只选择 `score` 大于 7 的行：

```python
filtered_reviews = reviews[score_filter]
filtered_reviews.head()
```

|      | score_phrase | title                                    | url                                      | platform         | score | genre      | editors_choice | release_year | release_month | release_day |
| ---- | ------------ | ---------------------------------------- | ---------------------------------------- | ---------------- | ----- | ---------- | -------------- | ------------ | ------------- | ----------- |
| 0    | Amazing      | LittleBigPlanet PS Vita                  | /games/littlebigplanet-vita/vita-98907   | PlayStation Vita | 9.0   | Platformer | Y              | 2012         | 9             | 12          |
| 1    | Amazing      | LittleBigPlanet PS Vita -- Marvel Super Hero E... | /games/littlebigplanet-ps-vita-marvel-super-he... | PlayStation Vita | 9.0   | Platformer | Y              | 2012         | 9             | 12          |
| 2    | Great        | Splice: Tree of Life                     | /games/splice/ipad-141070                | iPad             | 8.5   | Puzzle     | N              | 2012         | 9             | 12          |
| 3    | Great        | NHL 13                                   | /games/nhl-13/xbox-360-128182            | Xbox 360         | 8.5   | Sports     | N              | 2012         | 9             | 11          |
| 4    | Great        | NHL 13                                   | /games/nhl-13/ps3-128181                 | PlayStation 3    | 8.5   | Sports     | N              | 2012         | 9             | 11          |

可以使用多个条件进行过滤。 让我们找找在` Xbox One` 发布得分超过 `7` 的游戏。 在下面的代码中：

* 为过滤器设置两个条件：
  * 检查 `score` 是否大于 `7`
  * 检查 `platform` 是否是 `Xbox One`
    * 给 `reviews` 应用上边的顾虑器来获取我们想要的行。
* 使用 `head` 方法打印 `filtered_review `的前 5 行。

```python
xbox_one_filter = (reviews['score'] > 7) & (reviews['platform']=='Xbox one')
filter_reviews = reviews[xbox_one_filter]
filtered_reviews.head()
```

|      | score_phrase | title                                    | url                                      | platform         | score | genre      | editors_choice | release_year | release_month | release_day |
| ---- | ------------ | ---------------------------------------- | ---------------------------------------- | ---------------- | ----- | ---------- | -------------- | ------------ | ------------- | ----------- |
| 0    | Amazing      | LittleBigPlanet PS Vita                  | /games/littlebigplanet-vita/vita-98907   | PlayStation Vita | 9.0   | Platformer | Y              | 2012         | 9             | 12          |
| 1    | Amazing      | LittleBigPlanet PS Vita -- Marvel Super Hero E... | /games/littlebigplanet-ps-vita-marvel-super-he... | PlayStation Vita | 9.0   | Platformer | Y              | 2012         | 9             | 12          |
| 2    | Great        | Splice: Tree of Life                     | /games/splice/ipad-141070                | iPad             | 8.5   | Puzzle     | N              | 2012         | 9             | 12          |
| 3    | Great        | NHL 13                                   | /games/nhl-13/xbox-360-128182            | Xbox 360         | 8.5   | Sports     | N              | 2012         | 9             | 11          |
| 4    | Great        | NHL 13                                   | /games/nhl-13/ps3-128181                 | PlayStation 3    | 8.5   | Sports     | N              | 2012         | 9             | 11          |

当使用多个条件进行过滤时，将每个过滤条件放在括号中，并用 & 符号把它们连接起来。

### Pandas Plotting

现在我们知道如何进行过滤，我们可以创建图来观察 Xbox One 的评论分布与 PS 4 的评论分布。 这将帮助我们了解哪个平台有更好的游戏。 我们可以通过直方图来做到这一点，这将绘制不同得分范围的游戏出现的次数，这将告诉我们哪个平台更多的高评级游戏。

我们可以使用 [pandas.DataFrame.plot](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.plot.html) 方法，为每个平台创建一个直方图。这个方法利用流行的 Python 绘图库 matplotlib，从而生成好看的图标。

> 译者注： pip3 install matplotlib 安装 matplotlib 包

绘图方法默认为绘制线图。 我们需要传入关键字参数 `kind =“hit”` 来绘制一个直方图。

在下面的代码中，我们：

* 在 Jupyter notebook 中调用 `％matplotlib inline` 设置绘图。
* 从 `reviews` 中筛选只有 Xbox One 的数据。
* 绘制 `score `列。

```python
%matplotlib inline
reviews[reviews["platform"] == "Xbox One"]["score"].plot(kind="hist")
```

```
<matplotlib.axes._subplots.AxesSubplot at 0x113988860>
```

![pic1](data:image/png;base64,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)

我们同样可以绘制 PS 4 的直方图：

```python
reviews[reviews["platform"] == "PlayStation 4"]["score"].plot(kind="hist")
```

```
<matplotlib.axes._subplots.AxesSubplot at 0x113a8d588>
```

![pic2](data:image/png;base64,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)

从直方图看来，PS 4 具有比 Xbox One 更多的高评级游戏。

```python
filtered_reviews["score"].hist()
```

```
<matplotlib.axes._subplots.AxesSubplot at 0x113cb6b70>
```

![pic3](data:image/png;base64,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)