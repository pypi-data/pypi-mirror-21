Do What Thou Wilt Shall be the Whole of the Law.

======
gulag
=======

`gulag` is a high level mongo encapsulation.

Dedicated to all political, corporate & religious dissidents. In every juristiction.
Vive toutes les differences!


Highlights:

- Declarative collections (model in MVC paradigmn)
- Auto-reconnect
- Cache


Python package installation
----------------------------
>pip install gulag


setting.py
----------
MONGO_URL      = "mongodb://127.0.0.1:27017"


# Example in-application use:
-----------------------------

```

from gulag import nosql
import setting

setting.MAX_POOL_SIZE = 300

nosql.conf.from_object(setting)
from myapp.mymodel import Model

doc = Model.find_one({"key": "unique"})

```

Author: @jorjun
Love is the Law. Love under will.

# Change log --------------------------------------------------------------------------------------------------------------
- Remove Django cache// replace with generic cache + unit test
- Turn off automatic test_ prefix to database name. Sometimes you want to test on real data...
- Add analytics support e.g.
    MONGO_METRICS = {
        "DB_NAME": "analytics",
        "LIMIT_MS" : 500.0,  # Record nothing quicker than 500ms
    }
- Dedication & motivation
- Increase default connection pool from 20 to 200
