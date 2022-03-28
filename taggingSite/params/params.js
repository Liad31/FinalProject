const DATABASECONNECTION = "mongodb+srv://ourProject:EMGwk59xADuSIIkv@cluster0.lhfaj.mongodb.net/production3?retryWrites=true&w=majority";
const WEEKLY_TAGS_NUM = "150"
const WEKKLY_UPDATE_TIME = "0 10 * * 2"
// const WEKKLY_UPDATE_TIME = "5 * * * * *"
const STRONG_FEATURES =  ["ביזוי דגל ישראל",
                          "הר הבית בצירוף השטאג לאומני",
                          "חיכוך עם כוחות הביטחון",
                          "תמונה של שהיד", 
                          "שמחה לאיד כלפי יהודים",
                          "כיתוב לאומני בתוך הסרט",
                          "אסירים",
                          "שהידים",
                          "עצירים",
                          "מחאה אלימה",
                          "שיר לאומני",
                          "האם הסרטון הועלה בלייב?"
                         ]
const WEAK_FEATURES =  ["השטאג לאומני ",
                         "כאפיה",
                         "דגל פלסטין",
                         "תמונה של יהודים בעלי חזות דתית מובהקת", 
                         "תמונה של כוחות הבטחון (ללא חיכוך)",
                        ]

const FEATURE_LIST = STRONG_FEATURES.slice()
FEATURE_LIST.push(WEAK_FEATURES)
const MAX_VIDEOS_PER_TAG = 3;

module.exports = {
    DATABASECONNECTION,
    WEEKLY_TAGS_NUM,
    WEKKLY_UPDATE_TIME,
    FEATURE_LIST,
    STRONG_FEATURES,
    WEAK_FEATURES,
    MAX_VIDEOS_PER_TAG
};