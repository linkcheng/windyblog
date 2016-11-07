* OpenERP "objects" are usually called classes in object orientedprogramming.

OpenERP 的“对象”，在面向对象编程中通常被称为类。

* A OpenERP "resource" is usually called an object in OO programming,instance of a class.

一个 OpenERP 的“资源”在面向对象编程中通常称为一个对象，一个类的实例。

It's a bit confusing when you try to program inside OpenERP, because thelanguage used is Python, and Python is a fully object oriented language, andhas objects and instances ...								当您尝试在 OpenERP 内编程时，这是有一点混乱，因为所使用的语言是Python，Python 是一种完全面向对象的语言，有对象和实例...								

Luckily, an OpenERP "resource" can be converted magically into a nicePython object using the "browse" class method (OpenERP object method).								

幸运的是，OpenERP 的“资源”，可以神奇地转换成一个漂亮的使用“浏览”类方法的 Python 对象，(OpenERP 的对象方法)。



ORM:对象 - 关系-映射的缩写，是 OpenERP 的核心部分。

在 OpenERP 中，通过 Python 类和对象描述和操作数据模型。ORM 用来在Python 和底层关系数据库(PostgreSQL 系统)之间缩小差距，对开发者尽可能透明，提供我们需要的对象持久。