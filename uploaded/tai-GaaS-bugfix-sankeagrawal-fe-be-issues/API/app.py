from fastapi import FastAPI

from input_scanners_util import InputScannerUtil as IScanners
from output_scanners_util import OutputScannerUtil as OScanners
from schemas import (
    InputScannerRequest,
    OutputScannerRequest
)
from fastapi.middleware.cors import CORSMiddleware


app= FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

input_scanner_obj= IScanners()
output_scanner_obj= OScanners()

#an api with pydantic data validation
@app.post("/run_input_scanners")
async def run_input_scanners(request: InputScannerRequest):
    data= dict(**request.model_dump())
    prompt= data.get("prompt")
    scanner_configs= data.get("scanner_configs")
    fail_fast= data.get("fail_fast")
    return input_scanner_obj.run_input_scanners(prompt, scanner_configs, fail_fast)

# @app.post("/input_scanners_with_scan_prompt/")
# async def run_input_scanners(request: InputScannerRequest):
#     data= dict(**request.model_dump())
#     prompt= data.get("prompt")
#     scanner_configs= data.get("scanner_configs")
#     fail_fast= data.get("fail_fast")
#     return input_scanner_obj.run_with_scan_prompt(prompt, scanner_configs, fail_fast)

@app.post("/run_output_scanners")
async def run_input_scanners(request: OutputScannerRequest):
    data= dict(**request.model_dump())
    prompt= data.get("prompt")
    output= data.get("output")
    scanner_configs= data.get("scanner_configs")
    fail_fast= data.get("fail_fast")
    return output_scanner_obj.run_output_scanners(prompt, output, scanner_configs, fail_fast)

# @app.post("/output_scanners_with_scan_output/")
# async def run_input_scanners(request: OutputScannerRequest):
#     data= dict(**request.model_dump())
#     prompt= data.get("prompt")
#     output= data.get("output")
#     scanner_configs= data.get("scanner_configs")
#     fail_fast= data.get("fail_fast")
#     return output_scanner_obj.run_with_scan_output(prompt, output, scanner_configs, fail_fast)
