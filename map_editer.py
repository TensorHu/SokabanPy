import pygame
import sys
import json
import time

class MapEditor:
    """用法：打上 MapEditor（），然后进入循环"""
    def __init__(self):
        # 设置窗口尺寸及相关参数
        W = 1500*0.8
        H = 1000*0.8
        W1 = W * 0.7
        H1 = H * 0.7
        # 读取关卡配置文件
        with open('levelConfig.json', 'r') as file:
            levelConfig = json.load(file)
        level_id = 0
        # 加载各种游戏图像资源
        carpet = pygame.image.load('img/carpet.png')
        box = pygame.image.load('img/box.png')
        box_c = pygame.image.load('img/box_complete.png')
        aim_pos = pygame.image.load('img/aim_pos.png')
        hero = pygame.image.load('img/player_gif/player_0.png')
        wall = pygame.image.load('img/wall.png')
        level_to_select = 1

        # 显示状态
        disp_state = 0
        # 界面状态标志
        interface = 0
        # 初始化 Pygame
        pygame.init()
        # 创建游戏窗口
        screen = pygame.display.set_mode((W, H))
        pygame.display.set_caption("Map Editor")
        # 设置字体
        font1 = pygame.font.SysFont("arial", 33)
        font3 = pygame.font.SysFont("arial", 16)
        font2 = pygame.font.SysFont("arial", 100)
        # 地图的实际宽度和高度
        map_width = 10
        map_height = 10
        # 定义一个函数用于在矩形中显示文本
        def display_text_in_rect(screen, text, rect, color,mode = 0):
            if mode == 0:
                text_surface = font1.render(text, True, color)
            else:
                text_surface = font3.render(text, True, color)
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)

        # 存储关卡数据的初始字典
        data1 = {
            "level_id" : 0,
            "level_info" :
            {
                "level_map" : "level/0.map",
                "player_pos" : [1, 1],
                "box_pos_list" : []
            }
        }
        data = data1.copy()
        wall_ = pygame.transform.scale(wall, (H * 0.1, H * 0.1))
        hero_ = pygame.transform.scale(hero, (H * 0.1, H * 0.1))
        box_ = pygame.transform.scale(box, (H * 0.1, H * 0.1))
        box_c_ = pygame.transform.scale(box_c, (H * 0.1, H * 0.1))
        carpet_ = pygame.transform.scale(carpet, (H * 0.1, H * 0.1))
        aim_pos_ = pygame.transform.scale(aim_pos, (H * 0.1, H * 0.1))
        # 创建各种矩形区域，用于界面交互
        create_rect = pygame.Rect(W * 0.6, H * 0.7, W * 0.2, H * 0.1)
        select_rect = pygame.Rect(W * 0.6, H * 0.55, W * 0.2, H * 0.1)
        stage_rect = pygame.Rect(W * 0.2, H * 0.55, W * 0.2, H * 0.1)
        stage_up_rect = pygame.Rect(W * 0.4, H * 0.55, W * 0.05, H * 0.05)
        stage_down_rect = pygame.Rect(W * 0.4, H * 0.6, W * 0.05, H * 0.05)
        return_rect = pygame.Rect(W * 0.2, H * 0.75, W * 0.15, H * 0.1)
        save_rect = pygame.Rect(W * 0.4, H * 0.75, W * 0.15, H * 0.1)
        # 创建地图矩形列表和显示矩形列表
        map_rect = []
        display_rect = []
        for i in range(0,7):
            display_rect.append(pygame.Rect(W * 0.8, H * 0.11 * (1 + i), H * 0.1, H * 0.1))
        height_rect = pygame.Rect(W * 0.3, H * 0.7, W * 0.15, H * 0.1)
        width_rect = pygame.Rect(W * 0.3, H * 0.8, W * 0.15, H * 0.1)
        # 游戏地图最大高度和宽度
        HEIGHT_max = 16
        WIDTH_max = 16
        # 不同状态下的颜色
        color_unselected = (150, 150, 150)
        color_selected = (250, 255, 250)
        color_selecting = (190, 199, 190)
        # 主循环标志和计数器
        counter1 = 1
        counter2 = 1
        counter3 = 1
        running = True
        #设置帧率
        clock = pygame.time.Clock()
        while running:
            clock.tick(50)
            # 计数器递增
            counter1 = (counter1 + 1) % 255
            counter2 = (counter1 * 2) % 255
            counter3 = (counter3 + 2) % 255
            # 获取鼠标位置和相关事件
            mouse_pos = pygame.mouse.get_pos()
            mouse_l_clicked = 0
            wheel_down = 0
            wheel_up = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_l_clicked = 1
                    if event.button == 4:  # 鼠标滚轮向上滚动
                        wheel_up = 1
                    elif event.button == 5:  # 鼠标滚轮向下滚动
                        wheel_down = 1

            # 显示&修改界面
            if interface == 1:
                screen.fill((0, 0, 0))
                # 统计箱子和目标的数量
                num_box = len(data["level_info"]["box_pos_list"])
                num_aim = 0
                # 遍历地图绘制各种元素
                for y in range(map_height):
                    for x in range(map_width):
                        if map[y][x] == 'X':
                            screen.blit(wall, map_rect[y][x])
                        elif map[y][x] == '0':
                            pygame.draw.rect(screen, (0,2,6), map_rect[y][x])
                        elif map[y][x] == 'C':
                            screen.blit(carpet, map_rect[y][x])
                        elif map[y][x] == 'H':
                            num_aim += 1
                            screen.blit(aim_pos, map_rect[y][x])

                        # 判断鼠标是否在当前地图块上
                        if map_rect[y][x].collidepoint(mouse_pos):
                            c = 0
                            # 检查当前位置是否有箱子或玩家
                            for [y1, x1] in data["level_info"]["box_pos_list"]:
                                if y1 == y and x1 == x:
                                    c = 1
                            if (y == data["level_info"]["player_pos"][0]
                                    and x == data["level_info"]["player_pos"][1]):
                                c = 1
                            # 放置人物，地图块和箱子
                            if mouse_l_clicked == 1:
                                if disp_state == 0:
                                    temp_list = list(map[y])
                                    temp_list[x] = "C"
                                    map[y] = "".join(temp_list)
                                elif disp_state == 1:
                                    if map[y][x] == "C" or map[y][x] == "H":
                                        if c == 0:
                                            data["level_info"]["box_pos_list"].append([y,x])
                                elif disp_state == 2:
                                    if map[y][x] == "C" or map[y][x] == "H"and c == 0:
                                        data["level_info"]["player_pos"] = (y,x)
                                elif disp_state == 3:
                                    if c == 0:
                                        temp_list = list(map[y])
                                        temp_list[x] = "X"
                                        map[y] = "".join(temp_list)
                                elif disp_state == 4:
                                    temp_list = list(map[y])
                                    temp_list[x] = "H"
                                    map[y] = "".join(temp_list)
                                elif disp_state == 5:
                                    if c == 0:
                                        temp_list = list(map[y])
                                        temp_list[x] = "0"
                                        map[y] = "".join(temp_list)
                                elif disp_state == 6:
                                    j = -1
                                    for i in range(0,len(data["level_info"]["box_pos_list"])):
                                        if data["level_info"]["box_pos_list"][i][0] == y:
                                            if data["level_info"]["box_pos_list"][i][1] == x:
                                                j = i
                                    if j!= -1:
                                        del data["level_info"]["box_pos_list"][j]
                # 根据条件绘制玩家和箱子
                if counter1%40 <25:#不同时间内分别显示玩家箱子和地图块
                    y,x =data["level_info"]["player_pos"][0],data["level_info"]["player_pos"][1]
                    screen.blit(hero, map_rect[y][x])
                    for [y,x] in data["level_info"]["box_pos_list"]:
                        screen.blit(box, map_rect[y][x])
                        if map[y][x] == 'H':#箱子放到目标地点了
                            screen.blit(box_c, map_rect[y][x])

                # 绘制目前选中放置选项的标志
                rect_pointer = pygame.Rect(W * 0.79, H * 0.11 * (1 + disp_state), H * 0.03, H * 0.1)
                pygame.draw.rect(screen, (0,20*(counter1%10),0),rect_pointer)
                # 绘制放置选项
                sl = 0
                for i in range(0, 7):
                    if display_rect[i].collidepoint(mouse_pos):
                        if mouse_l_clicked == 1:
                            sl = 1#表示更新放置选项
                            disp_state = i
                    if i == 0:
                        screen.blit(carpet_, display_rect[i])
                    elif i == 1:
                        screen.blit(box_, display_rect[i])
                    elif i == 2:
                        screen.blit(hero_, display_rect[i])
                    elif i == 3:
                        screen.blit(wall_, display_rect[i])
                    elif i == 4:
                        screen.blit(aim_pos_, display_rect[i])
                    elif i == 5:
                        pygame.draw.rect(screen, (40, 40, 40),display_rect[i])
                        display_text_in_rect(screen, "Delete square", display_rect[i], color_unselected,1)
                    elif i == 6:
                        pygame.draw.rect(screen, (40,40,40),display_rect[i])
                        display_text_in_rect(screen, "Delete box", display_rect[i], color_unselected,1)

                # 绘制返回按钮
                pygame.draw.rect(screen, (70, 20, 0), return_rect)
                color = color_unselected
                if return_rect.collidepoint(mouse_pos):
                    color = color_selecting
                    if mouse_l_clicked:
                        interface = 0
                        data = data1.copy()#关卡信息初始化
                display_text_in_rect(screen, "cancel", return_rect, color)

                # 绘制保存按钮
                pygame.draw.rect(screen, (0, 90, 0), save_rect)
                color = color_unselected
                if save_rect.collidepoint(mouse_pos):
                    color = color_selecting
                    if mouse_l_clicked:
                        if num_aim!= num_box:
                            # 如果目标数量和箱子数量不一致，显示提示信息
                            text = font1.render("num of targets!= boxs?c(ﾟ.ﾟ*)｡｡｡", True, (255, 255, 255))
                            screen.blit(text, (W*0.1, H*0.9))
                            pygame.display.flip()
                            time.sleep(0.8)
                        else:
                            #保存信息到文件
                            interface = 0
                            id = data["level_id"]
                            map = '\n'.join([''.join(row) for row in map])
                            if id == len(levelConfig):
                                levelConfig.append(data)
                            else:
                                levelConfig[id] = data
                            with open(f"level/{id}.map", 'w') as file:
                                file.writelines(map)
                            with open('levelConfig.json', 'w') as file:
                                json.dump(levelConfig, file, indent = 4)
                            data = data1.copy()
                display_text_in_rect(screen, "save", save_rect, color)
                pygame.display.update()
                
            # 创建地图块
            if interface == 3:
                interface = 1
                map_rect = [[None] * map_width for _ in range(map_height)]
                w = W1 / map_width
                h = H1 / map_height
                l = min(h,w)
                for y in range(map_height):
                    for x in range(map_width):
                        map_rect[y][x] = pygame.Rect(l*x,l*y, l, l)
                wall = pygame.transform.scale(wall, (l, l))
                hero = pygame.transform.scale(hero, (l, l))
                box = pygame.transform.scale(box, (l, l))
                box_c = pygame.transform.scale(box_c, (l, l))
                carpet = pygame.transform.scale(carpet, (l, l))
                aim_pos = pygame.transform.scale(aim_pos, (l, l))
                
            # 选择关卡后的操作
            if interface == 2:
                # 新建关卡
                if level_to_select == len(levelConfig):
                    data['level_id'] = level_to_select
                    data['level_info']['level_map'] = f"level/{level_to_select}.map"
                    data['level_info']["player_pos"] = [1,1]
                    data["level_info"]['box_pos_list'] = []
                    map = [['X'] * map_width if i == 0 or i == map_height - 1 else ['X'] + ['C'] * (map_width - 2) + ['X'] for
                                i in range(map_height)]
                    interface = 3
                else:
                    # 修改关卡
                    interface = 3
                    data = levelConfig[level_to_select].copy()
                    with open(f"level/{level_to_select}.map", 'r') as file:
                        map = file.read()
                    map = map.split('\n')
                    map_height = len(map)
                    map_width = len(map[0])

            # 关卡选择界面
            if interface == 0:
                screen.fill((0, 0, 0))
                text_surface = font2.render("Map Editor", True, (100+60*(counter1%3), 100+60*(counter1%3), 0))
                screen.blit(text_surface, (W*0.2, H*0.2))
                # 绘制创建地图按钮
                pygame.draw.rect(screen, (0,69,1), create_rect)
                color = color_unselected
                if create_rect.collidepoint(mouse_pos):
                    color = color_selecting
                    if mouse_l_clicked:
                        color = color_selected
                        interface = 2
                        level_to_select = len(levelConfig)
                display_text_in_rect(screen, "create map", create_rect, color)

                # 绘制选择地图按钮
                pygame.draw.rect(screen, (50, 50, 1), select_rect)
                color = color_unselected
                if select_rect.collidepoint(mouse_pos):
                    color = color_selecting
                    if mouse_l_clicked:
                        color = color_selected
                        interface = 2

                display_text_in_rect(screen, "select map", select_rect, color)

                # 绘制关卡选择区域
                pygame.draw.rect(screen, (50, 50, 1), stage_rect)
                color = color_unselected
                if stage_rect.collidepoint(mouse_pos):
                    color = color_selecting
                    if mouse_l_clicked:
                        color = color_selected
                    if wheel_up:
                        level_to_select = (level_to_select + 1) % len(levelConfig)
                        if level_to_select == 0:
                            level_to_select = 1
                    if wheel_down:
                        level_to_select = level_to_select - 1
                        if level_to_select <= 0:
                            level_to_select = len(levelConfig) - 1

                display_text_in_rect(screen, f"stage {level_to_select}", stage_rect, color)
                
                # 绘制上下调整按钮
                pygame.draw.rect(screen, (50, 50, 50), stage_up_rect)
                color = color_unselected
                if stage_up_rect.collidepoint(mouse_pos):
                    color = color_selecting
                    if mouse_l_clicked:
                        level_to_select = (level_to_select + 1) % len(levelConfig)
                        if level_to_select == 0:
                            level_to_select = 1
                display_text_in_rect(screen, f"+", stage_up_rect, color)

                pygame.draw.rect(screen, (50, 50, 50), stage_down_rect)
                color = color_unselected
                if stage_down_rect.collidepoint(mouse_pos):
                    color = color_selecting
                    if mouse_l_clicked:
                        level_to_select = level_to_select - 1
                        if level_to_select <= 0:
                            level_to_select = len(levelConfig) - 1
                display_text_in_rect(screen, f"-", stage_down_rect, color)

                # 绘制高度宽度创建地图按钮
                pygame.draw.rect(screen, (5, 45, 1), height_rect)
                color = color_unselected
                if height_rect.collidepoint(mouse_pos):
                    color = color_selecting
                    if mouse_l_clicked:#鼠标左击
                        color = color_selected
                    if wheel_up:#鼠标上滚
                        map_height = (map_height + 1) % (HEIGHT_max + 1)#设置地图最大高度
                        if map_height == 0:
                            map_height = 5
                    if wheel_down:#鼠标下滚
                        map_height = map_height - 1
                        if map_height <= 4:#设置地图最小高度
                            map_height = HEIGHT_max
                display_text_in_rect(screen, f"height {map_height}", height_rect, color)

                pygame.draw.rect(screen, (5, 45, 1), width_rect)
                color = color_unselected
                if width_rect.collidepoint(mouse_pos):
                    color = color_selecting
                    if mouse_l_clicked:
                        color = color_selected
                    if wheel_up:
                        map_width = (map_width + 1) % (WIDTH_max + 1)#设置地图最大宽度
                        if map_width == 0:
                            map_width = 5
                    if wheel_down:
                        map_width = map_width - 1
                        if map_width <= 4:
                            map_width = HEIGHT_max#设置地图最小宽度
                display_text_in_rect(screen, f"width {map_width}", width_rect, color)

                pygame.display.update()


if __name__ == "__main__":
    MapEditor()
