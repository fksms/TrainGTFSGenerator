import os
import glob
import zipfile
import datetime
import json
from typing import Tuple

import jpholiday

# GTFSデータの有効期間
start_date = datetime.date(2024, 1, 1)
end_date = datetime.date(2025, 12, 31)

# 各オペレーターの情報
operators_info = [
    # ---------------ODPTにあるやつ--------------- #
    # 東日本旅客鉄道（JR東日本）
    {
        "agency_id": "jreast",
        "agency_name": "JR東日本",
        "agency_name_en": "East Japan Railway",
        "agency_url": "",
        "gtfs_output_file_name": "JR-East-Train.gtfs.zip",
    },
    # 京王電鉄
    {
        "agency_id": "keio",
        "agency_name": "京王電鉄",
        "agency_name_en": "Keio Corporation",
        "agency_url": "",
        "gtfs_output_file_name": "Keio-Train.gtfs.zip",
    },
    # 首都圏新都市鉄道（つくばエクスプレス）
    {
        "agency_id": "mir",
        "agency_name": "首都圏新都市鉄道",
        "agency_name_en": "Metropolitan Intercity Railway",
        "agency_url": "",
        "gtfs_output_file_name": "MIR-Train.gtfs.zip",
    },
    # 相模鉄道（相鉄）
    {
        "agency_id": "sotetsu",
        "agency_name": "相模鉄道",
        "agency_name_en": "Sagami Railway",
        "agency_url": "",
        "gtfs_output_file_name": "Sotetsu-Train.gtfs.zip",
    },
    # 多摩都市モノレール
    {
        "agency_id": "tamamonorail",
        "agency_name": "多摩都市モノレール",
        "agency_name_en": "Tokyo Tama Intercity Monorail",
        "agency_url": "",
        "gtfs_output_file_name": "TamaMonorail-Train.gtfs.zip",
    },
    # 東武鉄道
    {
        "agency_id": "tobu",
        "agency_name": "東武鉄道",
        "agency_name_en": "Tobu Railway",
        "agency_url": "",
        "gtfs_output_file_name": "Tobu-Train.gtfs.zip",
    },
    # 東京都交通局
    {
        "agency_id": "toei",
        "agency_name": "東京都交通局",
        "agency_name_en": "Tokyo Metropolitan Bureau of Transportation",
        "agency_url": "",
        "gtfs_output_file_name": "Toei-Train.gtfs.zip",
    },
    # 東京メトロ
    {
        "agency_id": "tokyometro",
        "agency_name": "東京メトロ",
        "agency_name_en": "Tokyo Metro",
        "agency_url": "",
        "gtfs_output_file_name": "TokyoMetro-Train.gtfs.zip",
    },
    # 東京臨海高速鉄道
    {
        "agency_id": "twr",
        "agency_name": "東京臨海高速鉄道",
        "agency_name_en": "Tokyo Waterfront Area Rapid Transit",
        "agency_url": "",
        "gtfs_output_file_name": "TWR-Train.gtfs.zip",
    },
    # 横浜市交通局
    {
        "agency_id": "yokohamamunicipal",
        "agency_name": "横浜市交通局",
        "agency_name_en": "Yokohama City Transportation Bureau",
        "agency_url": "",
        "gtfs_output_file_name": "YokohamaMunicipal-Train.gtfs.zip",
    },
    # -----------ODPTにないやつ（欲しい）----------- #
    # 京急電鉄
    {
        "agency_id": "keikyu",
        "agency_name": "京急電鉄",
        "agency_name_en": "Keikyu Corporation",
        "agency_url": "",
        "gtfs_output_file_name": "Keikyu-Train.gtfs.zip",
    },
    # 京成電鉄
    {
        "agency_id": "keisei",
        "agency_name": "京成電鉄",
        "agency_name_en": "Keisei Electric Railway",
        "agency_url": "",
        "gtfs_output_file_name": "Keisei-Train.gtfs.zip",
    },
    # 小田急電鉄
    {
        "agency_id": "odakyu",
        "agency_name": "小田急電鉄",
        "agency_name_en": "Odakyu Electric Railway",
        "agency_url": "",
        "gtfs_output_file_name": "Odakyu-Train.gtfs.zip",
    },
    # 西武鉄道
    {
        "agency_id": "seibu",
        "agency_name": "西武鉄道",
        "agency_name_en": "Seibu Railway",
        "agency_url": "",
        "gtfs_output_file_name": "Seibu-Train.gtfs.zip",
    },
    # 東急電鉄
    {
        "agency_id": "tokyu",
        "agency_name": "東急電鉄",
        "agency_name_en": "Tokyu Corporation",
        "agency_url": "",
        "gtfs_output_file_name": "Tokyu-Train.gtfs.zip",
    },
    # 横浜高速鉄道（みなとみらい線）
    {
        "agency_id": "minatomirai",
        "agency_name": "横浜高速鉄道（みなとみらい線）",
        "agency_name_en": "Yokohama Minatomirai Railway",
        "agency_url": "",
        "gtfs_output_file_name": "Minatomirai-Train.gtfs.zip",
    },
    # 埼玉高速鉄道
    {
        "agency_id": "saitamarailway",
        "agency_name": "埼玉高速鉄道",
        "agency_name_en": "Saitama Railway",
        "agency_url": "",
        "gtfs_output_file_name": "SR-Train.gtfs.zip",
    },
    # 東葉高速鉄道
    {
        "agency_id": "toyorapid",
        "agency_name": "東葉高速鉄道",
        "agency_name_en": "Toyo Rapid Railway",
        "agency_url": "",
        "gtfs_output_file_name": "TOYO-Train.gtfs.zip",
    },
    # ゆりかもめ
    {
        "agency_id": "yurikamome",
        "agency_name": "ゆりかもめ",
        "agency_name_en": "Yurikamome",
        "agency_url": "",
        "gtfs_output_file_name": "Yurikamome-Train.gtfs.zip",
    },
    # --------ODPTにないやつ（どっちでもいい）-------- #
    # 東京モノレール
    {
        "agency_id": "tokyomonorail",
        "agency_name": "東京モノレール",
        "agency_name_en": "Tokyo Monorail",
        "agency_url": "",
        "gtfs_output_file_name": "TokyoMonorail-Train.gtfs.zip",
    },
    # 新京成電鉄
    {
        "agency_id": "shinkeisei",
        "agency_name": "新京成電鉄",
        "agency_name_en": "Shin-Keisei Electric Railway",
        "agency_url": "",
        "gtfs_output_file_name": "ShinKeisei-Train.gtfs.zip",
    },
    # 北総鉄道
    {
        "agency_id": "hokuso",
        "agency_name": "北総鉄道",
        "agency_name_en": "Hokuso-Railway",
        "agency_url": "",
        "gtfs_output_file_name": "Hokuso-Train.gtfs.zip",
    },
]


def main():

    # 祝日のリストを作成
    holidays = []
    for holiday in jpholiday.between(start_date, end_date):
        holidays.append(holiday[0])

    # dist内のzipファイルを全て削除
    for path in glob.glob("dist/*.zip"):
        os.remove(path)

    for operator_info in operators_info:

        # agency.txtの生成
        with open("dist/agency.txt", "w", encoding="UTF-8") as f:
            text = generate_agency_txt(operator_info)
            f.write(text)

        # calendar.txtの生成
        with open("dist/calendar.txt", "w", encoding="UTF-8") as f:
            text = generate_calendar_txt(start_date, end_date)
            f.write(text)

        # calendar_dates.txtの生成
        with open("dist/calendar_dates.txt", "w", encoding="UTF-8") as f:
            text = generate_calendar_dates_txt(holidays)
            f.write(text)

        # feed_info.txtの生成
        with open("dist/feed_info.txt", "w", encoding="UTF-8") as f:
            text = generate_feed_info_txt(operator_info, start_date, end_date)
            f.write(text)

        texts = generate_trips_stop_times_stops_routes_translations_txt(operator_info)

        # trips.txtの生成
        with open("dist/trips.txt", "w", encoding="UTF-8") as f:
            f.write(texts["trips_txt"])

        # routes.txtの生成
        with open("dist/routes.txt", "w", encoding="UTF-8") as f:
            f.write(texts["routes_txt"])

        # stops.txtの生成
        with open("dist/stops.txt", "w", encoding="UTF-8") as f:
            f.write(texts["stops_txt"])

        # stop_times.txtの生成
        with open("dist/stop_times.txt", "w", encoding="UTF-8") as f:
            f.write(texts["stop_times_txt"])

        # translations.txtの生成
        with open("dist/translations.txt", "w", encoding="UTF-8") as f:
            f.write(texts["translations_txt"])

        # zip圧縮
        with zipfile.ZipFile(
            "dist/" + operator_info["gtfs_output_file_name"],
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=-1,
        ) as zf:
            for path in glob.glob("dist/*.txt"):
                # zip書き込み
                zf.write(
                    path,
                    arcname=os.path.splitext(operator_info["gtfs_output_file_name"])[0] + "/" + os.path.basename(path),
                )

        # テキストファイルを全て削除
        for path in glob.glob("dist/*.txt"):
            os.remove(path)

        # 生成状況表示
        print('"' + operator_info["gtfs_output_file_name"] + '" ' + "Generated")


# agency.txtの生成
def generate_agency_txt(operator_info: dict) -> str:

    header = [
        "agency_id",
        "agency_name",
        "agency_url",
        "agency_timezone",
        "agency_lang",
        "agency_phone",
        "agency_fare_url",
        "agency_email",
    ]

    header_str = ",".join(header)

    body = [
        operator_info["agency_id"],
        operator_info["agency_name"],
        operator_info["agency_url"],
        "Asia/Tokyo",
        "ja",
        "",
        "",
        "",
    ]

    body_str = ",".join(body)

    return header_str + "\n" + body_str


# calendar.txtの生成
def generate_calendar_txt(start_date: datetime, end_date: datetime) -> str:

    header = [
        "service_id",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
        "start_date",
        "end_date",
    ]

    header_str = ",".join(header)

    body = []

    # 平日ダイヤ（"0"）
    body.append("0,1,1,1,1,1,0,0," + start_date.strftime("%Y%m%d") + "," + end_date.strftime("%Y%m%d"))

    # 土曜・日曜ダイヤ（"1"）
    body.append("1,0,0,0,0,0,1,1," + start_date.strftime("%Y%m%d") + "," + end_date.strftime("%Y%m%d"))

    # 土曜ダイヤ（"2"）
    body.append("2,0,0,0,0,0,1,0," + start_date.strftime("%Y%m%d") + "," + end_date.strftime("%Y%m%d"))

    # 日曜ダイヤ（"3"）
    body.append("3,0,0,0,0,0,0,1," + start_date.strftime("%Y%m%d") + "," + end_date.strftime("%Y%m%d"))

    body_str = "\n".join(body)

    return header_str + "\n" + body_str


# calendar_dates.txtの生成
def generate_calendar_dates_txt(holidays: list) -> str:

    header = [
        "service_id",
        "date",
        "exception_type",
    ]

    header_str = ",".join(header)

    body = []

    for holiday in holidays:
        # 祝日は平日ダイヤ（"0"）非適用（"2"）
        body.append("0," + holiday.strftime("%Y%m%d") + ",2")
        # 祝日は土曜・日曜（"1"）ダイヤ適用（"1"）
        body.append("1," + holiday.strftime("%Y%m%d") + ",1")
        # 祝日は日曜ダイヤ（"3"）適用（"1"）
        body.append("3," + holiday.strftime("%Y%m%d") + ",1")

    body_str = "\n".join(body)

    return header_str + "\n" + body_str


# feed_info.txtの生成
def generate_feed_info_txt(operator_info: dict, start_date: datetime, end_date: datetime) -> str:

    header = [
        "feed_publisher_name",
        "feed_publisher_url",
        "feed_lang",
        "feed_start_date",
        "feed_end_date",
        "feed_version",
        "feed_contact_email",
        "feed_contact_url",
    ]

    header_str = ",".join(header)

    body = [
        operator_info["agency_name"],
        operator_info["agency_url"],
        "ja",
        start_date.strftime("%Y%m%d"),
        end_date.strftime("%Y%m%d"),
        start_date.strftime("%Y%m%d"),
        "",
        "",
    ]

    body_str = ",".join(body)

    return header_str + "\n" + body_str


# trips.txt
# stop_times.txt
# stops.txt
# routes.txt
# translations.txtの生成
def generate_trips_stop_times_stops_routes_translations_txt(operator_info: dict) -> dict:

    # 列車時刻表の格納場所
    train_timetables_dirpath = "mini-tokyo-3d/data/train-timetables"

    # 列車種別表の格納場所
    railways_json_path = "mini-tokyo-3d/data/railways.json"

    # 駅情報の格納場所
    stations_json_path = "mini-tokyo-3d/data/stations.json"

    trips_header = [
        "route_id",
        "service_id",
        "trip_id",
        "trip_headsign",
        "trip_short_name",
        "direction_id",
        "block_id",
        "shape_id",
        "wheelchair_accessible",
        "bikes_allowed",
    ]

    stop_times_header = [
        "trip_id",
        "arrival_time",
        "departure_time",
        "stop_id",
        "stop_sequence",
        "stop_headsign",
        "pickup_type",
        "drop_off_type",
        "shape_dist_traveled",
        "timepoint",
    ]

    routes_header = [
        "route_id",
        "agency_id",
        "route_short_name",
        "route_long_name",
        "route_desc",
        "route_type",
        "route_url",
        "route_color",
        "route_text_color",
    ]

    stops_header = [
        "stop_id",
        "stop_code",
        "stop_name",
        "stop_desc",
        "stop_lat",
        "stop_lon",
        "zone_id",
        "stop_url",
        "location_type",
        "parent_station",
        "stop_timezone",
        "wheelchair_boarding",
    ]

    translations_header = [
        "table_name",
        "field_name",
        "field_value",
        "language",
        "translation",
    ]

    trips_header_str = ",".join(trips_header)
    stop_times_header_str = ",".join(stop_times_header)
    routes_header_str = ",".join(routes_header)
    stops_header_str = ",".join(stops_header)
    translations_header_str = ",".join(translations_header)

    trips_body = []
    stop_times_body = []
    routes_body = []
    stops_body = []
    translations_body = []

    translation = [
        "agency",
        "agency_name",
        operator_info["agency_name"],
        "ja",
        operator_info["agency_name"],
    ]

    translations_body.append(",".join(translation))

    translation = [
        "agency",
        "agency_name",
        operator_info["agency_name"],
        "en",
        operator_info["agency_name_en"],
    ]

    translations_body.append(",".join(translation))

    # "railways.json"をオブジェクトとして読み込み
    with open(railways_json_path, "r", encoding="UTF-8") as f:
        railways_obj = json.load(f)

    # "stations.json"をオブジェクトとして読み込み
    with open(stations_json_path, "r", encoding="UTF-8") as f:
        stations_obj = json.load(f)

    # "train-timetables/*.json"をオブジェクトとして読み込み
    for path in sorted(glob.glob(train_timetables_dirpath + "/" + operator_info["agency_id"] + "-*.json")):

        # --------------------------- バグ対処用（ここから） --------------------------- #
        # 鶴見線、鶴見海芝浦支線、鶴見大川支線の一部のタイムテーブルに
        # 時間が記載されていないものが存在し、処理ができないため、処理をスキップさせる。

        # -> バグ対処済みのsubmodule（https://github.com/fksms/mini-tokyo-3d.git）に切り替えたため、コメントアウト
        """
        if (
            path == "mini-tokyo-3d/data/train-timetables/jreast-tsurumi.json" or
            path == "mini-tokyo-3d/data/train-timetables/jreast-tsurumiokawabranch.json" or
            path == "mini-tokyo-3d/data/train-timetables/jreast-tsurumiumishibaurabranch.json"
        ):
            continue
        """
        # --------------------------- バグ対処用（ここまで） --------------------------- #

        with open(path, "r", encoding="UTF-8") as f:
            timetables_obj = json.load(f)

        # ==================== routes.txt、translations.txtの生成部分（ここから） ==================== #
        # 経路ID（0番目の要素のIDを取得）
        route_id = timetables_obj[0]["r"]

        # 経路情報オブジェクト
        route_obj = get_route_obj_from_route_id(railways_obj, route_id)

        route = [
            route_id,
            operator_info["agency_id"],
            "",
            route_obj["title"]["ja"],
            "",
            "2",  # 鉄道は"2"を指定する
            "",
            route_obj["color"][1:],  # カラーコードの最初の"#"を取り除く
            "",
        ]

        routes_body.append(",".join(route))

        translation = [
            "routes",
            "route_long_name",
            route_obj["title"]["ja"],
            "ja",
            route_obj["title"]["ja"],
        ]

        translations_body.append(",".join(translation))

        translation = [
            "routes",
            "route_long_name",
            route_obj["title"]["ja"],
            "en",
            route_obj["title"]["en"],
        ]

        translations_body.append(",".join(translation))
        # ==================== routes.txt、translations.txtの生成部分（ここまで） ==================== #

        # ==================== stops.txt、translations.txtの生成部分（ここから） ==================== #
        # 経路ID（0番目の要素のIDを取得）
        route_id = timetables_obj[0]["r"]

        # 駅情報を1要素ずつ処理
        for station_obj in stations_obj:
            if station_obj.get("railway") == route_id:

                stop = [
                    station_obj["id"],
                    "",
                    station_obj["title"]["ja"],
                    "",
                    str(station_obj["coord"][1]),
                    str(station_obj["coord"][0]),
                    station_obj["id"],
                    "",
                    "0",  # 鉄道は"0"を指定で良いはず
                    "",
                    "",
                    "",
                ]

                stops_body.append(",".join(stop))

                translation = [
                    "stops",
                    "stop_name",
                    station_obj["title"]["ja"],
                    "ja",
                    station_obj["title"]["ja"],
                ]

                translations_body.append(",".join(translation))

                translation = [
                    "stops",
                    "stop_name",
                    station_obj["title"]["ja"],
                    "en",
                    station_obj["title"]["en"],
                ]

                translations_body.append(",".join(translation))
        # ==================== stops.txt、translations.txtの生成部分（ここまで） ==================== #

        # 時刻表を1要素ずつ処理
        for timetable_obj in timetables_obj:

            # ==================== trips.txt、translations.txtの生成部分（ここから） ==================== #
            # 経路ID
            route_id = timetable_obj["r"]

            # 便ID
            trip_id = timetable_obj["id"]

            # 列車の方向
            direction = timetable_obj["d"]

            # 運行日ID
            service_id = get_service_id_from_trip_id(trip_id)

            # 終点の駅情報オブジェクト
            headsign_obj = get_station_obj_from_station_id(stations_obj, timetable_obj["ds"][0]) if "ds" in timetable_obj.keys() else None

            # 終点の駅名
            headsign = headsign_obj["title"]["ja"] if headsign_obj is not None else ""

            # 終点の駅名（英語）
            headsign_en = headsign_obj["title"]["en"] if headsign_obj is not None else ""

            # 経路情報オブジェクト
            route_obj = get_route_obj_from_route_id(railways_obj, route_id)

            # 方向ID（"ascending"と一致した場合は"0"、"descending"と一致した場合は"1"）
            direction_id = "0" if route_obj["ascending"] == direction else "1"

            # 便結合ID（路線を跨ぐような列車は、"block_id"に次の便IDを設定）
            block_id = timetable_obj["nt"][0] if "nt" in timetable_obj.keys() else ""

            trip = [
                route_id,
                service_id,
                trip_id,
                headsign,
                "",
                direction_id,
                block_id,
                "",
                "",
                "",
            ]

            trips_body.append(",".join(trip))

            translation = [
                "trips",
                "trip_headsign",
                headsign,
                "ja",
                headsign,
            ]

            translations_body.append(",".join(translation))

            translation = [
                "trips",
                "trip_headsign",
                headsign,
                "en",
                headsign_en,
            ]

            translations_body.append(",".join(translation))
            # ==================== trips.txt、translations.txtの生成部分（ここまで） ==================== #

            # ==================== stop_times.txtの生成部分（ここから） ==================== #
            # 経路ID
            route_id = timetable_obj["r"]

            # 便ID
            trip_id = timetable_obj["id"]

            # 列車の方向
            direction = timetable_obj["d"]

            # 経路情報オブジェクト
            route_obj = get_route_obj_from_route_id(railways_obj, route_id)

            # 出発駅
            origin_station = timetable_obj["os"][0] if "os" in timetable_obj.keys() else ""

            # 終点駅
            destination_station = timetable_obj["ds"][0] if "ds" in timetable_obj.keys() else ""

            # 該当経路を最初に通過・停車する駅
            start_station = timetable_obj["tt"][0]["s"]

            # 該当経路を最後に通過・停車する駅
            end_station = timetable_obj["tt"][-1]["s"]

            # --------------- 部分配列の作成（ここから） --------------- #
            # 経路の駅一覧リスト
            # （昇順"ascending"の場合はそのまま、降順"descending"の場合は反転させる）
            route_stations_list = route_obj["stations"] if route_obj["ascending"] == direction else list(reversed(route_obj["stations"]))

            # "start_station"の位置を前からサーチ
            start_index = route_stations_list.index(start_station)

            # "end_station"の位置を後ろからサーチ
            end_index = 0
            for i in range(len(route_stations_list) - 1, -1, -1):
                if route_stations_list[i] == end_station:
                    end_index = i
                    break

            # 部分集合の生成（該当の列車が実際に通る区間）
            stations_list_subset = route_stations_list[start_index: end_index + 1]
            # --------------- 部分配列の作成（ここまで） --------------- #

            stop_counter = 0

            # 通過・停車する駅を1要素ずつ処理
            for index, station in enumerate(stations_list_subset):
                # 停車
                if station == timetable_obj["tt"][stop_counter]["s"]:

                    # 出発時刻と到着時刻
                    arrival_time, departure_time = get_a_d_times_from_timetable_element(timetable_obj["tt"][stop_counter])

                    # 乗車可能なら0、乗車不可なら1
                    pickup_type = "1" if station == destination_station else "0"

                    # 降車可能なら0、降車不可なら1
                    drop_off_type = "1" if station == origin_station else "0"

                    stop_time = [
                        trip_id,
                        arrival_time + ":00",
                        departure_time + ":00",
                        station,
                        str(index + 1),
                        "",
                        pickup_type,
                        drop_off_type,
                        "",
                        "1",  # 1を設定
                    ]

                    stop_times_body.append(",".join(stop_time))

                    stop_counter += 1

                # 通過
                else:

                    stop_time = [
                        trip_id,
                        "",
                        "",
                        station,
                        str(index + 1),
                        "",
                        "1",  # 乗車不可
                        "1",  # 降車不可
                        "",
                        "1",  # 1を設定
                    ]

                    stop_times_body.append(",".join(stop_time))

            # ==================== stop_times.txtの生成部分（ここまで） ==================== #

    # ソート
    translations_body.sort()

    # 重複削除
    translations_body = list(dict.fromkeys(translations_body))

    # 結合
    routes_body_str = "\n".join(routes_body)
    stops_body_str = "\n".join(stops_body)
    trips_body_str = "\n".join(trips_body)
    stop_times_body_str = "\n".join(stop_times_body)
    translations_body_str = "\n".join(translations_body)

    return {
        "routes_txt": routes_header_str + "\n" + routes_body_str,
        "stops_txt": stops_header_str + "\n" + stops_body_str,
        "trips_txt": trips_header_str + "\n" + trips_body_str,
        "stop_times_txt": stop_times_header_str + "\n" + stop_times_body_str,
        "translations_txt": translations_header_str + "\n" + translations_body_str,
    }


# 便IDから運行日IDに変換
def get_service_id_from_trip_id(trip_id: str) -> str:

    if "Weekday" in trip_id:
        return "0"  # 平日ダイヤ（"0"）

    elif "SaturdayHoliday" in trip_id:
        return "1"  # 土曜・日曜ダイヤ（"1"）

    elif "Saturday" in trip_id:
        return "2"  # 土曜ダイヤ（"2"）

    elif "Holiday" in trip_id:
        return "3"  # 日曜ダイヤ（"3"）

    else:
        print("定義されていない運行区分です。")
        return "-1"


# 全ての駅情報が格納されたオブジェクトを利用して、駅IDと一致する駅情報オブジェクトを探索
def get_station_obj_from_station_id(stations_obj: dict, station_id: str) -> dict:
    for station_obj in stations_obj:
        if station_id == station_obj["id"]:
            return station_obj


# 全ての経路情報が格納されたオブジェクトを利用して、経路IDと一致する経路情報オブジェクトを探索
def get_route_obj_from_route_id(routes_obj: dict, route_id: str) -> dict:
    for route_obj in routes_obj:
        if route_id == route_obj["id"]:
            return route_obj


# タイムテーブルの要素から、到着時刻と出発時刻を抽出
def get_a_d_times_from_timetable_element(element: dict) -> Tuple[str, str]:

    # "a"と"d"のどちらも存在する場合
    if "a" in element.keys() and "d" in element.keys():  # キーチェック
        return element["a"], element["d"]

    # "a"のみ存在する場合
    elif "a" in element.keys():  # キーチェック
        return element["a"], element["a"]

    # "d"のみ存在する場合
    elif "d" in element.keys():  # キーチェック
        return element["d"], element["d"]

    # "a"と"d"のどちらも存在しない場合
    else:
        print("不適切なタイムテーブルが存在します。")
        return None


if __name__ == "__main__":
    main()
