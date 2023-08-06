# Timeswitch: Time Period Expression Language #

Timeswitch allows dates to be tested against a time range to see if they are contained within the
time range. Time ranges are expressed using a simple grammar that supports absolute dates and
times, repeating periods, greater, less than, between and exact match comparisons, and combinations
of brackets and infix notation logical operators.

A time is made up of the following ordered components, with sensible defaults for
components when omitted:

* *year:* range expression with values 1-9999
* *month:* range expression with integer values 1-12 or case insensitive jan, feb, mar, apr, may, 
    jun, jul, aug, sep, oct, nov, dec
* *day:* range expression with either integer values 1-31 or case insensitive mon, tue, wed, thu, 
    fri, sat, sun. When used with a month a weekday has an optional ordinal 1st, 2nd, 3rd, 4th or 
    5th prefix to indicate nth weekday in the month
* *hour-minute:* range expression with two integer values separated by a colon 0-23:0-59
* *compound:* range expression with all or partial non ambiguous sequences of year month day 
    hour-minute values

The expected month, weekday and ordinal strings can be overriden if necessary using the API.

A time range expression is similar to Python array syntax:

* `-` is any value
* `x` is a value = x
* `x-y` is a value x ≤ value ≤ y. Note that:
    * The expressions on either side of the `-` must  specify the same rightmost elements, e.g 
      `2017 jan - feb` not `2017 jan - feb 12`
    * The repeat period of the right hand side must be the same as or more frequent thant the first
      e.g `jan - 2017 feb` is not valid
    * For weekday ranges, Monday is considered the start of the week
* `-x` is a value less than or equal to x
* `x-` is a value greater than or equal to x

Time range expressions can be combined using `and`, `or`, `not` and `( )` to form nested 
expressions.

The empty string is always off. A dash is always on:

```-```

Always on from 1:30am on the 3rd of April 2017:

```2017 apr 3 1:30 -```

Always on every Friday on or after the 3rd of April 2017 (year and month can be omitted because 
'fri' is unambiguously a weekday):

```fri and 2017 apr 3 -```

Always on every 1st Friday of the month on or after the 3rd of April 2017:

```1st fri and 2017 apr 3 -```

Always on every 1st or 3rd Friday of the month on or after the 3rd of April 2017:

```(1st fri or 3rd fri) and 2017 apr 3 -```

First Friday of the month between 6:30pm and 9:50pm:

```1st fri 18:30-21:50```

Thanksgiving, Christmas, Boxing Day and New Year's Day:

```nov 4th thu or dec 25 or dec 26 or jan 1```

Normal operator precedence is `not`, `and`, `or`. Parenthesis can be used to change this:

```not((jun or aug) and 2017)```


## Usage ##

A command line interface for timeswitch is available:

```bash
$ timeswitch
usage: timeswitch [-h] [-d] [-w] [-y] [-a] [-p] expression [date]
timeswitch: error: too few arguments
$ timeswitch "2017 jan 20 -"
on
$ echo $?
0
$ timeswitch "1972 dec 5 - 1975 nov 11"
off
$ echo $?
1
$
```

The `--year`, `--week`, and `--day` options provide helpful visualisations when developing and
debugging timeswitch expressions.

To use the library directly in Python:

```python
from timeswitch import timeswitch
from datetime import datetime

ts = timeswitch('2017 may 4 20:20 - 20:30')
print ts(datetime(2017, 5, 4, 20, 21))  # True
print ts(datetime(2017, 5, 4, 20, 31))  # False
```

`timeswitch()` accepts optional named `months`, `weekdays` and `ordinal` arguments. Each is an
array of alternative literal strings used when parsing the corresponding date part, for example if
you want to write 'first wed' instead of '1st wed':

```python
ts = timeswitch('first wed', ordinals='first second third fourth fifth'.split(' '))
```


## Contributing ##

You may contribute to the project by logging issues through the project issue tracker or by
submitting a pull request.

### Development ###

A development environment may be setup like this:

```bash
git clone https://bitbucket.org/rocketboots/timeswitch.git
cd timeswitch
pip install -e .[test]
python setup.py nosetests
```

Contributions should include passing unit tests.

### PyPI Registration ###

To support reStructuredText as PyPI expects, this document is automatically converted provided the
[Pandoc](http://pandoc.org/) package is installed. On OS X,

```bash
brew install pandoc
pip install pypandoc twine
python setup.py sdist
twine register dist/timeswitch-*.tar.gz
```
