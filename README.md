# Документация к приложению

## Описание проекта

Приложение позволяет обрабатывать изображения с помощью OCR (оптического распознавания текста). Оно предоставляет API для загрузки изображений, выполнения распознавания текста и получения результатов. Приложение состоит из двух частей:

- **Backend** на базе FastAPI.
- **Frontend** на базе Streamlit для взаимодействия с пользователем.

---

## Структура проекта

**Файлы проекта:**

- `main.py` — Backend-приложение (FastAPI).
- `streamlit_app.py` — Frontend-приложение (Streamlit).
- `requirements.txt` — Список необходимых библиотек.

---

## Основные эндпоинты FastAPI

### POST `/process`

**Описание:** Загружает изображение и инициирует процесс OCR.

**Параметры:**

- `file` (формат: jpg/png/jpeg/tiff) — файл изображения.
- `lang` (по умолчанию: rus+eng) — язык для OCR.

**Ответ:** Возвращает `task_id` для отслеживания задачи.

### GET `/status/{task_id}`

**Описание:** Проверяет статус выполнения задачи OCR.

**Параметры:**

- `task_id` — ID задачи, возвращаемый эндпоинтом `/process`.

**Ответ:** Возвращает текущий статус задачи (`work`, `done`, `cancelled`) и результат OCR, если задача завершена.

### POST `/cancel/{task_id}`

**Описание:** Отменяет задачу OCR.

**Параметры:**

- `task_id` — ID задачи.

**Ответ:** Статус задачи после отмены.

---

## Установка и запуск приложения

### Шаг 1: Клонирование репозитория
Склонируйте проект из репозитория:
```bash
git clone https://github.com/Za1cevMaksim/API_TRec
```
---

### Шаг 2: Установите зависимости

Создайте виртуальное окружение и активируйте его:

```bash
python -m venv venv
venv\Scripts\activate
```
Установите зависимости из requirements.txt:

```bash
pip install -r requirements.txt
```

---

### Шаг 3: Убедитесь в наличии Tesseract-OCR

Убедитесь, что Tesseract установлен на вашем компьютере:

#### Windows:

Скачайте Tesseract [отсюда](https://github.com/tesseract-ocr/tesseract).
Добавьте путь к исполняемому файлу Tesseract в переменную окружения PATH.

#### Linux:
```bash
sudo apt install tesseract-ocr 
```

---

### Шаг 4: Запустите Backend

```bash
uvicorn main:app --reload
```

Приложение FastAPI запустится по адресу: http://127.0.0.1:8000.

Документация к API доступна по адресу: http://127.0.0.1:8000/docs.

---

### Шаг 5: Запустите Frontend


```bash
streamlit run frontend.py
```
Приложение Streamlit будет доступно по адресу: http://127.0.0.1:8501.
