from numba import jit
import re
import os
import sys
import time
import json
from fuzzywuzzy import fuzz
from tqdm import tqdm
import logging
import speech_recognition

dir_path = ""
if getattr(sys, 'frozen', False):
    dir_path = os.path.dirname(os.path.realpath(sys.executable))
elif __file__:
    dir_path = os.path.dirname(os.path.realpath(__file__))

langs_json = [{
    "0": {
        "Language": "Afrikaans (Suid-Afrika)",
        "code": "af-ZA",
        "name": "南非荷蘭文 (南非)"
    },
    "1": {
        "Language": "አማርኛ (ኢትዮጵያ)",
        "code": "am-ET",
        "name": "阿姆哈拉文 (衣索比亞)"
    },
    "2": {
        "Language": "Հայ (Հայաստան)",
        "code": "hy-AM",
        "name": "亞美尼亞文 (亞美尼亞)"
    },
    "3": {
        "Language": "Azərbaycan (Azərbaycan)",
        "code": "az-AZ",
        "name": "亞塞拜然文 (亞塞拜然)"
    },
    "4": {
        "Language": "Bahasa Indonesia (Indonesia)",
        "code": "id-ID",
        "name": "印尼文 (印尼)"
    },
    "5": {
        "Language": "Bahasa Melayu (Malaysia)",
        "code": "ms-MY",
        "name": "馬來文 (馬來西亞)"
    },
    "6": {
        "Language": "বাংলা (বাংলাদেশ)",
        "code": "bn-BD",
        "name": "孟加拉文 (孟加拉)"
    },
    "7": {
        "Language": "বাংলা (ভারত)",
        "code": "bn-IN",
        "name": "孟加拉文 (印度)"
    },
    "8": {
        "Language": "Català (Espanya)",
        "code": "ca-ES",
        "name": "加泰隆尼亞文 (西班牙)"
    },
    "9": {
        "Language": "Čeština (Česká republika)",
        "code": "cs-CZ",
        "name": "捷克文 (捷克共和國)"
    },
    "10": {
        "Language": "Dansk (Danmark)",
        "code": "da-DK",
        "name": "丹麥文 (丹麥)"
    },
    "11": {
        "Language": "Deutsch (Deutschland)",
        "code": "de-DE",
        "name": "德文 (德國)"
    },
    "12": {
        "Language": "English (Australia)",
        "code": "en-AU",
        "name": "英文 (澳洲)"
    },
    "13": {
        "Language": "English (Canada)",
        "code": "en-CA",
        "name": "英文 (加拿大)"
    },
    "14": {
        "Language": "English (Ghana)",
        "code": "en-GH",
        "name": "英文 (迦納)"
    },
    "15": {
        "Language": "English (Great Britain)",
        "code": "en-GB",
        "name": "英文 (英國)"
    },
    "16": {
        "Language": "English (India)",
        "code": "en-IN",
        "name": "英文 (印度)"
    },
    "17": {
        "Language": "English (Ireland)",
        "code": "en-IE",
        "name": "英文 (愛爾蘭)"
    },
    "18": {
        "Language": "English (Kenya)",
        "code": "en-KE",
        "name": "英文 (肯亞)"
    },
    "19": {
        "Language": "English (New Zealand)",
        "code": "en-NZ",
        "name": "英文 (紐西蘭)"
    },
    "20": {
        "Language": "English (Nigeria)",
        "code": "en-NG",
        "name": "英文 (奈及利亞)"
    },
    "21": {
        "Language": "English (Philippines)",
        "code": "en-PH",
        "name": "英文 (菲律賓)"
    },
    "22": {
        "Language": "English (Singapore)",
        "code": "en-SG",
        "name": "英文 (新加坡)"
    },
    "23": {
        "Language": "English (South Africa)",
        "code": "en-ZA",
        "name": "英文 (南非)"
    },
    "24": {
        "Language": "English (Tanzania)",
        "code": "en-TZ",
        "name": "英文 (坦尚尼亞)"
    },
    "25": {
        "Language": "English (United States)",
        "code": "en-US",
        "name": "英文 (美國)"
    },
    "26": {
        "Language": "Español (Argentina)",
        "code": "es-AR",
        "name": "西班牙文 (阿根廷)"
    },
    "27": {
        "Language": "Español (Bolivia)",
        "code": "es-BO",
        "name": "西班牙文 (玻利維亞)"
    },
    "28": {
        "Language": "Español (Chile)",
        "code": "es-CL",
        "name": "西班牙文 (智利)"
    },
    "29": {
        "Language": "Español (Colombia)",
        "code": "es-CO",
        "name": "西班牙文 (哥倫比亞)"
    },
    "30": {
        "Language": "Español (Costa Rica)",
        "code": "es-CR",
        "name": "西班牙文 (哥斯大黎加)"
    },
    "31": {
        "Language": "Español (Ecuador)",
        "code": "es-EC",
        "name": "西班牙文 (厄瓜多)"
    },
    "32": {
        "Language": "Español (El Salvador)",
        "code": "es-SV",
        "name": "西班牙文 (薩爾瓦多)"
    },
    "33": {
        "Language": "Español (España)",
        "code": "es-ES",
        "name": "西班牙文 (西班牙)"
    },
    "34": {
        "Language": "Español (Estados Unidos)",
        "code": "es-US",
        "name": "西班牙文 (美國)"
    },
    "35": {
        "Language": "Español (Guatemala)",
        "code": "es-GT",
        "name": "西班牙文 (瓜地馬拉)"
    },
    "36": {
        "Language": "Español (Honduras)",
        "code": "es-HN",
        "name": "西班牙文 (宏都拉斯)"
    },
    "37": {
        "Language": "Español (México)",
        "code": "es-MX",
        "name": "西班牙文 (墨西哥)"
    },
    "38": {
        "Language": "Español (Nicaragua)",
        "code": "es-NI",
        "name": "西班牙文 (尼加拉瓜)"
    },
    "39": {
        "Language": "Español (Panamá)",
        "code": "es-PA",
        "name": "西班牙文 (巴拿馬)"
    },
    "40": {
        "Language": "Español (Paraguay)",
        "code": "es-PY",
        "name": "西班牙文 (巴拉圭)"
    },
    "41": {
        "Language": "Español (Perú)",
        "code": "es-PE",
        "name": "西班牙文 (秘魯)"
    },
    "42": {
        "Language": "Español (Puerto Rico)",
        "code": "es-PR",
        "name": "西班牙文 (波多黎各)"
    },
    "43": {
        "Language": "Español (República Dominicana)",
        "code": "es-DO",
        "name": "西班牙文 (多米尼克共和國)"
    },
    "44": {
        "Language": "Español (Uruguay)",
        "code": "es-UY",
        "name": "西班牙文 (烏拉圭)"
    },
    "45": {
        "Language": "Español (Venezuela)",
        "code": "es-VE",
        "name": "西班牙文 (委內瑞拉)"
    },
    "46": {
        "Language": "Euskara (Espainia)",
        "code": "eu-ES",
        "name": "巴斯克文 (西班牙)"
    },
    "47": {
        "Language": "Filipino (Pilipinas)",
        "code": "fil-PH",
        "name": "菲律賓文 (菲律賓)"
    },
    "48": {
        "Language": "Français (Canada)",
        "code": "fr-CA",
        "name": "法文 (加拿大)"
    },
    "49": {
        "Language": "Français (France)",
        "code": "fr-FR",
        "name": "法文 (法國)"
    },
    "50": {
        "Language": "Galego (España)",
        "code": "gl-ES",
        "name": "加里西亞文 (西班牙)"
    },
    "51": {
        "Language": "ქართული (საქართველო)",
        "code": "ka-GE",
        "name": "喬治亞文 (喬治亞)"
    },
    "52": {
        "Language": "ગુજરાતી (ભારત)",
        "code": "gu-IN",
        "name": "古吉拉特文 (印度)"
    },
    "53": {
        "Language": "Hrvatski (Hrvatska)",
        "code": "hr-HR",
        "name": "克羅埃西亞文 (克羅埃西亞)"
    },
    "54": {
        "Language": "IsiZulu (Ningizimu Afrika)",
        "code": "zu-ZA",
        "name": "祖魯文 (南非)"
    },
    "55": {
        "Language": "Íslenska (Ísland)",
        "code": "is-IS",
        "name": "冰島文 (冰島)"
    },
    "56": {
        "Language": "Italiano (Italia)",
        "code": "it-IT",
        "name": "義大利文 (義大利)"
    },
    "57": {
        "Language": "Jawa (Indonesia)",
        "code": "jv-ID",
        "name": "爪哇文 (印尼)"
    },
    "58": {
        "Language": "ಕನ್ನಡ (ಭಾರತ)",
        "code": "kn-IN",
        "name": "卡納達文 (印度)"
    },
    "59": {
        "Language": "ភាសាខ្មែរ (កម្ពុជា)",
        "code": "km-KH",
        "name": "高棉文 (柬埔寨)"
    },
    "60": {
        "Language": "ລາວ (ລາວ)",
        "code": "lo-LA",
        "name": "寮文 (寮國)"
    },
    "61": {
        "Language": "Latviešu (latviešu)",
        "code": "lv-LV",
        "name": "拉脫維亞文 (拉脫維亞)"
    },
    "62": {
        "Language": "Lietuvių (Lietuva)",
        "code": "lt-LT",
        "name": "立陶宛文 (立陶宛)"
    },
    "63": {
        "Language": "Magyar (Magyarország)",
        "code": "hu-HU",
        "name": "匈牙利文 (匈牙利)"
    },
    "64": {
        "Language": "മലയാളം (ഇന്ത്യ)",
        "code": "ml-IN",
        "name": "馬拉雅拉姆文 (印度)"
    },
    "65": {
        "Language": "मराठी (भारत)",
        "code": "mr-IN",
        "name": "馬拉地文 (印度)"
    },
    "66": {
        "Language": "Nederlands (Nederland)",
        "code": "nl-NL",
        "name": "荷蘭文 (荷蘭)"
    },
    "67": {
        "Language": "नेपाली (नेपाल)",
        "code": "ne-NP",
        "name": "尼泊爾文 (尼泊爾)"
    },
    "68": {
        "Language": "Norsk bokmål (Norge)",
        "code": "nb-NO",
        "name": "挪威博克馬爾文 (挪威)"
    },
    "69": {
        "Language": "Polski (Polska)",
        "code": "pl-PL",
        "name": "波蘭文 (波蘭)"
    },
    "70": {
        "Language": "Português (Brasil)",
        "code": "pt-BR",
        "name": "葡萄牙文 (巴西)"
    },
    "71": {
        "Language": "Português (Portugal)",
        "code": "pt-PT",
        "name": "葡萄牙文 (葡萄牙)"
    },
    "72": {
        "Language": "Română (România)",
        "code": "ro-RO",
        "name": "羅馬尼亞文 (羅馬尼亞)"
    },
    "73": {
        "Language": "සිංහල (ශ්රී ලංකාව)",
        "code": "si-LK",
        "name": "錫蘭文 (斯里蘭卡)"
    },
    "74": {
        "Language": "Slovenčina (Slovensko)",
        "code": "sk-SK",
        "name": "斯洛伐克文 (斯洛伐克)"
    },
    "75": {
        "Language": "Slovenščina (Slovenija)",
        "code": "sl-SI",
        "name": "斯洛維尼亞文 (斯洛維尼亞)"
    },
    "76": {
        "Language": "Urang (Indonesia)",
        "code": "su-ID",
        "name": "巽他文 (印尼)"
    },
    "77": {
        "Language": "Swahili (Tanzania)",
        "code": "sw-TZ",
        "name": "斯瓦希里文 (坦尚尼亞)"
    },
    "78": {
        "Language": "Swahili (Kenya)",
        "code": "sw-KE",
        "name": "斯瓦希里文 (肯亞)"
    },
    "79": {
        "Language": "Suomi (Suomi)",
        "code": "fi-FI",
        "name": "芬蘭文 (芬蘭)"
    },
    "80": {
        "Language": "Svenska (Sverige)",
        "code": "sv-SE",
        "name": "瑞典文 (瑞典)"
    },
    "81": {
        "Language": "தமிழ் (இந்தியா)",
        "code": "ta-IN",
        "name": "泰米爾文 (印度)"
    },
    "82": {
        "Language": "தமிழ் (சிங்கப்பூர்)",
        "code": "ta-SG",
        "name": "泰米爾文 (新加坡)"
    },
    "83": {
        "Language": "தமிழ் (இலங்கை)",
        "code": "ta-LK",
        "name": "泰米爾文 (斯里蘭卡)"
    },
    "84": {
        "Language": "தமிழ் (மலேசியா)",
        "code": "ta-MY",
        "name": "泰米爾文 (馬來西亞)"
    },
    "85": {
        "Language": "తెలుగు (భారతదేశం)",
        "code": "te-IN",
        "name": "泰盧固文 (印度)"
    },
    "86": {
        "Language": "Tiếng Việt (Việt Nam)",
        "code": "vi-VN",
        "name": "越南文 (越南)"
    },
    "87": {
        "Language": "Türkçe (Türkiye)",
        "code": "tr-TR",
        "name": "土耳其文 (土耳其)"
    },
    "88": {
        "Language": "اردو (پاکستان)",
        "code": "ur-PK",
        "name": "烏都文 (巴基斯坦)"
    },
    "89": {
        "Language": "اردو (بھارت)",
        "code": "ur-IN",
        "name": "烏都文 (印度)"
    },
    "90": {
        "Language": "Ελληνικά (Ελλάδα)",
        "code": "el-GR",
        "name": "希臘文 (希臘)"
    },
    "91": {
        "Language": "Български (България)",
        "code": "bg-BG",
        "name": "保加利亞文 (保加利亞)"
    },
    "92": {
        "Language": "Русский (Россия)",
        "code": "ru-RU",
        "name": "俄文 (俄羅斯)"
    },
    "93": {
        "Language": "Српски (Србија)",
        "code": "sr-RS",
        "name": "塞爾維亞文 (塞爾維亞)"
    },
    "94": {
        "Language": "Українська (Україна)",
        "code": "uk-UA",
        "name": "烏克蘭文 (烏克蘭)"
    },
    "95": {
        "Language": "עברית (ישראל)",
        "code": "he-IL",
        "name": "希伯來文 (以色列)"
    },
    "96": {
        "Language": "العربية (إسرائيل)",
        "code": "ar-IL",
        "name": "阿拉伯文 (以色列)"
    },
    "97": {
        "Language": "العربية (الأردن)",
        "code": "ar-JO",
        "name": "阿拉伯文 (約旦)"
    },
    "98": {
        "Language": "العربية (الإمارات)",
        "code": "ar-AE",
        "name": "阿拉伯文 (阿拉伯聯合大公國)"
    },
    "99": {
        "Language": "العربية (البحرين)",
        "code": "ar-BH",
        "name": "阿拉伯文 (巴林)"
    },
    "100": {
        "Language": "العربية (الجزائر)",
        "code": "ar-DZ",
        "name": "阿拉伯文 (阿爾及利亞)"
    },
    "101": {
        "Language": "العربية (السعودية)",
        "code": "ar-SA",
        "name": "阿拉伯文 (沙烏地阿拉伯)"
    },
    "102": {
        "Language": "العربية (العراق)",
        "code": "ar-IQ",
        "name": "阿拉伯文 (伊拉克)"
    },
    "103": {
        "Language": "العربية (الكويت)",
        "code": "ar-KW",
        "name": "阿拉伯文 (科威特)"
    },
    "104": {
        "Language": "العربية (المغرب)",
        "code": "ar-MA",
        "name": "阿拉伯文 (摩洛哥)"
    },
    "105": {
        "Language": "العربية (تونس)",
        "code": "ar-TN",
        "name": "阿拉伯文 (突尼西亞)"
    },
    "106": {
        "Language": "العربية (عُمان)",
        "code": "ar-OM",
        "name": "阿拉伯文 (阿曼)"
    },
    "107": {
        "Language": "العربية (فلسطين)",
        "code": "ar-PS",
        "name": "阿拉伯文 (巴勒斯坦國)"
    },
    "108": {
        "Language": "العربية (قطر)",
        "code": "ar-QA",
        "name": "阿拉伯文 (卡達)"
    },
    "109": {
        "Language": "العربية (لبنان)",
        "code": "ar-LB",
        "name": "阿拉伯文 (黎巴嫩)"
    },
    "110": {
        "Language": "العربية (مصر)",
        "code": "ar-EG",
        "name": "阿拉伯文 (埃及)"
    },
    "111": {
        "Language": "فارسی (ایران)",
        "code": "fa-IR",
        "name": "波斯文 (伊朗)"
    },
    "112": {
        "Language": "हिन्दी (भारत)",
        "code": "hi-IN",
        "name": "北印度文 (印度)"
    },
    "113": {
        "Language": "ไทย (ประเทศไทย)",
        "code": "th-TH",
        "name": "泰文 (泰國)"
    },
    "114": {
        "Language": "한국어 (대한민국)",
        "code": "ko-KR",
        "name": "韓文 (南韓)"
    },
    "115": {
        "Language": "國語 (台灣)",
        "code": "zh-TW",
        "name": "中文，華語 (繁體，台灣)"
    },
    "116": {
        "Language": "廣東話 (香港)",
        "code": "yue-Hant-HK",
        "name": "中文，粵語 (繁體，香港)"
    },
    "117": {
        "Language": "日本語（日本）",
        "code": "ja-JP",
        "name": "日文 (日本)"
    },
    "118": {
        "Language": "普通話 (香港)",
        "code": "zh-HK",
        "name": "中文，華語 (簡體，香港)"
    },
    "119": {
        "Language": "普通话 (中国大陆)",
        "code": "zh",
        "name": "中文，華語 (簡體，中國)"
    }
}]

class SpeechRecognize:
    def __init__(self, audio_json_path, result_path):
        self.audio_json_path = audio_json_path
        self.result_path = result_path
        self.log_folder = os.path.join(dir_path, "speech_recognize_logs")
        os.makedirs(self.log_folder) if not os.path.exists(self.log_folder) else None
        self.do_recognize()

    def do_recognize(self):
        # exception 重試次數
        retries = 5
        test_date = str(time.strftime("%Y%m%d%H%M%S", time.localtime()))
        # 模組執行時的log, 等級為debug
        log_file = 'speech_recognize_{}.log'.format(test_date)
        file_handler = logging.FileHandler(encoding='utf-8', filename=os.path.join(self.log_folder, log_file))
        stdout_handler = logging.StreamHandler(sys.stdout)
        handlers = [file_handler, stdout_handler]
        logging.basicConfig(
            level=logging.DEBUG,
            format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
            handlers=handlers,
        )
        logger = logging.getLogger('SpeechLog')
        text_file = open(self.result_path, "w", encoding="utf-8")
        logger.info("Speech recognize starting.")

        # init recognizer
        r = speech_recognition.Recognizer()

        # 讀取辨識音檔 json
        with open(self.audio_json_path, encoding="utf-8") as reader:
            jf = json.loads(reader.read())

        json_result = dict()
        for index in tqdm(jf):
            for retry in range(retries):
                try:
                    # result的json dictionary
                    ocr_dict = dict()
                    ocr_result = "Fail"
                    ocr_course = 'File not found'
                    ocr_answer = ''
                    ocr_matches = int(jf[index]['matches'])
                    answers = jf[index]['answer'].split('^@^')
                    answer = jf[index]['answer']
                    audio_path = jf[index]['audio']
                    lang = jf[index]['lang']
                    passTimes = 0
                    if ocr_matches > len(answers):
                        ocr_course = 'Number of matches exceeds number of answers'
                    else:
                        if audio_path != '':
                            try:
                                # 開始辨識
                                with speech_recognition.AudioFile(audio_path) as source:
                                    audio_temp = r.record(source)
                                string_of_speech = r.recognize_google(audio_temp, language=lang)
                                ocr_answer = string_of_speech
                                if answer == '':
                                    # ocr_answer = string_of_speech
                                    ocr_result = ''
                                    ocr_course = ''
                                else:
                                    ocr_course = ''
                                    for temp_answer in answers:
                                        find_match_case = re.findall(temp_answer.lower(), string_of_speech.lower())
                                        str_match_case = len(find_match_case)
                                        if str_match_case > 1:
                                            ocr_course += '{} duplicate {} times^%^'.format(temp_answer, str_match_case)
                                            # ocr_answer += temp_answer + '^%^'
                                            passTimes += 1
                                        elif str_match_case == 1:
                                            ocr_course += '{} Pass^%^'.format(temp_answer)
                                            # ocr_answer += temp_answer + '^%^'
                                            passTimes += 1
                                        else:
                                            # 比對Answer結果, 以Levenshtein Distance演算法計算符合程度
                                            temp_data_list = string_of_speech.split('\n')
                                            result_value_list = []
                                            for ocr_str in temp_data_list:
                                                result_value_list.append(fuzz.ratio(temp_answer, ocr_str))
                                            match_value = max(result_value_list)
                                            match_index = result_value_list.index(match_value)
                                            ocr_course += '{} match {}%^%^'.format(temp_answer, match_value)
                                            # ocr_answer += temp_data_list[match_index] + '^%^'
                                    if passTimes >= ocr_matches:
                                        ocr_result = 'Pass'
                            except ValueError:
                                ocr_result = 'Fail'
                                ocr_course = 'Audio file format error'
                                ocr_answer = ''
                                logger.error(
                                    "Audio file could not be read as PCM WAV, AIFF/AIFF-C, or Native FLAC; check if file is corrupted or in another format")
                            except speech_recognition.UnknownValueError:
                                ocr_result = 'Fail'
                                ocr_course = 'Could not recognize'
                                ocr_answer = ''
                                logger.error("Google Speech Recognition could not understand audio")
                            except speech_recognition.RequestError as e1:
                                ocr_result = 'Fail'
                                ocr_course = 'RequestError'
                                ocr_answer = ''
                                logger.error(
                                    "Could not request results from Google Speech Recognition service; {0}".format(e1))
                    logger.info(
                        " --- Audio Recognize result --- answer : {} , audio : {} , result : {} , course : {} , recognize : {} , matches : {}".format(
                            answer, audio_path, ocr_result, ocr_course, ocr_answer, ocr_matches))
                    ocr_dict['answer'] = answer
                    ocr_dict['audio'] = audio_path
                    ocr_dict['lang'] = lang
                    ocr_dict['result'] = ocr_result
                    ocr_dict['course'] = ocr_course
                    ocr_dict['recognize'] = ocr_answer
                    ocr_dict['matches'] = ocr_matches
                    json_result[index] = ocr_dict
                    # json.dump(json_result, text_file, indent=4, ensure_ascii=False)
                except Exception as e:
                    print(e, flush=True)
                    logger.exception("Exception occurred", exc_info=True)
                    if retry < retries - 1:
                        continue
                    else:
                        break
                break
        json.dump(json_result, text_file, indent=4, ensure_ascii=False)
        logger.info("Result file : " + text_file.name)
        text_file.close()


if __name__ == '__main__':
    import argparse


    class ShowLang(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            print("support languages : \n" + json.dumps(langs_json,
                                                        sort_keys=True, indent=4,
                                                        ensure_ascii=False))


    ap = argparse.ArgumentParser()
    ap.add_argument("-p", required=True,
                    help="json file path of audio list")
    ap.add_argument("-r", required=True,
                    help="full file path of result json")

    ap.add_argument('--lang', action=ShowLang, nargs=0)
    args = vars(ap.parse_args())
    # # path, result_path, lang, auth
    if args['lang']:
        print(json.dumps(langs_json,
                         sort_keys=True, indent=4,
                         ensure_ascii=False))
    SpeechRecognize(audio_json_path=args['p'], result_path=args['r'])

    # SpeechRecognize('E://tmp.json', "E://vo.json")
    # TranslationModule("E:/TV/numbers/1/amount_17.json", "d:/kkkk.json", "")
