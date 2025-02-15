from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse
import os
from llm import generate_steps
from tasks import execute_steps
from utils import resolve_data_path

app = FastAPI()

@app.post("/run")
async def run_task(task: str = Query(...)):
    try:
        steps = generate_steps(task)
        execute_steps(steps)
        return {"status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/read", response_class=PlainTextResponse)
async def read_file(path: str = Query(...)):
    try:
        resolved_path = resolve_data_path(path)
        with open(resolved_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))