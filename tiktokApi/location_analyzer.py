from collections import Counter
import json

import pandas as pd

hashtags_by_city = {
    'Bethlehem': ['بيتلحم', 'بيت_لحم'],
    'Hebron': ['الخليل', 'يطا', 'خليل', 'خليلي'],
    'Jenin': ['جنين', 'قباطية'],
    'Jericho': ['أريحا'],
    'Jerusalem': ['القدس'],
    'Nablus': ['نابلس', 'مخيم_بلاطة', 'بلاطة'],
    'Qalqilya': ['قلقيلية'],
    'Ramallah and Al-Bireh': ['رامالله', 'رام_الله', 'البيرة'],
    'Salfit': ['سلفيت'],
    'Tubas': ['طوباس'],
    'Tulkarm': ['طولكرم']
}
city_by_hashtag = {hashtag: city for city, hashtags in hashtags_by_city.items() for hashtag in hashtags}


def get_hashtags_in_users_posts(dfs):
    hashtags_counters = {}
    for sec_uid, df in dfs.items():
        hashtags_in_posts = df['hashtags']
        hashtags_counter = Counter([hashtag['name'] for post in hashtags_in_posts for hashtag in json.loads(post)])
        hashtags_counters[sec_uid] = hashtags_counter
    return hashtags_counters


def get_cities_hashtags(hashtags_counter, name_to_city):
    cities_counter = Counter()
    for k, v in hashtags_counter.items():
        if k in name_to_city:
            cities_counter[name_to_city[k]] += v
    return cities_counter


def norm_counter(counter):
    s = sum(counter.values())
    if s == 0:
        return counter
    result = {k: v / s for k, v in counter.items()}
    return Counter(result)


def get_cities_in_bio(bio, name_to_city):
    if type(bio) != str:
        return Counter()
    bio = bio.replace(' ', '').lower()
    cities_counter = Counter()
    for k in name_to_city:
        cities_counter[name_to_city[k]] += bio.count(k)
    for city in set(name_to_city.values()):
        cities_counter[city] += bio.count(city.split()[0].lower())
    cities_counter = Counter({k: v for k, v in cities_counter.items() if v > 0})
    return cities_counter


def calc_users_cities_counters(sec_uids_to_users, user_df_by_sec_uid, name_to_city):
    result = {}
    hashtags_counters = get_hashtags_in_users_posts(user_df_by_sec_uid)
    for sec_uid in hashtags_counters:
        sec_uid, username, bio = sec_uids_to_users[sec_uid]
        hashtags_counter = hashtags_counters[sec_uid]
        cities_counter = get_cities_hashtags(hashtags_counter, name_to_city)
        bio_counter = get_cities_in_bio(bio, name_to_city)
        result[(sec_uid, username)] = (bio_counter, cities_counter)
    return result


def counter_is_not_empty(counter):
    return len(counter) > 0


def counter_have_one_element(counter):
    return len(counter) == 1


def link_of_user(sec_uid):
    return f'www.tiktok.com/@{sec_uid}'


def create_df_of_users(users_cities_counters):
    rows = []
    for user in users_cities_counters:
        bio_counter, cities_counter = users_cities_counters[user]
        norm_bio_counter = norm_counter(bio_counter)
        norm_cities_counter = norm_counter(cities_counter)
        if counter_have_one_element(bio_counter):
            city, bio_freq = norm_bio_counter.most_common(1)[0]
            row = [link_of_user(user[0]), city, bio_freq, norm_cities_counter[city], 'bio']
            rows.append(row)
        elif counter_is_not_empty(cities_counter):
            city, hashtags_freq = norm_cities_counter.most_common(1)[0]
            if hashtags_freq >= 0.6 and cities_counter[city] >= 3:
                row = [link_of_user(user[0]), city, norm_bio_counter[city], hashtags_freq, 'hashtags']
                rows.append(row)
    return pd.DataFrame(rows, columns=["link", "city", "bio freq", "hashtags freq", 'classified by'])


def parse_link(link):
    return link.split('@')[-1]


def get_location_by_sec_uid(cities_df):
    location_by_sec_uid = {}
    for _, row in cities_df.iterrows():
        sec_uid = parse_link(row['link'])
        location = row['city']
        location_by_sec_uid[sec_uid] = location
    return location_by_sec_uid


def find_users_locations(users, map_secure_id_to_posts_df):
    user_details_by_sec_uids = {user.secure_id: (user.secure_id, user.username, user.bio) for user in users}
    result = calc_users_cities_counters(user_details_by_sec_uids, map_secure_id_to_posts_df, city_by_hashtag)
    df_users_locations = create_df_of_users(result)
    location_by_sec_uid = get_location_by_sec_uid(df_users_locations)
    print(f"location: {location_by_sec_uid}")
    return location_by_sec_uid
