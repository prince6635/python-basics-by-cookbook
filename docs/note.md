* string concatenation: + or +=
http://stackoverflow.com/questions/12169839/which-is-the-preferred-way-to-concatenate-a-string-in-python

* always implement __repr__ for printing, since __str__ uses it, too.
http://stackoverflow.com/questions/1436703/difference-between-str-and-repr-in-python

* string format: https://pyformat.info/

* arbitrary number of arguments http://stackoverflow.com/questions/36901/what-does-double-star-and-star-do-for-python-parameters
    - \*args will give you all function parameters as a tuple
    - \**kwargs will give you all keyword arguments except for those corresponding to a formal parameter as a dictionary

* __slots__
    http://stackoverflow.com/questions/472000/usage-of-slots
    http://stackoverflow.com/questions/20406363/setattr-versus-slots-for-constraining-attribute-creation-in-python
    mainly based on whether you need __setattr__ or not.
