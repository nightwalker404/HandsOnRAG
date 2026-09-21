from fastapi import FastAPI
from contextlib import asynccontextmanager
from
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("start of the project")
        yield
        print("shutdown woth no problem")
    except Exception as e:
        print(f"we can not countinue for there because of the error:\n {e}")

app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    import uvicorn
