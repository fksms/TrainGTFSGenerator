import os
import glob
import zipfile
import datetime
import json

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
        "agency_url": "",
        "gtfs_output_file_name": "JR-East-Train.gtfs.zip",
    },
    # 京王電鉄
    {
        "agency_id": "keio",
        "agency_name": "京王電鉄",
        "agency_url": "",
        "gtfs_output_file_name": "Keio-Train.gtfs.zip",
    },
    # 首都圏新都市鉄道（つくばエクスプレス）
    {
        "agency_id": "mir",
        "agency_name": "首都圏新都市鉄道",
        "agency_url": "",
        "gtfs_output_file_name": "MIR-Train.gtfs.zip",
    },
    # 相模鉄道（相鉄）
    {
        "agency_id": "sotetsu",
        "agency_name": "相模鉄道",
        "agency_url": "",
        "gtfs_output_file_name": "Sotetsu-Train.gtfs.zip",
    },
    # 多摩都市モノレール
    {
        "agency_id": "tamamonorail",
        "agency_name": "多摩都市モノレール",
        "agency_url": "",
        "gtfs_output_file_name": "TamaMonorail-Train.gtfs.zip",
    },
    # 東武鉄道
    {
        "agency_id": "tobu",
        "agency_name": "東武鉄道",
        "agency_url": "",
        "gtfs_output_file_name": "Tobu-Train.gtfs.zip",
    },
    # 東京都交通局
    {
        "agency_id": "toei",
        "agency_name": "東京都交通局",
        "agency_url": "",
        "gtfs_output_file_name": "Toei-Train.gtfs.zip",
    },
    # 東京メトロ
    {
        "agency_id": "tokyometro",
        "agency_name": "東京メトロ",
        "agency_url": "",
        "gtfs_output_file_name": "TokyoMetro-Train.gtfs.zip",
    },
    # 東京臨海高速鉄道
    {
        "agency_id": "twr",
        "agency_name": "東京臨海高速鉄道",
        "agency_url": "",
        "gtfs_output_file_name": "TWR-Train.gtfs.zip",
    },
    # 横浜市交通局
    {
        "agency_id": "yokohamamunicipal",
        "agency_name": "横浜市交通局",
        "agency_url": "",
        "gtfs_output_file_name": "YokohamaMunicipal-Train.gtfs.zip",
    },
    # -----------ODPTにないやつ（欲しい）----------- #
    # 京急電鉄
    {
        "agency_id": "keikyu",
        "agency_name": "京急電鉄",
        "agency_url": "",
        "gtfs_output_file_name": "Keikyu-Train.gtfs.zip",
    },
    # 京成電鉄
    {
        "agency_id": "keisei",
        "agency_name": "京成電鉄",
        "agency_url": "",
        "gtfs_output_file_name": "Keisei-Train.gtfs.zip",
    },
    # 小田急電鉄
    {
        "agency_id": "odakyu",
        "agency_name": "小田急電鉄",
        "agency_url": "",
        "gtfs_output_file_name": "Odakyu-Train.gtfs.zip",
    },
    # 西武鉄道
    {
        "agency_id": "seibu",
        "agency_name": "西武鉄道",
        "agency_url": "",
        "gtfs_output_file_name": "Seibu-Train.gtfs.zip",
    },
    # 東急電鉄
    {
        "agency_id": "tokyu",
        "agency_name": "東急電鉄",
        "agency_url": "",
        "gtfs_output_file_name": "Tokyu-Train.gtfs.zip",
    },
    # 横浜高速鉄道（みなとみらい線）
    {
        "agency_id": "minatomirai",
        "agency_name": "横浜高速鉄道（みなとみらい線）",
        "agency_url": "",
        "gtfs_output_file_name": "Minatomirai-Train.gtfs.zip",
    },
    # 埼玉高速鉄道
    {
        "agency_id": "saitamarailway",
        "agency_name": "埼玉高速鉄道",
        "agency_url": "",
        "gtfs_output_file_name": "SR-Train.gtfs.zip",
    },
    # 東葉高速鉄道
    {
        "agency_id": "toyorapid",
        "agency_name": "東葉高速鉄道",
        "agency_url": "",
        "gtfs_output_file_name": "TOYO-Train.gtfs.zip",
    },
    # ゆりかもめ
    {
        "agency_id": "yurikamome",
        "agency_name": "ゆりかもめ",
        "agency_url": "",
        "gtfs_output_file_name": "Yurikamome-Train.gtfs.zip",
    },
    # --------ODPTにないやつ（どっちでもいい）-------- #
    # 東京モノレール
    {
        "agency_id": "tokyomonorail",
        "agency_name": "東京モノレール",
        "agency_url": "",
        "gtfs_output_file_name": "TokyoMonorail-Train.gtfs.zip",
    },
    # 新京成電鉄
    {
        "agency_id": "shinkeisei",
        "agency_name": "新京成電鉄",
        "agency_url": "",
        "gtfs_output_file_name": "ShinKeisei-Train.gtfs.zip",
    },
    # 北総鉄道
    {
        "agency_id": "hokuso",
        "agency_name": "北総鉄道",
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

        # trips.txtの生成
        with open("dist/trips.txt", "w", encoding="UTF-8") as f:
            text = generate_trips_stop_times_stops_routes_txt(operator_info)[
                "trips_txt"
            ]
            f.write(text)

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
                    arcname=os.path.splitext(operator_info["gtfs_output_file_name"])[0]
                    + "/"
                    + os.path.basename(path),
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
    body.append(
        "0,1,1,1,1,1,0,0,"
        + start_date.strftime("%Y%m%d")
        + ","
        + end_date.strftime("%Y%m%d")
    )
    # 土曜・日曜ダイヤ（"1"）
    body.append(
        "1,0,0,0,0,0,1,1,"
        + start_date.strftime("%Y%m%d")
        + ","
        + end_date.strftime("%Y%m%d")
    )
    # 土曜ダイヤ（"2"）
    body.append(
        "2,0,0,0,0,0,1,0,"
        + start_date.strftime("%Y%m%d")
        + ","
        + end_date.strftime("%Y%m%d")
    )
    # 日曜ダイヤ（"3"）
    body.append(
        "3,0,0,0,0,0,0,1,"
        + start_date.strftime("%Y%m%d")
        + ","
        + end_date.strftime("%Y%m%d")
    )

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
def generate_feed_info_txt(
    operator_info: dict, start_date: datetime, end_date: datetime
) -> str:

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
# routes.txtの生成
def generate_trips_stop_times_stops_routes_txt(operator_info: dict) -> dict:

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

    trips_header_str = ",".join(trips_header)
    stop_times_header_str = ",".join(stop_times_header)
    routes_header_str = ",".join(routes_header)
    stops_header_str = ",".join(stops_header)

    trips_body = []
    stop_times_body = []
    routes_body = []
    stops_body = []

    # "railways.json"をオブジェクトとして読み込み
    with open(railways_json_path, "r", encoding="UTF-8") as f:
        railways_obj = json.load(f)

    # "stations.json"をオブジェクトとして読み込み
    with open(stations_json_path, "r", encoding="UTF-8") as f:
        stations_obj = json.load(f)

    # "train-timetables/*.json"をオブジェクトとして読み込み
    for path in glob.glob(
        train_timetables_dirpath + "/" + operator_info["agency_id"] + "-*.json"
    ):
        with open(path, "r", encoding="UTF-8") as f:
            timetables_obj = json.load(f)

        # 時刻表を1要素ずつ処理
        for timetable_obj in timetables_obj:

            # 経路ID
            route_id = timetable_obj["r"]

            # 便ID
            trip_id = timetable_obj["id"]

            # 列車の方向
            direction = timetable_obj["d"]

            # 運行日ID
            service_id = trip_id_2_service_id(trip_id)

            # 終点の駅名（山手線等、終点が設定されていないものもあるので、"ds"が存在するかを先に確認）
            headsign = ""
            if "ds" in timetable_obj.keys():
                # （"ds"が複数設定されているものが存在しており、0要素目を選択する形で問題無いか検討中）
                headsign_obj = station_id_2_station_obj(
                    stations_obj, timetable_obj["ds"][0]
                )
                headsign = headsign_obj["title"]["ja"]

            # 経路情報オブジェクト
            route_obj = route_id_2_route_obj(railways_obj, route_id)

            # 方向ID（"ascending"と一致した場合は"0"、"descending"と一致した場合は"1"）
            direction_id = "0" if route_obj["ascending"] == direction else "1"

            # 便結合ID（路線を跨ぐような列車は、"block_id"に次の便IDを設定。設定されていないものもあるので、"nt"が存在するかを先に確認）
            block_id = ""
            if "nt" in timetable_obj.keys():
                # （"nt"が複数設定されているものが存在しており、0要素目を選択する形で問題無いか検討中）
                block_id = timetable_obj["nt"][0]

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

    trips_body_str = "\n".join(trips_body)

    return {"trips_txt": trips_header_str + "\n" + trips_body_str}


# 便IDから運行日IDに変換
def trip_id_2_service_id(trip_id: str) -> str:

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
def station_id_2_station_obj(stations_obj: dict, station_id: str) -> dict:
    for station_obj in stations_obj:
        if station_id == station_obj["id"]:
            return station_obj


# 全ての経路情報が格納されたオブジェクトを利用して、経路IDと一致する経路情報オブジェクトを探索
def route_id_2_route_obj(routes_obj: dict, route_id: str) -> dict:
    for route_obj in routes_obj:
        if route_id == route_obj["id"]:
            return route_obj


if __name__ == "__main__":
    main()
