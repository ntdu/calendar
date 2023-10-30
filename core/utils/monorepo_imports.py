# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path

try:
    import core  # noqa
except ModuleNotFoundError:
    current_path = Path(os.getcwd())
    sys.path.append(str(current_path.parents[1]))
    import core  # noqa
