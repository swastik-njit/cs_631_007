import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

import app.customer_routes as cust_routes
import app.cc_routes as cc_routes
import app.shipping_routes as ship_routes
import app.product_routes as prod_routes
import app.orders_routes as order_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')


app.include_router(cust_routes.router, prefix="/api")
app.include_router(cc_routes.router, prefix="/api")
app.include_router(ship_routes.router, prefix="/api")
app.include_router(prod_routes.router, prefix="/api")
app.include_router(order_routes.router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)


