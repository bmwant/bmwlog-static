---
title: Deprecation of package extras
tags: [python, poetry, packaging, setuptools, pip]
author: Misha Behersky
language: en
date: 2022-09-23 11:45:27
---

It's a common case for the package to rely on [extras](https://peps.python.org/pep-0508/#extras) syntax to optionally install packages which are not required for the main functionality. For example, `pip install 'black[jupyter]'` allows you to use [black](https://black.readthedocs.io/en/stable/index.html) formatting utility with your [Jupyter notebooks](https://jupyter.org/), but otherwise there is no need to bring new dependencies into your virtual environment especially if they are *heavy* to install.

With that premise sometimes you want to either completely deprecate extras or refactor them into a different name. As an aware package maintainer you should release an intermediate version with the warning about deprecation. That's the case where you might want to consider adding [package-extras](https://pypi.org/project/package-extras/) package. It's a simple hack that allows you to emit a warning only when package has been installed through extras syntax invocation.

### How to use useless package

First step is to update your project's configuration file `pyproject.toml` and add `package-extras` into the section we want to deprecate (`databases` in the example below).

```toml
[tool.poetry.dependencies]
package-extras = { version = "^0.2.0", optional = true }
# your actual extras below
psycopg2 = { version = "^2.9", optional = true }
mysqlclient = { version = "^1.3", optional = true }

[tool.poetry.extras]
# append our package to the list
databases = ["package-extras", "mysqlclient", "psycopg2"]
```

Same example as above, but for the case when you still maintain `setup.py` file for your project.

```python
from setuptools import setup

install_requires = [
  # list of your main dependencies
]

extras_require = {
  'databases': [
    'psycopg2>=2.9,<3.0',
    'mysqlclient>=1.3,<2.0',
    # append our package to the list
    'package-extras>=0.2.0,<1.0.0',
  ]
}

setup_kwargs = {
    # rest of the arguments
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}

setup(**setup_kwargs)
```

Then add this logic to your entrypoint or top-level `__init__.py` file to raise deprecation warning

```python
import warnings

try:
    import package_extras
except ImportError:
    pass
else:
    warnings.warn(
        "'test_package[databases]' extra is deprecated and will be "
        "removed in a future release. Read more in this issue: "
        "https://bmwlog.pp.ua/deprecation-of-package-extras/",
        category=DeprecationWarning,
        stacklevel=2,
    )
```

You might wonder why don't we just import some package from the list and make assertion based on its presence. First of all this package might be installed by some other dependency or just be present in your virtual environment. Secondly, you might end up with a huge import block in case you decided to check *every package* that belongs to extras (even this wouldn't guarantee mitigation of the first case). In contrast, `package_extras` is definitely present in the environment only if you have invoked installation using extra syntax, so this approach is the most resillient one.

### Opposite scenario

There is an opposite case where you want to make sure that some extras were installed. Imagine your CI uses a lot of tools to bump version, update release notes, publish release to artifactory and upload *wheel* to the internal S3 bucket. You don't need this tools neither for development, nor to be packaged by default with your project.

```toml
[tool.poetry.dependencies]
package-extras = { version = "^0.2.0", optional = true }
# your actual extras below
"github3.py" = { version = "^3.2.0", optional = true }

[tool.poetry.extras]
# A lot more of other dependencies here
# It doesn't make sense to use this approach for one simple library
ci = ["package-extras", "github3.py"]
```

In the same time you might rely on the cli entrypoint that invokes all the mentioned steps within its code. So this check can warn you about missing `pip install test_package[ci]` step or just *fail fast* after this step instead of having unexpected import error somewhere in the middle of your pipeline.

```python
import warnings

try:
    import package_extras
except ModuleNotFoundError:
    warnings.warn(
        "You are going to use functionality that depends on 'ci' extras. "
        "Please install 'test_package[ci]' to proceed.",
        category=ImportWarning,
        stacklevel=2,
    )
```

> **NOTE**: `ImportWarning` warnings are disabled by default, so if you want your users to actually see the error during the import it is better to use `RuntimeWarning` instead. Alternatively, you can pass extra command line flag `python -Walways` on invocation.

### Resources

* [package-extras on PyPI](https://pypi.org/project/package-extras/)
* [Python warning categories](https://docs.python.org/3/library/warnings.html#warning-categories)
* [Inspired by approach used in urllib3](https://github.com/urllib3/urllib3/blob/1.26.12/src/urllib3/__init__.py#L27)
* [asottile video on the topic](https://youtu.be/_jUXdX8e9Wg)
