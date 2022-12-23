import os
import sys


PSSE_PATH = r"C:\Instalacije\PTI\PSSE35\35.3\PSSBIN"
PSSPY_PATH = r"C:\Instalacije\PTI\PSSE35\35.3\PSSPY37"

for PATH in [PSSE_PATH, PSSPY_PATH]:
    sys.path.append(PATH)
    os.environ['PATH'] = os.environ['PATH'] + ';' + PATH

import psspy
