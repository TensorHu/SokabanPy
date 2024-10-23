# display.py
__author__ = 'Zhewei Hu'

from stage import LevelStage
import pygame

MAX_LEVEL_ID = 10

class Display:
    """
        显示游戏界面的窗口
    """
    def __init__(self):
        self.stage = LevelStage()
        self.init_img_src()
        self.flip = 0

    def init_img_src(self):
        """
            初始化图像素材
        """
        self.player_gif_img_list = [pygame.image.load("./img/player_gif/player_0.png"), pygame.image.load("./img/player_gif/player_1.png")]
        self.aim_pos_img = pygame.image.load("./img/aim_pos.png")
        self.box_img = pygame.image.load("./img/box.png")
        self.box_complete_img = pygame.image.load("./img/box_complete.png")
        self.carpet_img = pygame.image.load("./img/carpet.png")
        self.wall_img = pygame.image.load("./img/wall.png")

    def load_level(self, level_id):
        """
            读取关卡，读取完成后初始化图形界面

            Parameters
            ----------
            level_id : int
                关卡id
        """
        # 读取关卡
        self.stage.load_level(level_id)
        self.grid_size =100
        self.screen_size = (self.stage.get_map_size()[0] * self.grid_size, self.stage.get_map_size()[1] * self.grid_size)
        # 初始化图形界面
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('push box - level %d' % level_id)
        self.main_loop()

    def main_loop(self):
        """
            图形界面的主循环
        """
        self.time_stamp = 0
        self.fps = 60
        self.is_game_win = False
        while True:
            events = pygame.event.get()
            self.flip = (self.flip + 1) % 100
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if not self.is_game_win:
                        if not pygame.key.get_pressed()[pygame.K_UP] and not pygame.key.get_pressed()[
                            pygame.K_LEFT] and not pygame.key.get_pressed()[pygame.K_DOWN] and not \
                        pygame.key.get_pressed()[pygame.K_RIGHT]:
                            pass
                        # 方向键
                        else:
                            if pygame.key.get_pressed()[pygame.K_UP]:
                                direction = 1
                            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                                direction = 2
                            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                                direction = 3
                            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                                direction = 4
                            if self.stage.player_direction_signal_handler(direction=direction):
                                self.game_win()
                        # 撤销
                        if pygame.key.get_pressed()[pygame.K_z]:
                            self.stage.undo()
                        # 重做
                        if pygame.key.get_pressed()[pygame.K_y]:
                            self.stage.redo()
                        # 重开
                        if pygame.key.get_pressed()[pygame.K_r]:
                            self.stage.restart_level()
            # 绘制游戏界面
            self.game_stage_draw()
            pygame.display.update()
            # 更新时间戳
            self.update_time_stamp()

    def update_time_stamp(self):
        pygame.time.delay(int(1e3 / self.fps))
        self.time_stamp += 1
        self.time_stamp = self.time_stamp % self.fps

    def game_stage_draw(self):
        """
            绘制游戏界面
        """
        # 初始化-黑屏
        self.screen.fill((0,0,0))
        # 绘制地毯/墙壁/目标点
        carpet_rect = self.carpet_img.get_rect()
        wall_rect = self.wall_img.get_rect()
        aim_pos_rect = self.aim_pos_img.get_rect()
        level_map = self.stage.level_map
        [level_map_width, level_map_height] = self.stage.get_map_size()
        for i in range(level_map_height):
            for j in range(level_map_width):
                if(level_map[i][j] == 'C'):
                    img_list = [self.carpet_img]
                    rect_list = [carpet_rect]
                elif(level_map[i][j] == "X"):
                    img_list = [self.wall_img]
                    rect_list = [wall_rect]
                elif(level_map[i][j] == "H"):
                    img_list = [self.carpet_img, self.aim_pos_img]
                    rect_list = [carpet_rect, aim_pos_rect]
                else:
                    continue
                centerx = self.grid_size * (0.5 + j)
                centery = self.grid_size * (0.5 + i)
                for img, rect in zip(img_list, rect_list):
                    rect.centerx = centerx
                    rect.centery = centery
                    self.screen.blit(img, rect)
        # 绘制箱子
        box_rect = self.box_img.get_rect()
        box_complete_rect = self.box_complete_img.get_rect()
        for each_box_pos in self.stage.box_pos_list:
            i = each_box_pos[0]
            j = each_box_pos[1]
            centerx = self.grid_size * (0.5 + each_box_pos[1])
            centery = self.grid_size * (0.5 + each_box_pos[0])
            if(level_map[i][j] == 'H'):
                img = self.box_complete_img
                rect = box_complete_rect
            else:
                img = self.box_img
                rect = box_rect
            rect.centerx = centerx
            rect.centery = centery
            self.screen.blit(img, rect)
        # 绘制玩家
        frame = (self.time_stamp % 30) // int(self.fps / 4)
        player_gif_img = self.player_gif_img_list[frame]
        player_gif_rect = player_gif_img.get_rect()
        player_pos = self.stage.player_pos
        centerx = self.grid_size * (0.5 + player_pos[1])
        centery = self.grid_size * (0.5 + player_pos[0])
        player_gif_rect.centerx = centerx
        player_gif_rect.centery = centery
        self.screen.blit(player_gif_img, player_gif_rect)
        # 通关文字显示
        if(self.is_game_win):
            font = pygame.font.SysFont("arial", 100)
            img = font.render('Game Win', True, (0, 100 + self.flip , 0) )
            rect = img.get_rect()
            rect.centerx = self.screen_size[0] / 2
            rect.centery = self.grid_size
            self.screen.blit(img, rect)

    def game_win(self):
        self.is_game_win = True
        self.unlock_new_level()

    def unlock_new_level(self):
        """
            通关，解锁新的一关
        """
        sav_file_path = "./level.sav"
        with open(sav_file_path, "r") as f:
            max_unlock_level = int(f.readline().strip("\n"))
        if(self.stage.level_id == max_unlock_level and max_unlock_level < MAX_LEVEL_ID):
            with open(sav_file_path, "w") as f:
                f.write("%d" % (max_unlock_level+1))
