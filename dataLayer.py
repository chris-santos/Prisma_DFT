#  manipular arquivo de dados
# Autor: Christiano dos Santos

import sys
class DAO:
    def __init__(self):
        self.filename = ""
        self.output_lines = []
        self.wavenum_list = []
        self.negative_waves_list = []
        self.irData_list = []
        self.VIBRATIONAL_str = "VIBRATIONAL FREQUENCIES"
        self.NORMAL_MODES_str = "NORMAL MODES"
        self.inputSection = ''