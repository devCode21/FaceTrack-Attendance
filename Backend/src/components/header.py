from bson.objectid import ObjectId 
import cv2 
import torch
from pathlib import Path
from ultralytics import YOLO
import numpy as np
import logging
from datetime import datetime
import os
import sys
from facenet_pytorch import MTCNN, InceptionResnetV1
from bson.objectid import ObjectId  # <-- CRITICAL FIX 1: For MongoDB query
from src.utils.log import setup_logger
import PIL
from PIL import Image
import torch
import torchvision 
from torch import nn 
from dataclasses import dataclass
from facenet_pytorch import MTCNN, InceptionResnetV1
image_size=160
from pathlib import Path 
import cv2 as cv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from src.components.helper_function import get_embeddings_from_database , detect_faces_from_frame 



Yolo_Model_path = r'uploads\yolov12n-face.pt'
EDSR_Model_path = r"uploads\EDSR_x2.pb"    