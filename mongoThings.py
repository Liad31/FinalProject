from pymongo import MongoClient

import time
import math
# Requires the PyMongo package.
# https://api.mongodb.com/python/current
# Requires the PyMongo package.
# https://api.mongodb.com/python/current

client = MongoClient('mongodb+srv://ourProject:EMGwk59xADuSIIkv@cluster0.lhfaj.mongodb.net/production2?authSource=admin&replicaSet=atlas-mnojto-shard-0&w=majority&readPreference=primary&appname=MongoDB+Compass&retryWrites=true&ssl=true')
def avgScore(startEpoch, endEpoch,topPer=0.2):
    result = client['production3']['videos'].aggregate([
    {
        '$addFields': {
            'dateInt': {
                '$toInt': '$date'
            }
        }
    }, {
        '$match': {
            '$and': [
                {
                    'score': {
                        '$gt': -1
                    }
                }, {
                    'dateInt': {
                        '$lt': endEpoch
                    }
                }, {
                    'dateInt': {
                        '$gt': startEpoch
                    }
                }
            ]
        }
    }, {
        '$count': 'count'
    }
    ])
    result=list(result)
    if not result:
        return None
    numResults=result[0]['count']
    # print(numResults)
    result = client['production3']['videos'].aggregate([
        {
            '$addFields': {
                'dateInt': {
                    '$toInt': '$date'
                }
            }
        }, {
            '$match': {
                '$and': [
                    {
                        'score': {
                            '$gt': -1
                        }
                    }, {
                        'dateInt': {
                            '$lt': endEpoch
                        }
                    }, {
                        'dateInt': {
                            '$gt': startEpoch
                        }
                    }
                ]
            }
        }, {
            '$sort': {
                'score': -1
            }
        }, {
            '$limit': int(numResults*topPer)
        }, {
            '$group': {
                '_id': 1, 
                'avg': {
                    '$avg': "$relScore"
                }, 
                'count': {
                    '$sum': 1
                }
            }
        }
    ])
    return list(result)[0]['avg']
def mostRelevant(startEpoch,endEpoch):
    result = client['production3']['videos'].aggregate([
    {
        '$addFields': {
            'dateInt': {
                '$toInt': '$date'
            }
        }
    }, {
        '$match': {
            '$and': [
                 {
                    'dateInt': {
                        '$lt': endEpoch
                    }
                }, {
                    'dateInt': {
                        '$gt': startEpoch
                    }
                }
            ]
        }
    }, {
        '$sort': {
            'score': -1
        }
    }, {
        '$limit': 1
    }
    ])
    result= list(result)
    if not result:
        return None
    return result[0]['Vid']
def avgScoreOverTime( iters=130,topPer=0.2,daysDelta=1,daysBack=3):
    currEpoch=int(time.time())
    dayToSec=24*60*60
    res=[]
    for i in range(iters):
        end=currEpoch-i*dayToSec*daysDelta
        mostRel= mostRelevant(end-daysBack*dayToSec,end)
        if not mostRel:
            continue
        avg= avgScore(end-daysBack*dayToSec,end,topPer)
        formatedDate= time.strftime("%Y-%m-%d", time.localtime(end))
        res.append([avg,formatedDate,mostRel])
    return res
def governorateScores(topPer=0.2,startEpoch=None):
    if not startEpoch:
        currentTimeEpoch=int(time.time())
        lastMonthEpoch= currentTimeEpoch-30*24*60*60*3
        startEpoch=lastMonthEpoch
    x=[]
    for governorate in ['Bethlehem','Hebron', 'Jenin','Jericho','Jerusalem','Nablus', 'Qalqilya','Ramallah and Al-Bireh', 'Salfit', 'Tubas', 'Tulkarm']:
        numResults = client['production3']['videos'].aggregate([
            {
                '$addFields': {
                    'dateInt': {
                        '$toInt': '$date'
                    }
                }
            }, {
                '$match': {
                    '$and': [
                        {
                            'score': {
                                '$gt': -1
                            }
                        }, {
                            'dateInt': {
                                '$gt': startEpoch
                            }
                        }
                    ]
                }
            }, {
                '$group': {
                    '_id': '$user', 
                    'avg': {
                        '$avg': '$score'
                    }, 
                    'count': {
                        '$sum': 1
                    }
                }
            }, {
                '$lookup': {
                    'from': 'tiktokusernationalistics', 
                    'localField': '_id', 
                    'foreignField': '_id', 
                    'as': 'user'
                }
            }, {
                '$addFields': {
                    'user': {
                        '$first': '$user'
                    }
                }
            }, {
                '$match': {
                    'user.governorate': governorate
                }
            }, {
                '$count': 'count'
            }
        ])
        numResults=list(numResults)
        if not numResults:
            print(governorate+' has no results')
            continue
        result = client['production3']['videos'].aggregate([
            {
                '$addFields': {
                    'dateInt': {
                        '$toInt': '$date'
                    }
                }
            }, {
                '$match': {
                    '$and': [
                        {
                            'score': {
                                '$gt': -1
                            }
                        }, {
                            'dateInt': {
                                '$gt': startEpoch
                            }
                        }
                    ]
                }
            }, {
                '$group': {
                    '_id': '$user', 
                    'avg': {
                        '$avg': '$score'
                    }, 
                    'count': {
                        '$sum': 1
                    }
                }
            }, {
                '$lookup': {
                    'from': 'tiktokusernationalistics', 
                    'localField': '_id', 
                    'foreignField': '_id', 
                    'as': 'user'
                }
            }, {
                '$addFields': {
                    'user': {
                        '$first': '$user'
                    }
                }
            }, {
                '$match': {
                    'user.governorate': governorate
                }
            }, {
                '$sort': {
                    'user.nationalisticScore': -1
                }
            }, {
                '$limit': math.ceil(topPer*numResults[0]['count'])
            }, {
                '$group': {
                    '_id': '$user.governorate', 
                    'governorateAvg': {
                        '$avg': '$user.nationalisticScore'
                    }
                }
            }
        ])
        result=list(result)
        if not result:
            return []
        x.append((governorate, result[0]['governorateAvg']))
    return x
