import asyncio

from mavsdk import start_mavlink
from mavsdk import connect as mavsdk_connect
from mavsdk import (MissionItem)

import geopy # could replace this with some standard ROS package, (maybe hector_geotiff?)
import geopy.distance

import numpy as np
import mlrose 
np.random.seed(14552)

start_mavlink(connection_url="udp://:14552")
drone = mavsdk_connect(host="127.0.0.1")

# Coordinate part:

N_POINTS = 10
# Define starting point.
origin = geopy.Point(37.331553, -121.882767)
# Define azimuth
SPACE_AZIMUTH = -32

def translate_point(origin, dx, dy): # dx, dy in meters

    dist_x = geopy.distance.geodesic(meters = dx)
    dist_y = geopy.distance.geodesic(meters = dy)
    # move by y
    left_upper = dist_y.destination(point=origin, bearing=SPACE_AZIMUTH)
    # move by x
    dest = dist_x.destination(point=left_upper, bearing=SPACE_AZIMUTH+90)
    return dest

# generate 30 points on campus (the dimensions of campus are 650 x 550m)
points_metric = np.hstack([np.random.rand(N_POINTS,1)*650, np.random.rand(N_POINTS,1)*550])

# convert points from metric to (lat,lon,alt) frame
points_geo = np.array([translate_point(origin, dx, dy) for (dx, dy) in points_metric])

fitness_coords = mlrose.TravellingSales(coords = points_metric)

problem_fit = mlrose.TSPOpt(length = N_POINTS, fitness_fn = fitness_coords, maximize = False)

best_state, best_fitness = mlrose.genetic_alg(problem_fit, mutation_prob = 0.2, max_attempts = 100, random_state = 2)

points_geo = points_geo[best_state]
# Drone part:

async def run():
    mission_items = []

    for p in points_geo:
        mission_items.append(MissionItem(p[0],
                                        p[1],
                                        25,
                                        10,
                                        True,
                                        float('nan'),
                                        float('nan'),
                                        MissionItem.CameraAction.NONE,
                                        float('nan'),
                                        float('nan')))
                                     

    await drone.mission.set_return_to_launch_after_mission(True)

    print("-- Uploading mission")
    await drone.mission.upload_mission(mission_items)

    print("-- Arming")
    await drone.action.arm()

    print("-- Starting mission")
    await drone.mission.start_mission()


async def print_mission_progress():
    async for mission_progress in drone.mission.mission_progress():
        print(f"Mission progress: {mission_progress.current_item_index}/{mission_progress.mission_count}")


async def observe_is_in_air():
    """ Monitors whether the drone is flying or not and
    returns after landing """

    was_in_air = False

    async for is_in_air in drone.telemetry.in_air():
        if is_in_air:
            was_in_air = is_in_air

        if was_in_air and not is_in_air:
            await asyncio.get_event_loop().shutdown_asyncgens()
            return


def setup_tasks():
    asyncio.ensure_future(run())
    asyncio.ensure_future(print_mission_progress())


if __name__ == "__main__":
    setup_tasks()
    asyncio.get_event_loop().run_until_complete(observe_is_in_air())
