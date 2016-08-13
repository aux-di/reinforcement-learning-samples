# -*- coding: utf-8 -*-

import time
import random
import numpy as np
import cv2

class Maze():

    def __init__(self):
        self.maze = [[3, 3, 3, 3, 3, 3, 3, 3],
                     [3, 1, 0, 0, 0, 0, 0, 3],
                     [3, 0, 3, 0, 3, 0, 0, 3],
                     [3, 0, 0, 0, 3, 0, 0, 3],
                     [3, 0, 0, 0, 0, 0, 2, 3],
                     [3, 3, 3, 3, 3, 3, 3, 3]]    # 0:aisle, 1:start, 2:goal, 3:wall
        self.maze_size = (len(self.maze[0]), len(self.maze)) # x, y
        self.unit_size = 60
        self.width = self.unit_size * self.maze_size[0]
        self.height = self.unit_size * self.maze_size[1]
        self.img = np.zeros((self.height, self.width, 3), np.uint8)  # all black

        # draw maze
        for y in range(self.maze_size[1]):
            for x in range(self.maze_size[0]):
                self.drawUnit(x, y)

    def drawUnit(self, x, y, now = 0):
        start = (self.unit_size * x, self.unit_size * y)
        end = (start[0] + self.unit_size, start[1] + self.unit_size)

        if self.maze[y][x] == 1:
            cv2.rectangle(self.img, start, end, (255, 255, 255), -1)
        elif self.maze[y][x] == 2:
            cv2.rectangle(self.img, start, end, (255, 0, 0), -1)
        elif self.maze[y][x] == 3:
            cv2.rectangle(self.img, start, end, (128, 128, 128), -1)
        else:
            cv2.rectangle(self.img, start, end, (0, 0, 0), -1)
            cv2.rectangle(self.img, start, end, (128, 128, 128), 1)

        if now == 1:
            cv2.rectangle(self.img, start, end, (255, 255, 255), -1)

    def update(self, position, new_position):

        y, x = position
        newy, newx = new_position

        self.drawUnit(x, y)
        self.drawUnit(newx, newy, 1)

class Agent():

    def __init__(self, maze):
        self.q_value = []
        self.alpha = 0.2
        self.gamma = 0.9
        self.epsilon = 0.8
        self.maze = maze.maze
        self.reward = 1

        for y in range(maze.maze_size[1]):
            q = []
            for x in range(maze.maze_size[0]):
                q.append(np.array([0., 0., 0., 0.]))    # top, right, bottom, left

            self.q_value.append(q)

    def action(self, position):

        y, x = position
        r = random.random()
        m = max(self.q_value[y][x])

        if r > self.epsilon or m == 0:
            direction = random.randint(0, 3)
        else:
            direction = np.argmax(self.q_value[y][x])

        return self.next_position(position, direction)

    def next_position(self, position, direction):

        y, x = position
        wall = 0
        next_position = position

        if direction == 0:
            if self.maze[y - 1][x] == 3:
                wall = 1
            else:
                next_position = [y - 1, x]

        elif direction == 1:
            if self.maze[y][x + 1] == 3:
                wall = 1
            else:
                next_position = [y, x + 1]

        elif direction == 2:
            if self.maze[y + 1][x] == 3:
                wall = 1
            else:
                next_position = [y + 1, x]

        elif direction == 3:
            if self.maze[y][x - 1] == 3:
                wall = 1
            else:
                next_position = [y, x - 1]

        if wall == 0:
            self.update_q_value(position, next_position, direction)

        newy, newx = next_position

        if self.maze[newy][newx] == 2:
            next_position = [1, 1]
            print self.q_value[y][x]
            cv2.waitKey(0)

        print direction, next_position

        return next_position

    def update_q_value(self, position, next_position, direction):
        y, x = position
        newy, newx = next_position
        d = direction

        if self.maze[newy][newx] == 2:
            reward = self.reward
        else:
            reward = 0

        self.q_value[y][x][d] = self.q_value[y][x][d] + self.alpha * (reward + self.gamma * max(self.q_value[y][x]) - self.q_value[y][x][d])

def main():

    maze = Maze()
    agent = Agent(maze)

    position = [1, 1]   # y, x

    cv2.imshow('image', maze.img)

    for i in range(16000):

        new_position = agent.action(position)
        maze.update(position, new_position)

        cv2.imshow('image', maze.img)
        cv2.waitKey(3)

        position = new_position

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
