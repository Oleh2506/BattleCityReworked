import os
import json
import game_config as gc


class StageData:
    def __init__(self, directory, number_of_stages):
        self._directory = directory
        self._number_of_stages = number_of_stages

    def load_stage_data(self):
        file_names = os.listdir(self._directory)
        for i in range(self._number_of_stages):
            supposed_stage_name = f'stage{i}.json'
            if supposed_stage_name not in file_names:
                self.save_stage_by_name(StageData._generate_default_stage(), supposed_stage_name)

        stages = []
        for i in range(self._number_of_stages):
            with open(f'{self._directory}/stage{i}.json', 'r') as open_file:
                stage_obj = json.load(open_file)
            stages.append(stage_obj)

        return stages

    def save_stage_by_name(self, stage, stage_name):
        with open(f'{self._directory}/{stage_name}', 'w+') as out_file:
            json.dump(stage, out_file)

    def save_stage_by_num(self, stage, num):
        with open(f'{self._directory}/stage{num}.json', 'w+') as out_file:
            json.dump(stage, out_file)

    @staticmethod
    def _generate_default_stage():
        stage_map = [[-1 for _ in range(26)] for _ in range(26)]
        enemy_queue = [0]
        for (x, y) in gc.DEFAULT_PLAYER_SPAWN_POS:
            stage_map[y][x] = 6

        for (x, y) in gc.DEFAULT_BASE_POS:
            stage_map[y][x] = 5

        for (x, y) in gc.DEFAULT_ENEMIES_SPAWN_POS[0]:
            stage_map[y][x] = 7

        for (x, y) in gc.DEFAULT_ENEMIES_SPAWN_POS[1]:
            stage_map[y][x] = 8

        for (x, y) in gc.DEFAULT_ENEMIES_SPAWN_POS[2]:
            stage_map[y][x] = 9

        stage = {'map': stage_map,
                 'enemy_queue': enemy_queue}

        return stage
