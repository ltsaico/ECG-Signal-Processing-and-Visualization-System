#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 22:11:54 2022

@author: carolinaazevedo
"""

from Interface import RootGUI_ECG, ComGUI, ECG_Functions

Root_Master = RootGUI_ECG()
ComMaster = ComGUI(Root_Master.root)
ECG = ECG_Functions(Root_Master.root)

# Start the Graphic User Interface
Root_Master.root.mainloop()