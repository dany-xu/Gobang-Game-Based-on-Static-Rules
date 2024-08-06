from env.gobang import GoBang
from env.obs_interfaces.observation import *
from env.simulators.gridgame import GridGame
class Robot(object):
    '''基于五子棋规则写的一个机器人'''

    def __init__(self, _board):
        self.board = _board

    def haveValuePoints(self, player, enemy, board):
        """算出棋盘中所有有价值的点"""
        points = []

        for x in range(15):
            for y in range(15):
                list1 = []
                list2 = []
                list3 = []
                list4 = []
                if self.board[x][y] == 0:
                    for tmp in range(9):
                        i = x + tmp - 4
                        j = y + tmp - 4
                        # 搜索的范围是x,y的周围8×8的空间
                        if i < 0 or i > 14:
                            list1.append(-1)
                        else:
                            list1.append(board[i][y])
                        if j < 0 or j > 14:
                            list2.append(-1)
                        else:
                            list2.append(board[x][j])
                        if i < 0 or j < 0 or i > 14 or j > 14:
                            list3.append(-1)
                        else:
                            list3.append(board[i][j])
                        k = y - tmp + 4
                        if i < 0 or k < 0 or i > 14 or k > 14:
                            list4.append(-1)
                        else:
                            list4.append(board[i][k])

                    player_score = self.value_point(player, enemy, list1, list2, list3, list4)
                    enemy_score = self.value_point(enemy, player, list1, list2, list3, list4)
                    if enemy_score >= 10000:
                        enemy_score -= 500
                    elif enemy_score >= 5000:
                        enemy_score -= 300
                    elif enemy_score >= 2000:
                        enemy_score -= 250
                    elif enemy_score >= 1500:
                        enemy_score -= 200
                    elif enemy_score >= 99:
                        enemy_score -= 10
                    elif enemy_score >= 5:
                        enemy_score -= 1
                    value = player_score + enemy_score
                    if value > 0:
                        points.append([x, y, value])
        #print("list1:",list1)
        #print("list2:", list2)
        #print("list3:", list3)
        #print("list4:", list4)
        return points

    def MaxValue_po(self, player, enemy):
        """算出最大价值的点，先求取有价值点，再求其中的最大价值点。"""
        '''
        if player==2 and enemy==1:
            player=1
            enemy=0
        elif player==1 and enemy==2:
            player = 0
            enemy = 1
        '''
        points = self.haveValuePoints(player, enemy, self.board)
        print(self.board)
        #print("points:", points)
        flag = 0
        _point = []
        for p in points:
            if p[2] > flag:
                _point = p
                flag = p[2]
        #如果棋盘上还没有棋子
        if len(_point)==0:
            _point.append(7)
            _point.append(7)
            _point.append(99)
        #print("_point:",_point)
        return _point[0], _point[1], _point[2]  # 返回x，y，value

    def value_point(self, player, enemy, list1, list2, list3, list4):
        """算出点的价值"""
        flag = 0
        flag += self.five(player, list1)
        flag += self.five(player, list2)
        flag += self.five(player, list3)
        flag += self.five(player, list4)
        flag += self.alive4(player, list1)
        flag += self.alive4(player, list2)
        flag += self.alive4(player, list3)
        flag += self.alive4(player, list4)
        flag += self.sleep4(player, enemy, list1)
        flag += self.sleep4(player, enemy, list2)
        flag += self.sleep4(player, enemy, list3)
        flag += self.sleep4(player, enemy, list4)
        flag += self.alive3(player, list1)
        flag += self.alive3(player, list2)
        flag += self.alive3(player, list3)
        flag += self.alive3(player, list4)
        flag += self.sleep3(player, enemy, list1)
        flag += self.sleep3(player, enemy, list2)
        flag += self.sleep3(player, enemy, list3)
        flag += self.sleep3(player, enemy, list4)
        flag += self.alive2(player, enemy, list1)
        flag += self.alive2(player, enemy, list2)
        flag += self.alive2(player, enemy, list3)
        flag += self.alive2(player, enemy, list4)
        flag += self.sleep2(player, enemy, list1)
        flag += self.sleep2(player, enemy, list2)
        flag += self.sleep2(player, enemy, list3)
        flag += self.sleep2(player, enemy, list4)
        return flag

    @staticmethod
    def five(player, compare):
        """下在这个点将会得到连五"""
        if compare[0] == player and compare[1] == player and \
                compare[2] == player and compare[3] == player:
            return 10000
        elif compare[5] == player and compare[6] == player and \
                compare[7] == player and compare[8] == player:
            return 10000
        elif compare[2] == player and compare[3] == player and \
                compare[5] == player and compare[6] == player:
            return 10000
        elif compare[1] == player and compare[2] == player and \
                compare[3] == player and compare[5] == player:
            return 10000
        elif compare[3] == player and compare[5] == player and \
                compare[6] == player and compare[7] == player:
            return 10000
        else:
            return 0

    @staticmethod
    def alive4(player, compare):
        """下在这个点将会形成活四"""
        if compare[0] == 0 and compare[1] == player and \
                compare[2] == player and compare[3] == player \
                and compare[5] == 0:
            return 5000
        elif compare[3] == 0 and compare[5] == player and \
                compare[6] == player and compare[7] == player \
                and compare[8] == 0:
            return 5000
        elif compare[1] == 0 and compare[2] == player and \
                compare[3] == player and compare[5] == player \
                and compare[6] == 0:
            return 5000
        elif compare[2] == 0 and compare[3] == player and \
                compare[5] == player and compare[6] == player \
                and compare[7] == 0:
            return 5000
        else:
            return 0

    @staticmethod
    def sleep4(player, enemy, compare):
        """下在这个点会形成眠四"""
        if compare[0] == enemy and compare[1] == player and \
                compare[2] == player and compare[3] == player \
                and compare[5] == 0:
            return 1700
        elif compare[1] == enemy and compare[2] == player and \
                compare[3] == player and compare[5] == player \
                and compare[6] == 0:
            return 1700
        elif compare[2] == enemy and compare[3] == player and \
                compare[5] == player and compare[6] == player \
                and compare[7] == 0:
            return 1700
        elif compare[3] == enemy and compare[5] == player and \
                compare[6] == player and compare[7] == player \
                and compare[8] == 0:
            return 1700
        elif compare[0] == 0 and compare[1] == player and \
                compare[2] == player and compare[3] == player \
                and compare[5] == enemy:
            return 1700
        elif compare[1] == 0 and compare[2] == player and \
                compare[3] == player and compare[5] == player \
                and compare[6] == enemy:
            return 1700
        elif compare[2] == 0 and compare[3] == player and \
                compare[5] == player and compare[6] == player \
                and compare[7] == enemy:
            return 1700
        elif compare[3] == 0 and compare[5] == player and \
                compare[6] == player and compare[7] == player \
                and compare[8] == enemy:
            return 1700
        else:
            return 0

    @staticmethod
    def alive3(player, compare):
        """下在这个点会形成活三"""
        if compare[0] == 0 and compare[1] == 0 and \
                compare[2] == player and compare[3] == player \
                and compare[5] == 0:
            return 1900
        elif compare[1] == 0 and compare[2] == 0 and \
                compare[3] == player and compare[5] == player \
                and compare[6] == 0:
            return 1900
        elif compare[2] == 0 and compare[3] == 0 and \
                compare[5] == player and compare[6] == player \
                and compare[7] == 0:
            return 1900
        elif compare[1] == 0 and compare[2] == player and \
                compare[3] == player and compare[5] == 0 \
                and compare[6] == 0:
            return 1900
        elif compare[2] == 0 and compare[3] == player and \
                compare[5] == player and compare[6] == 0 \
                and compare[7] == 0:
            return 1900
        elif compare[3] == 0 and compare[5] == player and \
                compare[6] == player and compare[7] == 0 \
                and compare[8] == 0:
            return 1900
        elif compare[0] == 0 and compare[1] == player and \
                compare[2] == player and compare[3] == 0 \
                and compare[5] == 0:
            return 1600
        elif compare[2] == 0 and compare[3] == player and \
                compare[6] == player and compare[5] == 0 \
                and compare[7] == 0:
            return 1600
        elif compare[3] == 0 and compare[5] == player and \
                compare[7] == player and compare[6] == 0 \
                and compare[8] == 0:
            return 1600
        elif compare[3] == 0 and compare[5] == 0 and \
                compare[7] == player and compare[6] == player \
                and compare[8] == 0:
            return 1600
        elif compare[0] == 0 and compare[1] == player and \
                compare[2] == player and compare[3] == 0 \
                and compare[6] == 0:
            return 1600
        elif compare[0] == 0 and compare[1] == player and \
                compare[2] == player and compare[3] == 0 \
                and compare[6] == 0:
            return 1600
        else:
            return 0

    @staticmethod
    def sleep3(player, enemy, compare):
        """下在这个点会形成眠三"""
        if compare[1] == enemy and compare[2] == player and \
                compare[3] == player and compare[5] == 0 \
                and compare[6] == 0:
            return 350
        elif compare[2] == enemy and compare[3] == player and \
                compare[5] == player and compare[6] == 0 \
                and compare[7] == 0:
            return 350
        elif compare[3] == enemy and compare[5] == player and \
                compare[6] == player and compare[7] == 0 \
                and compare[8] == 0:
            return 350
        elif compare[0] == 0 and compare[1] == 0 and \
                compare[2] == player and compare[3] == player \
                and compare[5] == enemy:
            return 350
        elif compare[1] == 0 and compare[2] == 0 and \
                compare[3] == player and compare[5] == player \
                and compare[6] == enemy:
            return 350
        elif compare[2] == 0 and compare[3] == 0 and \
                compare[5] == player and compare[6] == player \
                and compare[7] == enemy:
            return 350
        elif compare[0] == enemy and compare[1] == 0 and \
                compare[2] == player and compare[3] == player \
                and compare[5] == 0 and compare[6] == enemy:
            return 300
        elif compare[1] == enemy and compare[2] == 0 and \
                compare[3] == player and compare[5] == player \
                and compare[6] == 0 and compare[7] == enemy:
            return 300
        elif compare[2] == enemy and compare[3] == 0 and \
                compare[5] == player and compare[6] == player \
                and compare[7] == 0 and compare[8] == enemy:
            return 300
        elif compare[0] == enemy and compare[1] == player and \
                compare[2] == 0 and compare[3] == player \
                and compare[5] == 0 and compare[6] == enemy:
            return 300
        elif compare[1] == enemy and compare[2] == player and \
                compare[3] == 0 and compare[5] == player \
                and compare[6] == 0 and compare[7] == enemy:
            return 300
        elif compare[2] == enemy and compare[3] == player and \
                compare[5] == 0 and compare[6] == player \
                and compare[7] == 0 and compare[8] == enemy:
            return 300
        elif compare[0] == enemy and compare[1] == player and \
                compare[2] == 0 and compare[3] == player \
                and compare[5] == 0 and compare[6] == enemy:
            return 300
        elif compare[1] == enemy and compare[2] == player and \
                compare[3] == 0 and compare[5] == player \
                and compare[6] == 0 and compare[7] == enemy:
            return 300
        elif compare[3] == enemy and compare[5] == 0 and \
                compare[6] == player and compare[7] == player \
                and compare[8] == 0:
            return 300
        elif compare[0] == enemy and compare[1] == player and \
                compare[2] == player and compare[3] == 0 \
                and compare[5] == 0:
            return 300
        elif compare[2] == enemy and compare[3] == player and \
                compare[5] == 0 and compare[6] == player \
                and compare[7] == 0:
            return 300
        elif compare[3] == enemy and compare[5] == player and \
                compare[6] == 0 and compare[7] == player \
                and compare[8] == 0:
            return 300
        elif compare[0] == player and compare[1] == player and \
                compare[2] == 0 and compare[3] == 0 \
                and compare[5] == enemy:
            return 300
        elif compare[2] == enemy and compare[3] == player and \
                compare[5] == 0 and compare[6] == 0 \
                and compare[7] == player:
            return 300
        elif compare[3] == enemy and compare[5] == player and \
                compare[6] == 0 and compare[7] == 0 \
                and compare[8] == player:
            return 300
        elif compare[0] == player and compare[1] == 0 and \
                compare[2] == 0 and compare[3] == player \
                and compare[5] == enemy:
            return 300
        elif compare[1] == player and compare[2] == 0 and \
                compare[3] == 0 and compare[5] == player \
                and compare[6] == enemy:
            return 300
        elif compare[3] == enemy and compare[5] == 0 and \
                compare[6] == 0 and compare[7] == player \
                and compare[8] == player:
            return 300
        elif compare[0] == 0 and compare[1] == player and \
                compare[2] == player and compare[3] == 0 \
                and compare[5] == enemy:
            return 30
        elif compare[2] == 0 and compare[3] == player and \
                compare[5] == 0 and compare[6] == player \
                and compare[7] == enemy:
            return 300
        elif compare[3] == 0 and compare[5] == player and \
                compare[6] == 0 and compare[7] == player \
                and compare[8] == enemy:
            return 300
        elif compare[0] == 0 and compare[1] == player and \
                compare[2] == 0 and compare[3] == player \
                and compare[5] == enemy:
            return 300
        elif compare[1] == 0 and compare[2] == player and \
                compare[3] == 0 and compare[5] == player \
                and compare[6] == enemy:
            return 300
        elif compare[3] == 0 and compare[5] == 0 and \
                compare[6] == player and compare[7] == player \
                and compare[8] == enemy:
            return 300
        elif compare[0] == player and compare[1] == 0 and \
                compare[2] == player and compare[3] == 0 \
                and compare[5] == enemy:
            return 300
        elif compare[1] == enemy and compare[2] == player and \
                compare[3] == 0 and compare[5] == 0 \
                and compare[6] == player:
            return 300
        elif compare[2] == player and compare[3] == 0 and \
                compare[5]== 0 and compare[6] == player \
                and compare[7] == enemy:
            return 300
        elif compare[3] == enemy and compare[5] == 0 and \
                compare[6] == player and compare[7] == 0 \
                and compare[8] == player:
            return 300
        else:
            return 0

    @staticmethod
    def alive2(player, enemy, compare):
        """下在这个点会形成活二"""
        if compare[1] == 0 and compare[2] == 0 and \
                compare[3] == player and compare[5] == 0 \
                and compare[6] == 0:
            return 99
        elif compare[2] == 0 and compare[3] == 0 and \
                compare[5] == player and compare[6] == 0 \
                and compare[7] == 0:
            return 99
        elif compare[0] == 0 and compare[1] == 0 and \
                compare[2] == 0 and compare[3] == player \
                and compare[5] == 0 and compare[6] == enemy:
            return 99
        elif compare[1] == 0 and compare[2] == 0 and \
                compare[3] == 0 and compare[5] == player \
                and compare[6] == 0 and compare[7] == enemy:
            return 99
        elif compare[1] == enemy and compare[2] == 0 and \
                compare[3] == player and compare[5] == 0 \
                and compare[6] == 0 and compare[7] == 0:
            return 99
        elif compare[2] == enemy and compare[3] == 0 and \
                compare[5] == player and compare[6] == 0 \
                and compare[7] == 0 and compare[8] == 0:
            return 99
        else:
            return 0

    @staticmethod
    def sleep2(player, enemy, compare):
        """下在这个点会形成眠二"""
        if compare[2] == enemy and compare[3] == player and \
                compare[5] == 0 and compare[6] == 0 \
                and compare[7] == 0:
            return 5
        elif compare[3] == enemy and compare[5] == player and \
                compare[6] == 0 and compare[7] == 0 \
                and compare[8] == 0:
            return 5
        elif compare[0] == 0 and compare[1] == 0 and \
                compare[2] == 0 and compare[3] == player \
                and compare[5] == enemy:
            return 5
        elif compare[1] == 0 and compare[2] == 0 and \
                compare[3] == 0 and compare[5] == player \
                and compare[6] == enemy:
            return 5
        elif compare[1] == enemy and compare[2] == 0 and \
                compare[3] == player and compare[5] == 0 \
                and compare[6] == 0 and compare[7] == enemy:
            return 5
        elif compare[2] == enemy and compare[3] == 0 and \
                compare[5] == player and compare[6] == 0 \
                and compare[7] == 0 and compare[8] == enemy:
            return 5
        elif compare[0] == enemy and compare[1] == 0 and \
                compare[2] == player and compare[3] == 0 \
                and compare[5] == 0 and compare[6] == enemy:
            return 5
        elif compare[2] == enemy and compare[3] == 0 and \
                compare[5] == 0 and compare[6] == player \
                and compare[7] == 0 and compare[8] == enemy:
            return 5
        elif compare[0] == enemy and compare[1] == 0 and \
                compare[2] == 0 and compare[3] == player \
                and compare[5] == 0 and compare[6] == enemy:
            return 5
        elif compare[1] == enemy and compare[2] == 0 and \
                compare[3] == 0 and compare[5] == player \
                and compare[6] == 0 and compare[7] == enemy:
            return 5
        elif compare[0] == 0 and compare[1] == player and \
                compare[2] == 0 and compare[3] == 0 \
                and compare[5] == enemy:
            return 5
        elif compare[3] == 0 and compare[5] == 0 and \
                compare[6] == 0 and compare[7] == player \
                and compare[8] == enemy:
            return 5
        elif compare[0] == 0 and compare[1] == 0 and \
                compare[2] == player and compare[3] == 0 \
                and compare[5] == enemy:
            return 5
        elif compare[2] == 0 and compare[3] == 0 and \
                compare[5] == 0 and compare[6] == player \
                and compare[7] == enemy:
            return 5
        elif compare[1] == enemy and compare[2] == player and \
                compare[3] == 0 and compare[5] == 0 \
                and compare[6] == 0:
            return 5
        elif compare[3] == enemy and compare[5] == 0 and \
                compare[6] == player and compare[7] == 0 \
                and compare[8] == 0:
            return 5
        elif compare[0] == enemy and compare[1] == player and \
                compare[2] == 0 and compare[3] == 0 \
                and compare[5] == 0:
            return 5
        elif compare[3] == enemy and compare[5] == 0 and \
                compare[6] == 0 and compare[7] == player \
                and compare[8] == 0:
            return 5
        else:
            return 0



#获得题目定义的参数
'''
conf = GridObservation()
gb = GoBang(conf)
chess_player_idx = gb.chess_player #当前电脑玩家id. 1是黑棋，2是白棋，默认黑棋先下
board_width = gb.board_width #==15
board_height = gb.board_height #==15
current_state = gb.current_state #当前棋盘的整体情况==[x][y][0]
all_grids = gb.all_grids #所有未被占用的格点 ==[i][j]
all_observes = gb.all_observes #目前棋盘上所有黑白子 ==[i][j]
player_done = gb.joint_action_space #每个玩家的 action space list, 可以根据player_id获取对应的single_action_space==[i][j]
'''

'''
gobang可用函数：
check_at(x, y): 当前位置是否可以落子
'''


class check():
    def __init__(self,obs):
        #super().__init__(conf)

        '''
        self.width = board_width
        self.height = board_height
        #self.state = current_state
        self.grids = all_grids
        self.observes = all_observes
        self.done = player_done #此玩家的已有格点
        '''
        self.player_idx = obs["chess_player_idx"]
        self.current = obs["state_map"] #[[[]]]
        self.board = self.reshape32(self.current) #[[[]]]变成[[]]
        self.robot = Robot(self.board)

    def reshape32(self, dlist):
        #print("current:",self.current)
        #r = sum(dlist, [])
        import numpy as np
        temp = np.array(dlist)
        temp1 = temp.reshape(15,15)
        r = temp1.tolist()
        print("r:",r)
        return r

    def ai_play(self):
        """AI下棋"""
        if self.player_idx == 2:
            # 人执黑==机器是白棋2
            _x, _y, _z = self.robot.MaxValue_po(2, 1)
            #position_in_matrix = _x, _y
            return _x, _y
        else:
            _x, _y, _z = self.robot.MaxValue_po(1, 2)
            #position_in_matrix = _x, _y
            return _x, _y




#最终被主函数所调用，返回下棋的坐标（同时返回两个维度）
def my_controller(observation, action_space, is_act_continuous=False):
    agent_action = []

    for i in range(len(action_space)):
        #print("len:",len(action_space)) #2
        #print("action_space:",action_space) #[Discrete(15), Discrete(15)]

        #observation会传入dict, key分别为："state_map"、"chess_player_idx"、"board_width"和"board_height"
        #agent_id==0是黑棋，agent_id==1是白棋
        #传入的observation玩家idx是1和2
        #同一种棋盘state下分别返回两个玩家的两种策略，通过主函数中的顺序再决定选择哪个。因此，应该返回当前玩家的最佳下棋坐标即可。
        ai = check(observation)
        x, y = ai.ai_play()
        print("x,y:",x,y)
        #action_ = sample_single_dim(action_space[i], is_act_continuous, x, y)\
        action_ = change_form(x, y)
        #agent_action.append(action_)
    #print("agent ACTION:",agent_action) #[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    return action_


def change_form(x,y):
    list1 = [[0] * 15 for i in range(2)]
    list1[0][x]=1
    list1[1][y]=1
    return list1


#返回
def sample_single_dim(action_space_list_each, is_act_continuous, x, y):
    each = []
    if is_act_continuous:
        each = action_space_list_each.sample()
    else:
        #五子棋进这里====================================================================================================
        if action_space_list_each.__class__.__name__ == "Discrete":
            each = [0] * action_space_list_each.n
            #print("each:",each)
            idx = action_space_list_each.sample() #随机时所需要
            #idx
            each[idx] = 1
        #===============================================================================================================
        elif action_space_list_each.__class__.__name__ == "MultiDiscreteParticle":
            each = []
            nvec = action_space_list_each.high - action_space_list_each.low + 1
            sample_indexes = action_space_list_each.sample()

            for i in range(len(nvec)):
                dim = nvec[i]
                new_action = [0] * dim
                index = sample_indexes[i]
                new_action[index] = 1
                each.extend(new_action)
    return each


def sample(action_space_list_each, is_act_continuous):
    player = []
    if is_act_continuous:
        for j in range(len(action_space_list_each)):
            each = action_space_list_each[j].sample()
            player.append(each)
    else:
        player = []
        for j in range(len(action_space_list_each)):
            # each = [0] * action_space_list_each[j]
            # idx = np.random.randint(action_space_list_each[j])
            #五子棋进这里================================================================================================
            if action_space_list_each[j].__class__.__name__ == "Discrete":
                each = [0] * action_space_list_each[j].n
                idx = action_space_list_each[j].sample()
                each[idx] = 1
                player.append(each)
            # ==========================================================================================================
            elif action_space_list_each[j].__class__.__name__ == "MultiDiscreteParticle":
                each = []
                nvec = action_space_list_each[j].high
                sample_indexes = action_space_list_each[j].sample()

                for i in range(len(nvec)):
                    dim = nvec[i] + 1
                    new_action = [0] * dim
                    index = sample_indexes[i]
                    new_action[index] = 1
                    each.extend(new_action)
                player.append(each)
    return player
