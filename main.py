from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sympy as sp

BASE = Path(__file__).resolve().parent
app = FastAPI(title="AI Maths Engine", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
x, y = sp.symbols("x y")

class SolveRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return FileResponse(BASE / "index.html")

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "AI Maths Engine"}

@app.post("/api/solve")
def solve(req: SolveRequest):
    q = req.question.strip()
    if not q:
        raise HTTPException(400, "Please enter a maths question.")
    try:
        if "=" in q:
            left, right = q.split("=", 1)
            expr = sp.sympify(left.replace("^", "**")) - sp.sympify(right.replace("^", "**"))
            symbols = sorted(expr.free_symbols, key=str)
            if len(symbols) == 1:
                answers = sp.solve(expr, symbols[0])
                return {"answer": f"Solutions: {', '.join(str(a) for a in answers)}" if answers else "No solution found."}
            if len(symbols) == 2:
                return {"answer": "For simultaneous equations, submit both equations separated by a comma (for example: 2*x+y=7, x-y=1)."}
            return {"answer": str(sp.solve(expr))}
        expr = sp.sympify(q.replace("^", "**"))
        return {"answer": str(sp.simplify(expr))}
    except Exception as exc:
        raise HTTPException(400, f"I couldn't parse that expression. Try standard notation such as 2*x+3=9. Details: {exc}")

if __name__ == "__main__":
    import os, uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
