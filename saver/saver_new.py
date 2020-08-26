#!/usr/bin/env python3

import pygame
import random
import math


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

    def length(self):
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

    def increase_speed(self):
        for idx in range(len(self.speeds)):
            self.speeds[idx] *= 1.1

    def decrease_speed(self):
        for idx in range(len(self.speeds)):
            self.speeds[idx] *= 0.9


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

        self.lines = []

        if len(self.bases) < 3:
            return

        for idx in range(-2, len(bases) - 2):
            self.smooth_points = [(bases[idx] + bases[idx + 1]) * 0.5,
                                  bases[idx + 1],
                                  (bases[idx + 1] + bases[idx + 2]) * 0.5
                                  ]
            self.lines.extend(self._get_points())


class Game:

    def __init__(self, caption):
        self.knots = [Knot()]
        self.work_idx = 0
        self.calc_knot = None
        self.working = True
        self.show_help = False
        self.screen_help = False
        self.pause = True
        self.steps = 35
        self.hue = 0
        self.gameDisplay = pygame.display.set_mode(SCREEN_DIM)
        self.caption = caption
        self._set_caption()
        self.color = pygame.Color(0)

    def _set_caption(self):
        pygame.display.set_caption(f"{self.caption} Knot # {self.work_idx + 1} from {len(self.knots)}")

    def work(self):
        while self.working:
            self._event()

            if self.show_help:
                self._show_help()
                pygame.display.flip()
                continue

            if self.pause:
                self._stop()
            else:
                self._run()

            pygame.display.flip()

    def _event(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.working = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.working = False
                    break
                if event.key == pygame.K_F1:
                    self.show_help = not self.show_help
                    if not self.show_help:
                        self.screen_help = False
                        self._run()
                    break
                if event.key == pygame.K_r:
                    self.knots = [Knot()]

                if event.key == pygame.K_p:
                    self.pause = not self.pause

                if event.key == pygame.K_LEFT:
                    self.knots[self.work_idx].decrease_speed()
                if event.key == pygame.K_RIGHT:
                    self.knots[self.work_idx].increase_speed()

                if event.key == pygame.K_a:
                    self.knots.append(Knot())
                    self.work_idx = len(self.knots) - 1
                    self._set_caption()

                if event.key == pygame.K_c:
                    self._set_caption()

                    self.work_idx = self.work_idx + 1 if self.work_idx < len(self.knots) - 1 else 0
                    self._set_caption()

                if event.key == pygame.K_KP_PLUS:
                    self.knots[self.work_idx].steps += 1

                if event.key == pygame.K_KP_MINUS:
                    self.knots[self.work_idx].steps -= 1 if self.knots[self.work_idx].steps > 1 else 0

            self.screen_help = False
            if self.screen_help:
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.gameDisplay.fill((0, 0, 0))

                if event.button == 1:
                    self.knots[self.work_idx].add_base_point(event.pos)

                if event.button == 3 and self.pause:
                    self.knots[self.work_idx].del_base_point(event.pos)

                self._draw()

    def _draw(self):
        for idx in range(len(self.knots)):
            self.knots[idx].draw_points(self.gameDisplay)
            self.knots[idx].get_knot()
            self.knots[idx].draw_lines(self.gameDisplay, self.color)

    def _colorize(self):
        self.hue = (self.hue + 1) % 360
        self.color.hsla = (self.hue, 100, 50, 100)

    def _stop(self):

        for idx in range(len(self.knots)):
            self._colorize()
            self.knots[idx].draw_lines(self.gameDisplay, self.color)

    def _run(self):
        self.gameDisplay.fill((0, 0, 0))

        for idx in range(len(self.knots)):
            self._colorize()
            self.knots[idx].set_points()
        self._draw()

    def _show_help(self):
        if self.screen_help:
            return

        self.gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        menu = (("F1", "Show Help"),
                ("R", "Restart"),
                ("P", "Pause/Play"),
                ("Left mouse bottom", "Add new point for working Knot"),
                ("Right mouse bottom", "Delete point for working Knot"),
                ("A", "Add new Knot"),
                ("C", "Change working Knot"),
                ("<- left", "Decrease speed for selected Knot"),
                ("-> right", "Increase speed for selected Knot"),
                ("Num+", "More points"),
                ("Num-", "Less points"),
                ("", ""),
                (str(len(self.knots)), "Knots in system"),
                (str(self.work_idx + 1), "Working Knots number"),
                (str(self.knots[self.work_idx].steps), "Current points in working Knots"))

        pygame.draw.lines(self.gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)

        for i, text in enumerate(menu):
            self.gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (50, 100 + 30 * i))
            self.gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (350, 100 + 30 * i))

        self.screen_help = True


# =======================================================================================
# Основная программа
# =======================================================================================
if __name__ == "__main__":
    SCREEN_DIM = (800, 600)
    pygame.init()
    game = Game(f"My Screen Saver. ")
    game.work()
    pygame.display.quit()
    pygame.quit()
    exit(0)
