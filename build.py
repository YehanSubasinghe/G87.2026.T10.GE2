#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.coverage")
use_plugin("python.pylint")

name = "G89.2026.TYY.GE2"
default_task = "publish"

@init
def set_properties(project):
    project.set_property("pylint_options", ["--rcfile=pylintrc"])