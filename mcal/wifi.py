import time

import numpy as np

# TODO complete this file

def init():
    print("Driver Recognition System Initialized")


def get_driver_data_end_point(
        img_arr: np.ndarray,
):
    # Create payload as u want (up to you)

    response = {
        "id": 1,
        "name": "Abbas",
        "phone_num": "123",
        "email": "abc@gmail.com"
    }

    return response


def send_trap_start_flag(
        device_id: int,
        location_long: float,
        location_lat: float,
        action: str = 'start',
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

):
    payload = {
        "device_id": device_id,
        "action": action,
        "timestamp": timestamp,
        "location": {"lat": location_lat, "lng": location_long}
    }

    return None


def send_trap_end_flag(
        device_id: int,
        location_long: float,
        location_lat: float,
        action: str = 'end',
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

):
    payload = {
        "device_id": device_id,
        "action": action,
        "timestamp": timestamp,
        "location": {"lat": location_lat, "lng": location_long}
    }

    return None


def send_sensors_data_end_point(
        device_id: int,
        flame_sensor: bool,
        temperature: float,
        location_long: float,
        location_lat: float,
        rotation_x: float,
        rotation_y: float,
        rotation_z: float,
        trip_active: bool,
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
):
    payload = {
        "device_id": device_id,
        "flame_sensor": flame_sensor,
        "timestamp": timestamp,
        "temperature": temperature,
        "trip_active": trip_active,
        "gyroscope": {"x": rotation_x, "y": rotation_y, "z": rotation_z},
        "location": {
            "lat": location_lat,
            "lng": location_long
        }
    }

    return None  # nothing
