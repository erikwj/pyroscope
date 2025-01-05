import os
import time
import pyroscope
from fastapi import FastAPI
from lib.bike.bike import order_bike
from lib.car.car import order_car
from lib.scooter.scooter import order_scooter
from typing import List
from fastapi import Query
from lib.vehicle.vehicle import sort_and_order

pyroscope.configure(
	application_name = "ride-sharing-app",
	server_address   = "http://pyroscope:4040",
	tags             = {
        "region":   f'{os.getenv("REGION")}',
	}
)


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/bike")
def bike():
    order_bike(0.2)
    return "<p>Bike ordered</p>"


@app.get("/scooter")
def scooter():
    order_scooter(0.3)
    return "<p>Scooter ordered</p>"


@app.get("/car")
def car():
    order_car(0.4)
    return "<p>Car ordered</p>"


@app.get("/")
def environment():
    result = "<h1>environment vars:</h1>"
    for key, value in os.environ.items():
        result +=f"<p>{key}={value}</p>"
    return result

@app.get("/vehicles")
def vehicles(isBig: bool, search_terms: List[str] = Query([])):
    sorted_terms = sort_and_order(isBig, search_terms)
    return sorted_terms
