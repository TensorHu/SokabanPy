import json
import pygame
from collections import deque


class LevelStage:
    def __init__(self, level_info):
        self.level_map = self.load_level_map(level_info["level_map"])
        self.player_pos = tuple(level_info["player_pos"])
        self.box_pos_list = [tuple(box) for box in level_info["box_pos_list"]]

    def load_level_map(self, map_file):
        try:
            with open(map_file, 'r') as f:
                level_map = []
                for line in f:
                    level_map.append(list(line.strip()))
                return level_map
        except FileNotFoundError:
            print(f"地图文件 {map_file} 未找到！")
            return []
        except Exception as e:
            print(f"读取地图文件时出错: {e}")
            return []

    def get_map_size(self):
        return len(self.level_map), len(self.level_map[0]) if self.level_map else (0, 0)


class Display:
    def __init__(self, levels):
        self.levels = levels
        self.screen = None
        self.font = None

    def init_window(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Level Input')
        self.font = pygame.font.SysFont("arial", 30)

    def load_level(self, level_id):
        level_info = next((l for l in self.levels if l["level_id"] == level_id), None)
        if level_info:
            self.stage = LevelStage(level_info["level_info"])
            return self.calculate_solution()
        return None

    def calculate_solution(self):
        level_map = self.stage.level_map
        player_pos = self.stage.player_pos
        box_pos_list = self.stage.box_pos_list
        goal_pos = self.find_goal_positions(level_map)

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 右, 下, 左, 上
        direction_names = ['RIGHT', 'DOWN', 'LEFT', 'UP']

        queue = deque([(player_pos, box_pos_list, [])])  # (玩家位置, 箱子位置, 当前路径)
        visited = set()

        while queue:
            current_player_pos, current_box_pos_list, path = queue.popleft()

            if self.is_goal_state(current_box_pos_list, goal_pos):
                return path

            for i, (dx, dy) in enumerate(directions):
                new_player_pos = (current_player_pos[0] + dx, current_player_pos[1] + dy)

                if self.is_valid_move(level_map, new_player_pos, current_box_pos_list):
                    new_box_pos_list = self.move_boxes_if_needed(current_box_pos_list, current_player_pos,
                                                                 new_player_pos)
                    if new_box_pos_list is not None:
                        new_state = (new_player_pos, tuple(new_box_pos_list))
                        if new_state not in visited:
                            visited.add(new_state)
                            queue.append((new_player_pos, new_box_pos_list, path + [direction_names[i]]))

        return []

    def is_goal_state(self, box_pos_list, goal_pos):
        return all(box in goal_pos for box in box_pos_list)

    def is_valid_move(self, level_map, player_pos, box_pos_list):
        x, y = player_pos
        return 0 <= x < len(level_map) and 0 <= y < len(level_map[0]) and level_map[x][y] != 'X'

    def move_boxes_if_needed(self, box_pos_list, player_pos, new_player_pos):
        new_box_pos_list = list(box_pos_list)
        if new_player_pos in box_pos_list:
            box_index = box_pos_list.index(new_player_pos)
            box_pos = box_pos_list[box_index]
            new_box_pos = (box_pos[0] + (new_player_pos[0] - player_pos[0]),
                           box_pos[1] + (new_player_pos[1] - player_pos[1]))

            if self.is_valid_move(self.stage.level_map, new_box_pos, new_box_pos_list):
                new_box_pos_list[box_index] = new_box_pos
            else:
                return None

        return new_box_pos_list

    def find_goal_positions(self, level_map):
        goal_positions = []
        for i in range(len(level_map)):
            for j in range(len(level_map[i])):
                if level_map[i][j] == 'H':
                    goal_positions.append((i, j))
        return goal_positions

    def show_solution(self, level_id):
        solution = self.load_level(level_id)
        return "Level {} Solution: {}".format(level_id, " -> ".join(solution) if solution else "No solution found.")

    def run(self):
        self.init_window()
        input_box = pygame.Rect(100, 100, 140, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            try:
                                level_id = int(text)
                                solution_text = self.show_solution(level_id)
                                self.display_solution(solution_text)
                                text = ''  # 清空输入框文本
                            except ValueError:
                                solution_text = "请输入有效的关卡号"
                                self.display_solution(solution_text)
                                text = ''  # 清空输入框文本
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            self.screen.fill((255, 255, 255))  # 背景色为白色
            txt_surface = self.font.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(self.screen, color, input_box, 2)

            # 显示提示语
            prompt_text = self.font.render("which stage do you need help from 1 to 10(enter to confirm):", True, (0, 0, 0))  # 黑色文字
            self.screen.blit(prompt_text, (100, 60))  # 在输入框上方显示提示语

            pygame.display.flip()
            clock.tick(30)

    def display_solution(self, solution_text):
        # 清空屏幕并显示解决方案
        self.screen.fill((255, 255, 255))  # 背景色为白色
        lines = self.wrap_text(solution_text, self.font, 780)
        y_offset = 150  # 起始y坐标
        for line in lines:
            text_surface = self.font.render(line, True, (0, 0, 0))  # 黑色文字
            self.screen.blit(text_surface, (10, y_offset))  # 左上角位置
            y_offset += 40  # 行间距
        pygame.display.flip()

        # 等待用户按键返回输入
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    waiting = False  # 退出等待状态，返回输入

    def wrap_text(self, text, font, max_width):
        """将文本根据给定的最大宽度换行"""
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:  # 检查宽度
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "

        if current_line:  # 添加最后一行
            lines.append(current_line)

        return lines


def main():
    with open('levelConfig.json', 'r') as f:
        levels = json.load(f)

    display = Display(levels)
    display.run()


if __name__ == "__main__":
    main()
