
# VisionMaze

VisionMaze is a maze-solving application developed in Python, utilizing the power of numpy and OpenCV packages. The project aims to generate mazes and deploy various path-finding algorithms to find the shortest path from a given starting point to a destination within the maze or another map's image.

## Features

• Generate random mazes or select pre-processed maps.\
• Implement five different path-finding algorithms on them:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Breadth-first search\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Depth-first search\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Best-first search (Greedy)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Dijkstra's algorithm\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• A* algorithm\
• Maintain a log of the path length and execution time for each algorithm.\
• Visualize the path-finding algorithms and path found by them using OpenCV.

## Run Locally

Clone the project

```bash
  git clone https://github.com/aryangoenka26/VisionMaze
```

Go to the project directory

```bash
  cd VisionMaze
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python runner.py
```


## Note
To close any image or to exit any path finding process midway press “q” on keyboard.

