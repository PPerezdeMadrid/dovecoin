# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 09:36:03 2024

@author: pperezdemadrid
"""

# Cliente HTTP Postman: https://www.getpostman.com/ (descargar app)

import datetime
from flask import Flask, jsonify
import json
import hashlib

# Parte 1: Crear la cadena de bloques
class Blockchain:
    
    # Constructor
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        


