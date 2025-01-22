from PIL import Image
import pytesseract
import os
import asyncio
from fastapi import FastAPI, UploadFile, BackgroundTasks, HTTPException
from uuid import uuid4
from typing import Dict, Union
from fastapi.responses import JSONResponse



app = FastAPI()

tasks: Dict[str, asyncio.Future] = {}

class OCRProcessor:
    """
    ����� ��� ��������� OCR ��������.
    """
    @staticmethod
    async def process_image(file: UploadFile, lang: str) -> str:
        """
        ���������� ����� �� �����������.

        :param file: ����������� ����.
        :param lang: ����� ��� OCR.
        :return: ������������ �����.
        """
        try:
            image = Image.open(file.file)
            text = pytesseract.image_to_string(image, lang=lang)
            return text
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"{str(e)}")

@app.post("/process")
async def process_image_endpoint(file: UploadFile, lang: str = "rus+eng", background_tasks: BackgroundTasks = None):
    """
    �������� ��� ��������� OCR �������.

    :param file: ����������� ����.
    :param lang: ����� ��� OCR.
    :param background_tasks: �������� ������� �����.
    :return: ������������� ������.
    """
    task_id = str(uuid4())
    future = asyncio.create_task(OCRProcessor.process_image(file, lang))
    tasks[task_id] = future

    def remove_task():
        tasks.pop(task_id, None)

    future.add_done_callback(lambda _: remove_task())
    return {"task_id": task_id}

@app.get("/status/{task_id}")
async def get_task_status(task_id: str):
    """
    �������� ��� ��������� ������� ������.

    :param task_id: ������������� ������.
    :return: ������ ������.
    """
    task = tasks.get(task_id)
    if not task:
        return {"task_id": task_id, "status": "not found"}

    if task.done():
        return {"task_id": task_id, "status": "completed", "result": task.result()}

    return {"task_id": task_id, "status": "in progress"}

@app.post("/cancel/{task_id}")
async def cancel_task(task_id: str):
    """
    �������� ��� ������ ������.

    :param task_id: ������������� ������.
    :return: ������ ������.
    """
    task = tasks.get(task_id)
    if not task:
        return {"task_id": task_id, "status": "not found"}

    if task.done():
        return {"task_id": task_id, "status": "already completed"}

    task.cancel()
    return {"task_id": task_id, "status": "cancelled"}

# ��������� �������� � �������������� Streamlit
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)