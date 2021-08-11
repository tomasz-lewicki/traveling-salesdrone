# Traveling Salesdrone

Showcase of traveling salesman problem on a mavlink drone. Demo video: [https://www.youtube.com/watch?v=jAG2CS-mqwM](https://www.youtube.com/watch?v=jAG2CS-mqwM)


## Description
The program generates random points within given boundaries (here it's SJSU campus).
Then, it looks for the optimal (shortest total distance) order to visit the points (traveling salesman problem).

## Quickstart
1. First, run gazebo simulation. Here, for simplicity it is run in a docker container. You can set the starting location using flags (e.g. ```PX4_HOME_LAT=37.335404```)
```bash
docker run --rm -it --env PX4_HOME_LAT=37.335404 --env PX4_HOME_LON=-121.883400 --env PX4_HOME_ALT=488.0 jonasvautherin/px4-gazebo-headless:v1.9.2
```
2. Run mavproxy to route traffic from simulation to multiple ports
```
mavproxy.py --master=udp:0.0.0.0:14550 --out=udp:localhost:14551 --out=udp:localhost:14552
```

3. Install required packages:
```
pip3 install -r requirements.txt
```

4. Run the program
```
python3 control/mission.py
```

5. Run Qgroundcontrol to observe real-time trajectory of the drone.


## Demo
Below there are non-optimized and optimized flight paths.

Non-optimized:
![non-optimized](/docs/random10points.png)

Optimized ([video](https://www.youtube.com/watch?v=jAG2CS-mqwM), 10x speed):

[![Watch the video](https://img.youtube.com/vi/jAG2CS-mqwM/maxresdefault.jpg)](https://www.youtube.com/watch?v=jAG2CS-mqwM)
