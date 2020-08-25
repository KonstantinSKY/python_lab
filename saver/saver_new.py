#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math
from datetime import datetime
import time
from time import sleep

SCREEN_DIM = (800, 600)


class Vec2d:
    def __init__(self, point):
        self.x = point[0]
        self.y = point[1]

    def __add__(self, other):
        return Vec2d((self.x + other.x, self.y + other.y))

    def __mul__(self, other):
        return Vec2d((self.x * other, self.y * other))

    def __sub__(self, other):
        return Vec2d((self.x - other.x, self.y - other.y))

    def length(self):  # """возвращает длину вектора"""
        return math.sqrt(self.x * self.x + self.y * self.y)

    def int_pair(self):
        return self.x, self.y


class Polyline:

    def __init__(self):
        self.bases = []
        self.speeds = []
        self.lines = []
        self.steps = 35
        self.color_bases = (255, 255, 255)
        self.diameter = 3
        self.width = 3

    def add_base_point(self, point):
        self.bases.append(Vec2d(point))
        self.speeds.append(Vec2d((random.random() * 2, random.random() * 2)))
        print(self.bases)
        print(self.speeds)

    def del_base_point(self, del_point):
        del_x = del_point[0]
        del_y = del_point[1]
        for idx, point in enumerate(self.bases):
            if del_x - 3 < point.x < del_x + 3 and del_y - 3 < point.y < del_y + 3:
                del self.bases[idx]

    def set_points(self):
        for idx in range(len(self.bases)):
            self.bases[idx] += self.speeds[idx]

            if self.bases[idx].x > SCREEN_DIM[0] or self.bases[idx].x < 0:
                self.speeds[idx].x *= -1

            if self.bases[idx].y > SCREEN_DIM[1] or self.bases[idx].y < 0:
                self.speeds[idx].y *= -1

    def draw_points(self, display_obj):
        for point in self.bases:
            pygame.draw.circle(display_obj, self.color_bases, (int(point.x), int(point.y)), self.diameter)

    def draw_lines(self, display_obj, color):
        lines = self.lines

        for idx in range(-1, len(lines) - 1):
            pygame.draw.line(display_obj, color, (int(lines[idx].x), int(lines[idx].y)),
                             (int(lines[idx + 1].x), int(lines[idx + 1].y)), self.width)


class Knot(Polyline):

    def __init__(self):
        super().__init__()
        self.smooth_points = []
        self.alpha = 1 / self.steps

    def _get_point(self, alpha, deg=None):

        if deg is None:
            deg = len(self.smooth_points) - 1
        if deg == 0:
            return self.smooth_points[0]

        return (self.smooth_points[deg] * alpha) + (self._get_point(alpha, deg - 1) * (1 - alpha))

    def _get_points(self):
        res = []

        for i in range(self.steps):
            res.append(self._get_point(i * self.alpha))

        return res

    def get_knot(self):
        bases = self.bases

        start_time = datetime.now()

        self.lines = []

        if len(self.bases) < 3:
            return

        for idx in range(-2, len(bases) - 2):
            self.smooth_points = [(bases[idx] + bases[idx + 1]) * 0.5,
                                  bases[idx + 1],
                                  (bases[idx + 1] + bases[idx + 2]) * 0.5
                                  ]
            self.lines.extend(self._get_points())
        print(len(bases))
        print("Full knot", datetime.now() - start_time)


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


class Game:

    def __init__(self, caption):
        self.knots = [Knot()]
        self.working_knot = self.knots[0]
        self.working = True
        self.show_help = False
        self.pause = True
        self.steps = 35
        self.hue = 0
        self.gameDisplay = pygame.display.set_mode(SCREEN_DIM)
        pygame.display.set_caption(caption)
        self.color = pygame.Color(0)

    def work(self):
        while self.working:
            self._event()

            if self.pause:
                self._stop()
            else:
                self._run()

            if self.show_help:
                self._show_help()

            pygame.display.flip()


    def _event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.working = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.working = False

                if event.key == pygame.K_r:
                    pass
                if event.key == pygame.K_p:
                    self.pause = not self.pause
                if event.key == pygame.K_KP_PLUS:
                    self.steps += 1

                if event.key == pygame.K_F1:
                    self.show_help = not self.show_help

                if event.key == pygame.K_KP_MINUS:
                    self.steps -= 1 if self.steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.gameDisplay.fill((0, 0, 0))

                if event.button == 1:
                    self.working_knot.add_base_point(event.pos)

                if event.button == 3 and self.pause:
                    self.working_knot.del_base_point(event.pos)

                self._draw()

    def _draw(self):
        self.working_knot.draw_points(self.gameDisplay)
        self.working_knot.get_knot()
        self.working_knot.draw_lines(self.gameDisplay, self.color)

    def _colorize(self):
        self.hue = (self.hue + 1) % 360
        self.color.hsla = (self.hue, 100, 50, 100)

    def _stop(self):
        self._colorize()
        self.working_knot.draw_lines(self.gameDisplay, self.color)

    def _run(self):
        self.gameDisplay.fill((0, 0, 0))
        self._colorize()

        self.working_knot.set_points()
        self._draw()

    def add_knot(self):
        pass

    def _show_help(self):
        """ Method отрисовки экрана справки программы"""
        self.gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        menu = (("F1", "Show Help"),
                ("R", "Restart"),
                ("P", "Pause/Play"),
                ("Num+", "More points"),
                ("Num-", "Less points"),
                ("", ""),
                (str(self.steps), "Current points"))

        pygame.draw.lines(self.gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)

        for i, text in enumerate(menu):
            self.gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# =======================================================================================
# Основная программа
# =======================================================================================
if __name__ == "__main__":
    pygame.init()
    game = Game("My New Screen Saver")
    game.work()

    # sleep(10)
    # steps = 35
    # working = True
    # points = []
    # speeds = []
    # show_help = False
    # pause = True
    # hue = 0
    #
    # pygame.init()
    # gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    # pygame.display.set_caption("MyScreenSaver")
    # color = pygame.Color(0)
    #
    # K = Knot()
    # while working:
    #
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             working = False
    #
    #         if event.type == pygame.KEYDOWN:
    #
    #             if event.key == pygame.K_ESCAPE:
    #                 working = False
    #             if event.key == pygame.K_r:
    #                 points = []
    #                 speeds = []
    #             if event.key == pygame.K_p:
    #                 pause = not pause
    #             if event.key == pygame.K_KP_PLUS:
    #                 steps += 1
    #             if event.key == pygame.K_F1:
    #                 show_help = not show_help
    #             if event.key == pygame.K_KP_MINUS:
    #                 steps -= 1 if steps > 1 else 0
    #
    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             gameDisplay.fill((0, 0, 0))
    #
    #             if event.button == 1:
    #                 K.add_base_point(event.pos)
    #
    #             if event.button == 3 and pause:
    #                 K.del_base_point(event.pos)
    #
    #             K.draw_points(gameDisplay)
    #             K.get_knot()
    #             K.draw_lines(gameDisplay, color)
    #
    #     if pause:
    #         hue = (hue + 1) % 360
    #         color.hsla = (hue, 100, 50, 100)
    #         K.draw_lines(gameDisplay, color)
    #     else:
    #         gameDisplay.fill((0, 0, 0))
    #         hue = (hue + 1) % 360
    #         color.hsla = (hue, 100, 50, 100)
    #         K.set_points()
    #         K.draw_points(gameDisplay)
    #         K.get_knot()
    #         K.draw_lines(gameDisplay, color)
    #
    #     if show_help:
    #         draw_help()
    #         test()
    #
    #
    #     pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
