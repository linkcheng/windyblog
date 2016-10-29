## Coverage.py 简介

标签（空格分隔）：Python 代码覆盖率 翻译组

---
[阅读原文](http://www.blog.pythonlibrary.org/2016/07/20/an-intro-to-coverage-py/)

**Coverage.py**  是一个用来测试代码覆盖率的 Python 第三方库。它起初是由 Ned  Batchelder 创建。在编程界的术语“覆盖”通常是用来描述你的测试的有效性，以及单体测试的实际覆盖率。如果想使用 coverage.py 库，那么需要 Python2.6 或者更高的版本，并且它兼容 Python3 以及 PyPy 。

	pip install coverage

　　执行以上指令来安装 coverage.py ，不过我们需要码一些代码才能使用它。创建一个名为 mymath.py 的模块。代码如下：
```python
	def add(a, b):
		return a + b


	def subtract(a, b):
		return a - b


	def multiply(a, b):
		return a * b


	def divide(numerator, denominator):
		return float(numerator) / denominator
```
　　现在来做一下测试，如给 **add** 函数添加测试函数。首先我们需要创建一个名为 **test_mymath.py** 的文件，的文件，并且把它保存在与 mymath.py 的相同目录下。接着在测试文件中写入以下代码：
``` python
	# test_mymath.py
	import mymath
	import unittest

	class TestAdd(unittest.TestCase):
		"""
		Test the add function from the mymath library
		"""

		def test_add_integers(self):
			"""
			Test that the addition of two integers returns the correct total
			"""
			result = mymath.add(1, 2)
			self.assertEqual(result, 3)

		def test_add_floats(self):
			"""
			Test that the addition of two floats returns the correct result
			"""
			result = mymath.add(10.5, 2)
			self.assertEqual(result, 12.5)

		def test_add_strings(self):
			"""
			Test the addition of two strings returns the two string as one
			concatenated string
			"""
			result = mymath.add('abc', 'def')
			self.assertEqual(result, 'abcdef')


	if __name__ == '__main__':
		unittest.main()
```
　　一切准备就绪，让我们通过 coverage.py 来运行我们的测试文件。首先，打开终端并且进入我们刚才写的那两个文件的目录。接下来通过以下方式执行 coverage.py：

	coverage run test_mymath.py

　　注意，在运行 coverage.py 时需要参数 **run** 来指定测试的模块。如果被测试的模块接收参数，应该像正常运行这个的模块一样带上参数。当执行以上指令后，你会看到测试模块的输出，就像没有使用这个库一样，不受任何影响。在当前目录下你还会发现一个名字为 **.coverage** 的文件（注意开头的点号）。要想获得文件中的信息，需要执行以下指令：

	coverage report -m

　　执行这条指令将会在终端打印以下信息：
```
Name             Stmts   Miss  Cover   Missing
----------------------------------------------
mymath.py            9      3    67%   9, 13, 17
test_mymath.py      14      0   100%
----------------------------------------------
TOTAL
```
　　**-m** 选项告诉 coverage.py 你想在输出信息中显示 **Missing** 列。如果省略 **-m** 选项，就只能看到前四列信息。以上的就是 coverage 运行测试程序后的结果，结果表明这份单体测试程序对 mymath 模块的单体覆盖率只有 67% 。 “Missing” 列表明哪些行代码没有被覆盖。如果你看过 coverage.py 指出的那些行的代码，很快就会发现测试程序没有运行测试 **subtract**, **multiply** 和 **divide** 函数。
　　在尝试添加更多的覆盖率测试代码之前，先来学习一下怎么通过 coverage.py 来生成 HTML报告。只需要执行以下命令即可：

	coverage html

　　以上指令将会生成一个叫 **htmlcov** 的目录，其中包括各种各样的文件。进入这个目录，并通过浏览器打开 **index.html** 文件。在我的电脑上显示如下图：

![chp26_coverage_index](http://www.blog.pythonlibrary.org/wp-content/uploads/2016/07/chp26_coverage_index.png)

　　实际上，你可以通过点击 Module 列中列出的文件名来打开一个新的页面，页面中将会明显标识出代码中没有被单体覆盖的部分。显然 mymath.py 的覆盖率不够高，所以点击 mymath.py ，画面最终显示如下：

![chp26_mymath_coverage](http://www.blog.pythonlibrary.org/wp-content/uploads/2016/07/chp26_mymath_coverage.png)

　　以上截图清晰的展示了没有被初版单体测试所覆盖的部分。现在终于明确我们的单体覆盖率有哪些缺失了，现在就给 **subtract** 函数添加单体测试，并且看一下覆盖率的改变。
　　打开 **test_mymath.py** 并且添加下边的类：
``` python
	class TestSubtract(unittest.TestCase):
		"""
		Test the subtract function from the mymath library
		"""

		def test_subtract_integers(self):
			"""
			Test that subtracting integers returns the correct result
			"""
			result = mymath.subtract(10, 8)
			self.assertEqual(result, 2)
```
　　以上截图清晰的展示了没有被初版单体测试所覆盖的部分。现在终于明确我们的单体覆盖率有哪些缺失了，现在就给 **subtract** 函数添加单体测试，并且看一下覆盖率的改变。
　　打开 **test_mymath.py** 并且添加下边的类：

![chp26_subtract_coverage](http://www.blog.pythonlibrary.org/wp-content/uploads/2016/07/chp26_subtract_coverage.png)

　　这次修改覆盖率有 11% 的提高！让我们给 multiply 和 divide 函数页添加简单的测试，看覆盖率能否达到 100% ！
``` python
	class TestMultiply(unittest.TestCase):
		"""
		Test the multiply function from the mymath library
		"""

		def test_subtract_integers(self):
			"""
			Test that multiplying integers returns the correct result
			"""
			result = mymath.multiply(5, 50)
			self.assertEqual(result, 250)


	class TestDivide(unittest.TestCase):
		"""
		Test the divide function from the mymath library
		"""

		def test_divide_by_zero(self):
			"""
			Test that multiplying integers returns the correct result
			"""
			with self.assertRaises(ZeroDivisionError):
				result = mymath.divide(8, 0)
```
　　再次运行之前运行过的命令，然后再重新打开 “index.html”。然后就会看到如下截图：

<img src="http://www.blog.pythonlibrary.org/wp-content/uploads/2016/07/chp26_full_coverage.png" width="597">

　　正如你看到的那样，这次我们的覆盖率达到了 100%！显然，覆盖率 100% 意味着我们测试程序走到了每一个需要被测试的函数。当然这也有些不尽人意的地方，比如：add 函数的单体测试次数是其他几个函数的三倍，然而 coverage.py 给出关于这些的详细信息。尽管coverage.py 不能详尽说明我们测试的所有可能的排列组合的情况，但它却明确反映了关于覆盖率的一些基本信息。

### 附录

　　顺便再简单提及一些 coverage.py 的其他特性。首先，coverage.py 支持配置文件。配置文件格式跟传统的“.ini”文件相当，都是使用中括号作为节与节的分界（例如：[my_section]）。还可以使用 # 或者 ; （分号）来表示注释。

　　Coverage.py 也允许在上述提到的配置文件中指定你需要解析的源文件。一旦在配置文件中设置了需要解析的文件，就可以通过运行 coverage.py 来看运行结果。它还支持“-source”命令行选项。最后，还可以使用“-include”和“-omit”选项来包含一个文件名模式的列表或者移除这个列表。这些选项通过在配置文件中添加的配置项进行匹配。

　　关于 coverage.py 想最后再说明一点，就是它支持插件。你可以自己写也可以从网上下载并安装别人的插件来增强 coverage.py 的功能。

### 总结

　　现在你已经了解 coverage.py 的基本情况以及它的一些用途。Coverage.py 可以检测单体测试代码并且发现单体测试覆盖率中的漏洞。如果你不确定你的单体测试程序是否达标，那么使用这个库包将会帮助你找到那些存在的漏洞。即便如此，你任然需要认真负责的编写高质量的测试程序。如果你的测试程序书写不规范或者不合法，尽管它可以运行，但是 coverage.py 却不能帮到你。




















