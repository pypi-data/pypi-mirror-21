ctp_deps
========

Do not depend on me directly. After install this package,

``.h`` files will be installed in ``pkg_resources.resource_filename("ctp_deps", "include")``.
``.so`` files will be installed in ``pkg_resources.resource_filename("ctp_deps", "lib")``.

Now you can use these variables in ``setup.py``
