# 一个每个人都需要的 Python 库

你写 Python 程序？那你应该使用 [attrs](https://attrs.readthedocs.io/)。

你问为什么？我只能说，不要问，尽管去用它。

好的。让我回到主题。

我热爱 Python，并且也是我主要的编程语言，而且有十多年使用经验。尽管在此期间我也意外的切换到其他的[有趣的语言](https://www.haskell.org/)做[开发](https://www.rust-lang.org/zh-CN/)，但这并不是 Python 本身的问题。尽管在某些情况下，Python 会让你更容易犯错，特别是一些库在类的继承上与 [God-object](https://en.wikipedia.org/wiki/God_object) 的反面模式上有非常糟糕的扩展。这其中的一个原因可能是 Python 是一种非常方便的语言，所以缺乏经验的程序员犯错误后，他们就继续[忍受下去](https://twistedmatrix.com/documents/current/core/development/policy/compatibility-policy.html)。但我想，更明显的原因也许是，有时你努力做正确的事，然而 Python 自身的一些特性会影响你。

在目标设计的背景下的“正确的事“是设计体量小并且独立的类，它们只做[一件事](https://en.wikipedia.org/wiki/Single_responsibility_principle)，并且做的非常[好](https://www.destroyallsoftware.com/talks/boundaries)。例如，如果你发现你的对象开始累积了大量的私有方法，也许你应该给私有属性提供 “public” [^1]的方法。但是，如果这种事处理起来非常乏味，你可能就不会理会这些。

你应该定义对象的另一个地方是当你有一些相关的数据，并且需要数据间关系以及数据不变性和行为是可解释的。Python 使得非常容易只定义一个元组或列表。您键入的 `host, port = …` 而不是 `address = …`。这看起来似乎似乎没有什么大不了的，但随后很快你键入 `[(family, socktype, proto, canonname, sockaddr)] = …`。长此以往，你的生活充满了遗憾。如果你只是开发人员，你是幸运的。如果你不幸运的话，你只是维护代码，并且代码看起来是这样的 `values[0][7][4][HOSTNAME][“canonical”]`，那么你的生活将会充满花园式的各种痛苦，而不仅仅是感到遗憾。



这就提出了一个问题：在 Python中使用类是否是乏味的？让我们来看一个简单的数据结构：一个三维直角坐标。从最简单的开始：

```python
class Point3D(object):
```

到现在为止还挺好。我们已经有了一个三维点。 接下来呢？

```python
class Point3D(object):
    def __init__(self, x, y, z):
```

其实，这是有点可惜。我只想对数据的打包，而我不得不覆盖一个 Python 特殊的方法，其名字是 Python 运行时内部约定俗成的？这还不算太坏，我想；毕竟所有的编程语言在流行前看起来都很奇怪。

至少可以看到属性名了，这是还能说得通。

```python
class Point3D(object):
    def __init__(self, x, y, z):
        self.x
```

我已经说过，我想一个 `x`，但现在我必须把它指定为一个属性...

```python
class Point3D(object):
    def __init__(self, x, y, z):
        self.x = x
```

为了获取 `x` ？呃，很明显...

```python
class Point3D(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
```

现在我必须为每个属性做一次，所以这相当糟糕？我 3 次输入每个属性的名字？！？
好吧。至少我现在是这么做的。

```python
class Point3D(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __repr__(self):
```

先不要着急问我，我还没有写好。

```python
class Point3D(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __repr__(self):
        return (self.__class__.__name__ +
                ("(x={}, y={}, z={})".format(self.x, self.y, self.z)))
```

拜托。所以，我必须键入每个属性名 5 次，如果当我在调试时，我希望能够看到这些属性的值？！？！？

```python
class Point3D(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __repr__(self):
        return (self.__class__.__name__ +
                ("(x={}, y={}, z={})".format(self.x, self.y, self.z)))
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)
```

7 次？！？！？！？

```python
class Point3D(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __repr__(self):
        return (self.__class__.__name__ +
                ("(x={}, y={}, z={})".format(self.x, self.y, self.z)))
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)
    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.x, self.y, self.z) < (other.x, other.y, other.z)
```

9 次？！？！？！？！？

```python
from functools import total_ordering
@total_ordering
class Point3D(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __repr__(self):
        return (self.__class__.__name__ +
                ("(x={}, y={}, z={})".format(self.x, self.y, self.z)))
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)
    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.x, self.y, self.z) < (other.x, other.y, other.z)
```

好了，噢 - 尽管多了 2 行代码不是很好，但至少现在我们没有必要定义其他所有的比较方法。但是，现在我们就大功告成了，对不对？

```python
from unittest import TestCase
class Point3DTests(TestCase):
```

你知道吗？ 我受够了。一个类码了 20 行，却什么事都没做；这个类最困难的部分是在解四元方程的时候，而不是“做打印和比较的数据结构”。我陷入了大量无用的垃圾元组，列表和字典中；用 Python[^2] 定义好合适的数据结构是非常辛苦的。

### 命名元组 `namedtuple` 的（不是真的）救援

为解决这个难题，标准库的给出的解决方案是使用 [namedtuple](https://docs.python.org/2.7/library/collections.html#collections.namedtuple) 。然而不幸的是初稿（它的这种风格在许多方面与[我自己](https://github.com/twisted/epsilon/blob/master/epsilon/structlike.py)的处理方式有相似的尴尬的和过时的方式）`namedtuple` 仍然无法挽救这个现象。它引入了大量的设计糟糕的公共函数，这对于兼容性维护来说简直就是一场噩梦，并且它连问题的一半都没有解决。尽管罗列所有的缺点是单调乏味的，但是有些仍然需要强调：

* 不管你是否希望如此，它的字段都可以通过索引的方式访问。并且你不能有私有属性，因为所有属性通过公开的 \_\_getitem\_\_ 接口被暴露出来。
* 它与有相同值的原始元组作比较，因此很容易发生类型混乱，特别是如果你想把它转换成元组和列表。
* 这是一个元组，所以它总是不可变的。 

至于最后一点，要么你可以像这样使用它：

```python
Point3D = namedtuple('Point3D', ['x', 'y', 'z'])
```

在这种情况下，它在你的代码中看起来并不像一种类型；无特殊情况下，简单的语法分析工具将不能识别它为一体。这用方式下你不能给它添加任何其他方法，因为没有地方放任何的方法。更何况事实，你必须输入类的名字两次。
或者你可以使用继承：

```python
class Point3D(namedtuple('_Point3DBase', 'x y z'.split()])):
    pass
```

尽管这看起来像给你一个地方，你可以添加方法和文档字符串，看起来也像一个类……但作为回报，你现在有一个奇怪的内部名称（其中在 `repr` 中显示的内容，并不是类的真实名称）。如果你默默在此处添加未列出的可变属性，这又是一个添加 `class` 声明的奇怪的副作用；也就是说，除非你在类中添加 `__slots__='X Y z'.split()`，如此一来，我们又只是回到需要键入两次属性名的问题上。而这还没有提到已经被证明的事实，你[不应该使用继承](https://www.youtube.com/watch?v=3MNVP9-hglc)。

因此，`namedtuple` 可以改善，如果它已经满足你的需求，只是在某些情况下，它有它自己的怪异的行为。

### 使用 `attr`

这就到了我最喜欢的 Python 库。
让我们重新审视上述问题。如何使 `Point3D` 与 `attrs` 结合在一起呢？

```python
import attr
@attr.s
```

由于它还没有内置到 Python 中，所以我们必须用以上 2 行开始：导入包然后使用类装饰器。

```python
import attr
@attr.s
class Point3D(object):
```

你看，没有继承！通过使用类装饰，`Point3D` 仍然是一个普通的 Python 类（尽管我们会短暂的看到一些有用的双下划线的方法）。

```python
import attr
@attr.s
class Point3D(object):
    x = attr.ib()
```

添加属性 `x`。

```python
import attr
@attr.s
class Point3D(object):
    x = attr.ib()
    y = attr.ib()
    z = attr.ib()
```

再分别添加属性 `y` 和 `z`。这样就完成了。

我们做了什么？ 等等。字符串该怎样表示呢？

```
>>> Point3D(1, 2, 3)
Point3D(x=1, y=2, z=3)
```

比较？

```
>>> Point3D(1, 2, 3) == Point3D(1, 2, 3)
True
>>> Point3D(3, 2, 1) == Point3D(1, 2, 3)
False
>>> Point3D(3, 2, 3) > Point3D(1, 2, 3)
True
```

好了。但如果我想通过 JSON 序列化的方式提取有明确属性定义的数据呢？

```python
>>> attr.asdict(Point3D(1, 2, 3))
{'y': 2, 'x': 1, 'z': 3}
```

也许上边有一点点准确。尽管如此，它应该变得更容易，因为 `attrs` 允许声明类中的字段，有很多关于它们元数据有趣的事情，下面就获取元数据。

```
>>> import pprint
>>> pprint.pprint(attr.fields(Point3D))
(Attribute(name='x', default=NOTHING, validator=None, repr=True, cmp=True, hash=True, init=True, convert=None),
 Attribute(name='y', default=NOTHING, validator=None, repr=True, cmp=True, hash=True, init=True, convert=None),
 Attribute(name='z', default=NOTHING, validator=None, repr=True, cmp=True, hash=True, init=True, convert=None))
```

我不打算在这里深入 `attrs` 的每一个有趣的功能；你可以阅读它的文档。另外，它是容易维护的，并且每隔一段时间都会有新的东西出现，因此我也可能会错过一些重要的事情。但是 `attrs` 这样做，一旦你有它们，你就会意识到，Python 在之前是缺少几个关键的事情：

1. 它让你简洁地定义类型，而不是通过手动键入 `def __init __`…… 的方式来定义类型。
2. 它让你直接地说出你声明的意思，而不是拐弯抹角的表达它。不应该是“我有一个类型，它被称为 MyType ，它有一个构造函数，在构造函数中用参数 'A' 给属性 'A' 赋值”，而是应该“我有一个类型，它被称为 MyType ，它有一个属性叫做 `a`，以及跟它相关的方法，而不必通过逆向工程猜测它的方法（例如，在一个实例中运行 `dir` ，或寻找 `self.__ class__. __dict__`）。
3. 它提供了有用的默认方法，而不像 Python，尽管有时也是有用的，但默认值通常后置。
4. 它尽管一开始用起来很简单，但在之后却要更加严格的实施。

最后再说一点。

### 进阶高级篇

虽然我不打算谈及每一个功能，但如果我没有提到以下几个特点，那我就太不负责任了。你可以从这些特别长的 `Attribute` 的 `repr()` 中看到一些有趣的东西。
例如：你通过用 `@attr.s` 修饰类来验证属性。比如：Point3D 这个类，应该包含数字。为简单起见，我们可以说这些数字为 `float` 类型，像这样：

```python
import attr
from attr.validators import instance_of
@attr.s
class Point3D(object):
    x = attr.ib(validator=instance_of(float))
    y = attr.ib(validator=instance_of(float))
    z = attr.ib(validator=instance_of(float))
```

我们使用 `attrs`，这意味着我们必须在额外的地方验证：我们可以只给每个需要的属性添加类型信息。

其中的一些设计，可以让我们避免一些常见的错误。例如，这是一个很常见的关于 Python 缺陷的面试问题：

```python
class Bag:
    def __init__(self, contents=[]):
        self._contents = contents
    def add(self, something):
        self._contents.append(something)
    def get(self):
        return self._contents[:]
```

修正它，当然，就变成这个样子了：

```python
class Bag:
    def __init__(self, contents=None):
        if contents is None:
            contents = []
        self._contents = contents
```

额外添加了 2 行代码。

这样，`contents` 无意间就成了全局变量，这使得所有 `Bag` 对象都共享一个列表，而不是各自使用不同的列表

使用 `attrs` 就变成这样：

```python
@attr.s
class Bag:
    _contents = attr.ib(default=attr.Factory(list))
    def add(self, something):
        self._contents.append(something)
    def get(self):
        return self._contents[:]
```

`attrs` 还提供一些其他的特性让你在构建类时更方便更正确。另一个很好的例子？如果你严格的管控对象的无关时属性（或在内存使用上更有效率的 CPython ），你可以在类层级上使用 `slots=True`  - 例如 `@attr.s(slots=True)` - 自动与 `attrs` 声明的 [`__slots__ `属性](https://docs.python.org/3.5/reference/datamodel.html#object.__slots__)匹配。所有这些方便的功能会让你通过 `attr.ib()` 声明的属性更好更强大。

### Python 的未来

有些人因为最终能够用 Python 3 编程而感到高兴。而我期待的是能够在 Python 编程时一直用`attrs`。它在使用的过程中发挥微妙而又积极的影响。
试试看：你会发现一些惊讶的地方，你现在在使用一个整洁而具有解释性的类，而在以前，你可能在使用稀疏文件的元组，列表或一个字典，偶尔还要忍受共同维护的困惑。结构化类型是如此容易的明确指出代码的目的（在`__repr__` 与 `__doc__` 中，甚至只是它们属性的名称）。你可能会发现你使用它的次数越多，你的代码将会变得越好；至少我一直是这样的。

### 注：

1. 这里的用双引号是因为把属性暴露给调用者是没有意义的，它们只是这么叫而已。这种模式，完全摆脱私有方法并且仅有私有属性，可能值得单独写一篇帖子。
2. 甚至我们还尚未得到的真正令人兴奋的东西：类型验证，默认值可变。