import os
import shutil
from zipfile import ZipFile

import pandas as pd

import location_analyzer
from response_api import User


def get_posts_per_user(posts_df):
    map_post_index_to_user = {i: post_series['authorMeta.secUid'] for i, post_series in posts_df.iterrows()}
    users = set(map_post_index_to_user.values())
    map_user_to_posts_df = {user1: pd.concat([pd.DataFrame(posts_df.iloc[i]).T
                                              for i, user2 in map_post_index_to_user.items() if user1 == user2])
                            for user1 in users}
    return map_user_to_posts_df


def delete_files(files):
    # for file in files:
    #     os.remove(file)
    pass


def delete_dir(dir_name):
    # shutil.rmtree(dir_name)
    pass


class Scraper:
    def __init__(self, results_dir='scraper_data', cmds_filename='commands', proxy_filename='proxies.txt',
                 async_workers=10):
        self.results_dir = results_dir
        self.cmds_filename = cmds_filename
        self.proxy_filename = proxy_filename
        self.async_workers = async_workers
        self.counter = 0

    # EXTERNAL FUNCTIONS

    def scrap_posts(self, usernames, post_ids):
        cmds = [f'https://www.tiktok.com/@{username}/video/{post_id}' for username, post_id in zip(usernames, post_ids)]

        params= { 
            'filetype': 'csv'
        }
        dir_name = self.scrap_batch(cmds, params)

        output = self.generate_output_from_csv(dir_name)
        return output

    def scrap_hashtags(self, hashtags, num_posts, since, before, download=False):
        cmds = [f'#{hashtag}' for hashtag in hashtags]

        params = {
            'number': num_posts,
            'filetype': 'csv',
            'since': since,
            'before': before,
        }
        if download:
            params.update({'download': True})
        dir_name = self.scrap_batch(cmds, params)

        output = self.generate_output_from_csv(dir_name)
        return output

    def scrap_musics(self, music_ids, num_posts, since, before):
        cmds = [f'music:{music_id}' for music_id in music_ids]

        params = {
            'number': num_posts,
            'filetype': 'csv',
            'since': since,
            'before': before
        }
        dir_name = self.scrap_batch(cmds, params)

        output = self.generate_output_from_csv(dir_name)
        return output

    def scrap_users(self, usernames, num_posts, since, before):
        cmds = usernames

        params = {
            'number': num_posts,
            'filetype': 'csv',
            'since': since,
            'before': before
        }
        dir_name = self.scrap_batch(cmds, params)

        output = self.generate_output_from_csv(dir_name)
        print("dasdasd")
        return output

    # INTERNAL FUNCTIONS

    def scrap_batch(self, cmds, params):
        dir_name = os.path.join(self.results_dir, str(self.counter))
        cmds_name = self.cmds_filename + str(self.counter)
        
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        os.mkdir(dir_name)
        self.counter += 1

        self.generate_cmds_file(cmds, cmds_name)

        params['proxy-file'] = self.proxy_filename
        params['filepath'] = dir_name

        scrap_params = ' '.join(f'--{param_name} {param_value}' for param_name, param_value in params.items())
        scrap_cmd = f'ts-node tiktok-scraper/bin/cli.js from-file {cmds_name} {self.async_workers}'
        print(scrap_cmd)
        os.system(f'{scrap_cmd} {scrap_params}')

        os.remove(cmds_name)
        return dir_name

    def generate_cmds_file(self, cmds, path):
        with open(path, 'w', encoding='utf8') as cmds_file:
            file_content = '\n'.join(cmds)
            cmds_file.write(file_content)

    def generate_output_from_csv(self, dir_name):
        files = self.get_result_files('csv')
        posts_df = pd.concat([pd.read_csv(file) for file in files]).reset_index()

        map_secure_id_to_posts_df = get_posts_per_user(posts_df)
        output = [User.from_scraper_pandas_series(user_posts_df.iloc[0])
                      .add_posts_from_scraper_pandas_df(user_posts_df)
                  for user_posts_df in map_secure_id_to_posts_df.values()]

        user_location_by_secure_id = location_analyzer.find_users_locations(output, map_secure_id_to_posts_df)
        output = [user.set_governorate(user_location_by_secure_id.get(user.secure_id, '')).as_dict()
                  for user in output]

        delete_dir(dir_name)
        return output

    def get_from_csv(self, csv_file_name):
        posts_df = pd.read_csv(csv_file_name)
        map_secure_id_to_posts_df = get_posts_per_user(posts_df)
        output = [User.from_scraper_pandas_series(user_posts_df.iloc[0])
                      .add_posts_from_scraper_pandas_df(user_posts_df)
                  for user_posts_df in map_secure_id_to_posts_df.values()]

        user_location_by_secure_id = location_analyzer.find_users_locations(output, map_secure_id_to_posts_df)
        output = [user.set_governorate(user_location_by_secure_id.get(user.secure_id, '')).as_dict()
                  for user in output]
        return output

    def generate_output_from_mp4(self, dir_name):
        files = self.get_result_files('mp4')
        relative_filepaths = [file[len(self.results_dir) + 1:] for file in files]

        cwd = os.getcwd()
        os.chdir(self.results_dir)

        with ZipFile('mp4_files.zip', 'w') as zip_file:
            for file in relative_filepaths:
                zip_file.write(file)
        with open('mp4_files.zip', 'rb') as zip_file:
            output = zip_file.read()
        os.remove('mp4_files.zip')

        os.chdir(cwd)

        delete_dir(dir_name)
        return output

    def get_result_files(self, file_extention):
        result_files = []
        for root, _, files in os.walk(self.results_dir):
            for file in files:
                if file.endswith('.' + file_extention):
                    result_files.append(os.path.join(root, file))
        return result_files


scraper = Scraper()
