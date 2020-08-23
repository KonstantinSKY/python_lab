#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d:
    def __init__(self, point):
        self.point = list(point)

    def __add__(self, other):
        return Vec2d((self.point[0] + other.point[0], self.point[1] + other.point[1]))


class Point:
    points_new = []
    diameter = 3
    color = (255, 255, 255)

    def __init__(self, point):
        self.point = Vec2d(point)
        self.speed = Vec2d((random.random(), random.random()))
        self.x = self.point.point[0]
        self.y = self.point.point[1]
        Point.points_new.append(self)
        print(Point.points_new)

    def set(self):
        self.point += self.speed
        self.x = self.point.point[0]
        self.y = self.point.point[1]

        if self.x > SCREEN_DIM[0] or self.x < 0:
            self.speed.point[0] *= -1
        if self.y > SCREEN_DIM[1] or self.y < 0:
            self.speed.point[1] *= -1

    @classmethod
    def set_points(cls):
        """функция перерасчета координат опорных точек"""
        [point.set() for point in cls.points_new]

    @classmethod
    def draw_points(cls, display_obj):
        for point in cls.points_new:
            pygame.draw.circle(display_obj, cls.color, (int(point.x), int(point.y)), cls.diameter)


# class Polyline:
#
#     def __int__(self, point_1, point_2):
#         pass
#
#     @classmethod
#     def draw_lines(cls, display_obj):
#         for point in cls.points_new:
#             pygame.draw.circle(display_obj, cls.color, (int(point.x_point), int(point.y_point)), cls.diameter)


# =======================================================================================
# Функции для работы с векторами
# =======================================================================================

def sub(x, y):
    """"возвращает разность двух векторов"""
    return x[0] - y[0], x[1] - y[1]


def add(x, y):
    """возвращает сумму двух векторов"""
    return x[0] + y[0], x[1] + y[1]


def length(x):
    """возвращает длину вектора"""
    return math.sqrt(x[0] * x[0] + x[1] * x[1])


def mul(v, k):
    """возвращает произведение вектора на число"""
    return v[0] * k, v[1] * k


def vec(x, y):
    """возвращает пару координат, определяющих вектор (координаты точки конца вектора),
    координаты начальной точки вектора совпадают с началом системы координат (0, 0)"""
    return sub(y, x)


# =======================================================================================
# Функции отрисовки
# =======================================================================================
def draw_points(points, style="points", width=3, color=(255, 255, 255)):
    """функция отрисовки точек на экране"""
    if style == "line":
        for p_n in range(-1, len(points) - 1):
            pygame.draw.line(gameDisplay, color,
                             (int(points[p_n][0]), int(points[p_n][1])),
                             (int(points[p_n + 1][0]), int(points[p_n + 1][1])), width)

    elif style == "points":
        for p in points:
            pygame.draw.circle(gameDisplay, color,
                               (int(p[0]), int(p[1])), width)


def draw_help():
    """функция отрисовки экрана справки программы"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# =======================================================================================
# Функции, отвечающие за расчет сглаживания ломаной
# =======================================================================================
def get_point(points, alpha, deg=None):
    if deg is None:
        deg = len(points) - 1
    if deg == 0:
        return points[0]
    return add(mul(points[deg], alpha), mul(get_point(points, alpha, deg - 1), 1 - alpha))


def get_points(base_points, count):
    alpha = 1 / count
    res = []
    for i in range(count):
        res.append(get_point(base_points, i * alpha))
    return res


def get_knot(points, count):
    if len(points) < 3:
        return []
    res = []
    for i in range(-2, len(points) - 2):
        ptn = []
        ptn.append(mul(add(points[i], points[i + 1]), 0.5))
        ptn.append(points[i + 1])
        ptn.append(mul(add(points[i + 1], points[i + 2]), 0.5))

        res.extend(get_points(ptn, count))
    return res


# def set_points(points, speeds):
#     """функция перерасчета координат опорных точек"""
#     for p in range(len(points)):
#         points[p] = add(points[p], speeds[p])
#         if points[p][0] > SCREEN_DIM[0] or points[p][0] < 0:
#             speeds[p] = (- speeds[p][0], speeds[p][1])
#         if points[p][1] > SCREEN_DIM[1] or points[p][1] < 0:
#             speeds[p] = (speeds[p][0], -speeds[p][1])


# =======================================================================================
# Основная программа
# =======================================================================================
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    points = []
    speeds = []
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    points = []
                    speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                points.append(event.pos)
                # print(event.pos)
                #speeds.append((random.random() * 2, random.random() * 2))

                Point(event.pos)
                #print(Vec2d.points_new)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        # draw_points(points)
        Point.draw_points(gameDisplay)

        draw_points(get_knot(points, steps), "line", 3, color)
        if not pause:
            # set_points(points, speeds)  # перерисовываем точки
            Point.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
