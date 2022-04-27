import json
from dataclasses import dataclass
from datetime import datetime

import numpy as np


@dataclass()
class Music:
    id: str
    name: str
    author_name: str
    is_original: bool
    album: str
    url: str

    def as_dict(self):
        result = self.__dict__
        return result

    @classmethod
    def from_scraper_pandas_series(cls, series):
        return Music(
            id=str(series['musicMeta.musicId']),
            name=series['musicMeta.musicName'],
            author_name=series['musicMeta.musicAuthor'],
            is_original=bool(series['musicMeta.musicOriginal']),
            album=series['musicMeta.musicAlbum'] if series['musicMeta.musicAlbum'] != np.nan else '',
            url=series['musicMeta.playUrl']
        )


@dataclass()
class Video:
    height: int
    width: int

    def as_dict(self):
        result = self.__dict__
        return result

    @classmethod
    def from_scraper_pandas_series(cls, series):
        return Video(
            height=int(series['videoMeta.height']),
            width=int(series['videoMeta.width']),
        )


@dataclass()
class PostStats:
    diggs_count: int
    shares_count: int
    plays_count: int
    comments_count: int

    def as_dict(self):
        result = self.__dict__
        return result

    @classmethod
    def from_scraper_pandas_series(cls, series):
        return PostStats(
            diggs_count=int(series['diggCount']) if series['diggCount'] == series['diggCount'] else None,
            shares_count=int(series['shareCount']) if series['shareCount'] == series['shareCount'] else None,
            plays_count=int(series['playCount']) if series['playCount'] == series['playCount'] else None,
            comments_count=int(series['commentCount']) if series['commentCount'] == series['commentCount'] else None
        )


@dataclass()
class Post:
    id: str
    description: str
    upload_date: str
    music: Music
    web_url: str
    video: Video
    stats: PostStats
    mentions: list
    hashtags: list

    def as_dict(self):
        result = self.__dict__
        result['music'] = result['music'].as_dict()
        result['video'] = result['video'].as_dict()
        result['stats'] = result['stats'].as_dict()
        return result

    @classmethod
    def from_scraper_pandas_series(cls, series):
        return Post(
            id=str(series['id']),
            description=series['text'],
            upload_date=datetime.fromtimestamp(series['createTime']).strftime("%Y-%m-%dT%H:%M:%S"),
            music=Music.from_scraper_pandas_series(series),
            web_url=series['webVideoUrl'],
            video=Video.from_scraper_pandas_series(series),
            stats=PostStats.from_scraper_pandas_series(series),
            mentions=json.dumps([mention[1:] for mention in json.loads(series['mentions'])]),
            hashtags=json.dumps([hashtag['name'] for hashtag in json.loads(series['hashtags'])])
        )


@dataclass()
class UserStats:
    following_count: int
    followers_count: int
    likes_count: int
    posts_count: int
    diggs_count: int

    def as_dict(self):
        result = self.__dict__
        return result

    @classmethod
    def from_scraper_pandas_series(cls, series):
        return UserStats(
            following_count=int(series['authorMeta.following']) if series['authorMeta.following'] == series['authorMeta.following'] else None,
            followers_count=int(series['authorMeta.fans']) if series['authorMeta.fans'] == series['authorMeta.fans'] else None,
            likes_count=int(series['authorMeta.heart']) if series['authorMeta.heart'] == series['authorMeta.heart'] else None,
            posts_count=int(series['authorMeta.video']) if series['authorMeta.video'] == series['authorMeta.video'] else None,
            diggs_count=int(series['authorMeta.digg']) if series['authorMeta.digg'] == series['authorMeta.digg'] else None
        )


@dataclass()
class User:
    id: str
    secure_id: str
    username: str
    name: str
    is_verified: bool
    bio: str
    stats: UserStats
    governorate: str
    posts: list

    def add_posts_from_scraper_pandas_df(self, df):
        for _, series in df.iterrows():
            self.posts.append(Post.from_scraper_pandas_series(series))
        return self

    def set_governorate(self, governorate):
        self.governorate = governorate
        return self

    def as_dict(self):
        result = self.__dict__
        result['stats'] = result['stats'].as_dict()
        result['posts'] = [post.as_dict() for post in result['posts']]
        return result

    @classmethod
    def from_scraper_pandas_series(cls, series):
        return User(
            id=str(series['authorMeta.id']),
            secure_id=series['authorMeta.secUid'],
            username=series['authorMeta.name'],
            name=series['authorMeta.nickName'],
            is_verified=bool(series['authorMeta.verified']),
            bio=series['authorMeta.signature'],
            stats=UserStats.from_scraper_pandas_series(series),
            governorate='',
            posts=[]
        )
