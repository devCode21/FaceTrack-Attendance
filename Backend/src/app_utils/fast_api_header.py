from fastapi import FastAPI
from src.DataBase.pymong import Class_Embeddings , Course_info
from src.pipelines.gettingresults import GettingResults, GettingResults_for_image 
from pydantic import BaseModel
import requests
from fastapi import UploadFile, File , Form
import torch
import json
import os
import pandas as pd
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import shutil
from fastapi import status, HTTPException
from fastapi.middleware.cors import CORSMiddleware


    

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow ANY origin
    allow_credentials=True,
    allow_methods=["*"],        # allow all methods GET, POST, PUT, DELETE
    allow_headers=["*"],        # allow all headers
)
