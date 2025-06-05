# Created By: Agustin Do Canto 2025
from . import RelaxCore as RelaxCoreModule
import sys

# Permitir que se pueda hacer: from RelaxCore import Component
sys.modules["RelaxCore"] = RelaxCoreModule
