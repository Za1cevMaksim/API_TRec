from collections import deque
from io import BytesIO
from PIL import Image
import pytesseract
import os
import asyncio
from fastapi import FastAPI, UploadFile, BackgroundTasks, HTTPException
from uuid import uuid4
from typing import Dict, Union

app = FastAPI()
tasks = deque(maxlen=10)

class OCRProcessor:
    @staticmethod
    async def process_image(file_data: bytes, lang: str) -> str:
        try:
            image = Image.open(BytesIO(file_data))
            text = pytesseract.image_to_string(image, lang=lang)
            return text
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"{str(e)}")

@app.post("/process")
async def process_image_endpoint(file: UploadFile, lang: str = "rus+eng"):
    try:
        file_data = await file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")

    task_id = str(uuid4())
    lang=lang.replace(" ","+")
    task = {"task_id": task_id, "status": "work"}

    async def task_runner():
        try:
            result = await OCRProcessor.process_image(file_data, lang)
            task["status"] = "done"
        except Exception as e:
            task["status"] = "error"


    future = asyncio.create_task(OCRProcessor.process_image(file_data, lang))
    task["future"] = future

    tasks.append(task)

    return {"task_id": task_id}

@app.get("/status/{task_id}")
async def get_task_status(task_id: str):
    for task in tasks:
        if task["task_id"] == task_id:
            if task["status"] == "work" and task["future"].done():
                task["status"] = "done"
            return {
                "task_id": task_id,
                "status": task["status"],
                "result": task["future"].result() if task["status"] == "done" else None,
            }
    return {"task_id": task_id, "status": "not found"}

@app.post("/cancel/{task_id}")
async def cancel_task(task_id: str):
    for task in tasks:
        if task["task_id"] == task_id:
            if task["status"] == "work" and not task["future"].done():
                task["future"].cancel()
                task["status"] = "cancelled"
                return {"task_id": task_id, "status": "cancelled"}
            return {"task_id": task_id, "status": task["status"]}
    return {"task_id": task_id, "status": "not found"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)