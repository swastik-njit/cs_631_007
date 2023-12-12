import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

import app.customer_routes as cust_routes
import app.cc_routes as cc_routes
import app.shipping_routes as ship_routes
import app.product_routes as prod_routes
import app.basket_route as shop_basket_routes
import app.transactions_routes as transact_routes
import app.statistics_service as stats_router


tags_metadata = [
    {
        "name": "stats-1",
        "description": "Computing the total amount charged per credit card.",
    },
    {
        "name": "stats-2",
        "description": "Computing the 10 best customers (in terms of money spent) in descending order.",
    },
    {
        "name": "stats-3",
        "description": "For a given time period (begin date and end date) computing the most frequently sold products.",
    },
    {
        "name": "stats-4",
        "description": "For a given time period (begin date and end date) computing the products which are sold to the highest number of distinct customers.",
    },
    {
        "name": "stats-5",
        "description": "For a given time period (begin date and end date) computing the maximum basket total amount per credit card.",
    },
    {
        "name": "stats-6",
        "description": "For a given time period (begin date and end date) computing the average selling product price per product type (desktop, laptop and printer).",
    },
]

description = """
This backend interface focuses on three main applications: 
### 1. customer registration and management 
### 2. online sales 
### 3. collection of statistics 

Please note that many functions are left out in order to reduce the size and the complexity of the project.
"""

app = FastAPI(title="Newark-IT: The Online Computer Store", description=description, openapi_tags=tags_metadata)

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
app.include_router(shop_basket_routes.router, prefix="/api")
app.include_router(transact_routes.router, prefix="/api")
app.include_router(stats_router.router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)


