# NeoPySwitch

Python ```switch```-statement pseudo-implementation. Mimics C-style switch statements.

The following two code blocks should be equivalent:

```c
switch(arg):
{
    case 1:
        // Handle case
    case 2:
        // Handle case
    default:
        // Handle default case
}
```

```python
class Case1(SwitchCase):
    def __init__(self, arg1, arg2):
        self.__arg1 = arg1
        self.__arg2 = arg2
    def do_call(self, *args, **kwargs)
        # Handle call
        return self.__arg1 - self.__arg2
class Case2(SwitchCase):
    def __init__(self, arg1, arg2):
        self.__arg1 = arg1
        self.__arg2 = arg2
    def do_call(self, *args, **kwargs)
        # Handle call
        return self.__arg1 * self.__arg2
class CaseDefault(SwitchCase):
    def __init__(self, arg1, arg2):
        self.__arg1 = arg1
        self.__arg2 = arg2
    def do_call(self, *args, **kwargs)
        return self.__arg1 + self.__arg2
PySwitch(arg, {
    case_1 : Case1(arg1, arg2),
    case_2 : Case2(arg1, arg2)
}, CaseDefault(arg1, arg2))

```

## Installation

Simply use pip:

```
$ pip install NeoPySwitch
```

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History

* 0.1.0 - First alpha-release

## Credits

* [Zeno Rocha](https://github.com/zenorocha) - [GitHub README template](https://gist.github.com/zenorocha/4526327)
* [Ethan Forman](https://bitbucket.org/stoneleaf/) -
[```setup.py```-reference](https://bitbucket.org/stoneleaf/enum34/src/f24487b45cd041fc9406d67441d2186ac70772b7/setup.py?at=default&fileviewer=file-view-default)

## License

The MIT License (MIT)
Copyright (c) 2017 Thomas Li Fredriksen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.

