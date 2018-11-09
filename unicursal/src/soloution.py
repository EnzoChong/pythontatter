# -*- coding=utf8 -*-
import sys
from PIL import Image
import numpy
import copy
import time
import random

sys.path.append('../conf')

import default_conf as conf

class Soloution:
    """原始图像"""
    image = None
    """原始图像的数组形式"""
    image_matrix = None
    """原始图像像素点二值化后的数组"""
    image_bin_matrix = None
    
    """方块宽度"""
    block_width = 0
    """方块间隙"""
    space_width = 0
    """地图长宽"""
    map_size = None
    """剩余方块数量"""
    rest_block = 0

    """起点像素坐标"""
    sLocation = None
    """起点地图坐标"""
    sPoint = None
    """地图"""
    gameMap = []
    
    """解集"""
    answer = []

    def __init__(self, fileName):
        self.image = Image.open(fileName).convert(conf.default_image_format)
        self.image_matrix = numpy.array(self.image)
        self.image_bin_matrix = copy.deepcopy(self.image_matrix)

    def _cut_map(self):
        box = [0, 0, self.image.size[0], self.image.size[1]]

        rawBlackCnt = [0] * box[3]
        for raw in xrange(0, box[3]):
            for col in xrange(0, box[2]):
                colour = self.image_matrix[raw, col]
                if colour[0] > conf.rgb_white_pixel_threshold and\
                        colour[1] > conf.rgb_white_pixel_threshold and\
                        colour[2] > conf.rgb_white_pixel_threshold:
                    self.image_matrix[raw, col, :] = conf.rgb_white
                else:
                    self.image_matrix[raw, col, :] = conf.rgb_black
                    rawBlackCnt[raw] += 1
        
        space_line_cnt = 0
        for raw in xrange(0, len(rawBlackCnt)):
            if rawBlackCnt[raw] < conf.hot_pixel_threshold and raw != box[3] - 1:
                self.image_matrix[raw, :, :] = conf.rgb_white
                space_line_cnt += 1
            else:
                if space_line_cnt > conf.interval_threshold:
                    if box[1] == 0:
                        box[1] = raw
                    else:
                        box[3] = raw - space_line_cnt
                space_line_cnt = 0

        space_line_cnt = 0
        for col in xrange(0, box[2]):
            black_cnt = 0
            for raw in xrange(box[1], box[3]):
                if tuple(self.image_matrix[raw, col, :]) == conf.rgb_black_pixel:
                    black_cnt += 1
            if black_cnt < conf.hot_pixel_threshold and col != box[2] - 1:
                self.image_matrix[:, col, :] = conf.rgb_white
                space_line_cnt += 1
            else:
                if space_line_cnt > conf.interval_threshold:
                    if box[0] == 0:
                        box[0] = col
                    else:
                        box[2] = col - space_line_cnt
                space_line_cnt = 0
        self.image = self.image.crop(box)
        self.image_bin_matrix = copy.deepcopy(self.image_matrix[box[1]:box[3], box[0]:box[2]])
        self.image_matrix = numpy.array(self.image)
        return True

    def _map_size(self):
        diff = 10
        offset, len_block, len_space = 0, 0, 0

        for raw in xrange(0, self.image.size[1]):
            if tuple(self.image_bin_matrix[raw, 0]) == conf.rgb_black_pixel:
                while tuple(self.image_bin_matrix[raw, len_block]) == conf.rgb_black_pixel:
                    len_block += 1
                while len_space == 0 or len_space > len_block:
                    len_space = 0
                    while tuple(self.image_bin_matrix[raw, offset + len_block + len_space]) == conf.rgb_white_pixel:
                        len_space += 1
                    offset = len_block + len_space
                break
        self.block_width = len_block
        self.space_width = len_space
        step = len_block + len_space
        self.map_size = (self.image.size[0] / step + 1, self.image.size[1] / step +1)

    def _distinguishGameMap(self):
        gameMap = []
        size = self.image.size
        step = self.block_width + self.space_width
        test_cnt = 0
        for raw in xrange(0, size[1], step):
            line = []
            for col in xrange(0, size[0], step):
                cRaw = (self.block_width / 2) + raw
                cCol = (self.block_width / 2) + col
                cPixel = self.image_matrix[cRaw, cCol]
                if (cPixel[0] in conf.rgb_block) and (cPixel[1] in conf.rgb_block) and (cPixel[2] in conf.rgb_block):
                    line.append(1)
                    self.rest_block += 1
                elif cPixel[0] >= conf.rgb_white_pixel_threshold and\
                        cPixel[1] >= conf.rgb_white_pixel_threshold and\
                        cPixel[2] >= conf.rgb_white_pixel_threshold:
                    line.append(0)
                else:
                    self.sLocation = (cRaw, cCol)
                    self.sPoint = (cRaw / step, cCol / step)
                    line.append(0)
            gameMap.append(line)
        self.gameMap = gameMap

    def _solve_answer_once(self, gameMap, sRaw, sCol, ins, rest, ans):
        if rest == 0:
            ans.append(ins[:])

        if (sRaw != 0 and gameMap[sRaw - 1][sCol]):
            ins.append(conf.answer_ins_up)
            gameMap[sRaw - 1][sCol] = 0
            self._solve_answer_once(gameMap, sRaw - 1, sCol, ins, rest - 1, ans)
            ins.pop()
            gameMap[sRaw - 1][sCol] = 1

        if (sCol != 0 and gameMap[sRaw][sCol - 1]):
            ins.append(conf.answer_ins_left)
            gameMap[sRaw][sCol - 1] = 0
            self._solve_answer_once(gameMap, sRaw, sCol - 1, ins, rest - 1, ans)
            ins.pop()
            gameMap[sRaw][sCol - 1] = 1

        if (sRaw != len(gameMap) - 1 and gameMap[sRaw + 1][sCol]):
            ins.append(conf.answer_ins_down)
            gameMap[sRaw + 1][sCol] = 0
            self._solve_answer_once(gameMap, sRaw + 1, sCol, ins, rest - 1, ans)
            ins.pop()
            gameMap[sRaw + 1][sCol] = 1

        if (sCol != len(gameMap[0]) - 1 and gameMap[sRaw][sCol + 1]):
            ins.append(conf.answer_ins_right)
            gameMap[sRaw][sCol + 1] = 0
            self._solve_answer_once(gameMap, sRaw, sCol + 1, ins, rest - 1, ans)
            ins.pop()
            gameMap[sRaw][sCol + 1] = 1

    def _solve_answer(self):
        self._solve_answer_once(self.gameMap, self.sPoint[0], self.sPoint[1], [], self.rest_block, self.answer)

    def _draw_ans_once(self, ans):
        sRaw, sCol = self.sLocation
        step = self.block_width + self.space_width
        image = copy.deepcopy(self.image_matrix)
        w = conf.answer_line_width / 2
        for ins in ans:
            image[sRaw - w :sRaw + w, sCol - w: sCol + w, :] = 0
            if ins == conf.answer_ins_up:
                image[sRaw - step:sRaw - w, sCol - w:sCol + w, :] = 0
                sRaw -= step
            elif ins == conf.answer_ins_down:
                image[sRaw + w:sRaw + step, sCol - w:sCol + w, :] = 0
                sRaw += step
            elif ins == conf.answer_ins_left:
                image[sRaw - w:sRaw + w, sCol - step:sCol - w, :] = 0
                sCol -= step
            else:
                image[sRaw - w:sRaw + w, sCol + w:sCol + step, :] = 0
                sCol += step
        image_id = str(int(time.time()) + random.randint(0, 10))
        fileName = conf.answer_image_save_path + image_id + '.' + conf.answer_image_save_format
        Image.fromarray(image).convert(conf.default_image_format).save(fileName, conf.answer_image_save_format)
        return image_id

    def draw_answer(self):
        if len(self.answer) != 0:
            return self._draw_ans_once(self.answer[0])

    def analyse(self):
        self._cut_map()
        self._map_size()
        self._distinguishGameMap()
        self._solve_answer()

if __name__ == '__main__':
    print "ok"
