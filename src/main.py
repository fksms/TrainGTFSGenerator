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
operatorsInfo = [
    # ---------------ODPTにあるやつ--------------- #
    # 東日本旅客鉄道（JR東日本）
    {
        "agency_id": "jreast",
        "agency_name": "JR東日本",
        "agency_url": "",
        "railway_id": "JR-East",
        "gtfs_output_file_name": "JR-East-Train.gtfs.zip",
    },
    # 京王電鉄
    {
        "agency_id": "keio",
        "agency_name": "京王電鉄",
        "agency_url": "",
        "railway_id": "Keio",
        "gtfs_output_file_name": "Keio-Train.gtfs.zip",
    },
    # 首都圏新都市鉄道（つくばエクスプレス）
    {
        "agency_id": "mir",
        "agency_name": "首都圏新都市鉄道",
        "agency_url": "",
        "railway_id": "MIR",
        "gtfs_output_file_name": "MIR-Train.gtfs.zip",
    },
    # 相模鉄道（相鉄）
    {
        "agency_id": "sotetsu",
        "agency_name": "相模鉄道",
        "agency_url": "",
        "railway_id": "Sotetsu",
        "gtfs_output_file_name": "Sotetsu-Train.gtfs.zip",
    },
    # 多摩都市モノレール
    {
        "agency_id": "tamamonorail",
        "agency_name": "多摩都市モノレール",
        "agency_url": "",
        "railway_id": "TamaMonorail",
        "gtfs_output_file_name": "TamaMonorail-Train.gtfs.zip",
    },
    # 東武鉄道
    {
        "agency_id": "tobu",
        "agency_name": "東武鉄道",
        "agency_url": "",
        "railway_id": "Tobu",
        "gtfs_output_file_name": "Tobu-Train.gtfs.zip",
    },
    # 東京都交通局
    {
        "agency_id": "toei",
        "agency_name": "東京都交通局",
        "agency_url": "",
        "railway_id": "Toei",
        "gtfs_output_file_name": "Toei-Train.gtfs.zip",
    },
    # 東京メトロ
    {
        "agency_id": "tokyometro",
        "agency_name": "東京メトロ",
        "agency_url": "",
        "railway_id": "TokyoMetro",
        "gtfs_output_file_name": "TokyoMetro-Train.gtfs.zip",
    },
    # 東京臨海高速鉄道
    {
        "agency_id": "twr",
        "agency_name": "東京臨海高速鉄道",
        "agency_url": "",
        "railway_id": "TWR",
        "gtfs_output_file_name": "TWR-Train.gtfs.zip",
    },
    # 横浜市交通局
    {
        "agency_id": "yokohamamunicipal",
        "agency_name": "横浜市交通局",
        "agency_url": "",
        "railway_id": "YokohamaMunicipal",
        "gtfs_output_file_name": "YokohamaMunicipal-Train.gtfs.zip",
    },
    # -----------ODPTにないやつ（欲しい）----------- #
    # 京急電鉄
    {
        "agency_id": "keikyu",
        "agency_name": "京急電鉄",
        "agency_url": "",
        "railway_id": "Keikyu",
        "gtfs_output_file_name": "Keikyu-Train.gtfs.zip",
    },
    # 京成電鉄
    {
        "agency_id": "keisei",
        "agency_name": "京成電鉄",
        "agency_url": "",
        "railway_id": "Keisei",
        "gtfs_output_file_name": "Keisei-Train.gtfs.zip",
    },
    # 小田急電鉄
    {
        "agency_id": "odakyu",
        "agency_name": "小田急電鉄",
        "agency_url": "",
        "railway_id": "Odakyu",
        "gtfs_output_file_name": "Odakyu-Train.gtfs.zip",
    },
    # 西武鉄道
    {
        "agency_id": "seibu",
        "agency_name": "西武鉄道",
        "agency_url": "",
        "railway_id": "Seibu",
        "gtfs_output_file_name": "Seibu-Train.gtfs.zip",
    },
    # 東急電鉄
    {
        "agency_id": "tokyu",
        "agency_name": "東急電鉄",
        "agency_url": "",
        "railway_id": "Tokyu",
        "gtfs_output_file_name": "Tokyu-Train.gtfs.zip",
    },
    # 横浜高速鉄道（みなとみらい線）
    {
        "agency_id": "minatomirai",
        "agency_name": "横浜高速鉄道（みなとみらい線）",
        "agency_url": "",
        "railway_id": "Minatomirai",
        "gtfs_output_file_name": "Minatomirai-Train.gtfs.zip",
    },
    # 埼玉高速鉄道
    {
        "agency_id": "saitamarailway",
        "agency_name": "埼玉高速鉄道",
        "agency_url": "",
        "railway_id": "SaitamaRailway",
        "gtfs_output_file_name": "SR-Train.gtfs.zip",
    },
    # 東葉高速鉄道
    {
        "agency_id": "toyorapid",
        "agency_name": "東葉高速鉄道",
        "agency_url": "",
        "railway_id": "ToyoRapid",
        "gtfs_output_file_name": "TOYO-Train.gtfs.zip",
    },
    # ゆりかもめ
    {
        "agency_id": "yurikamome",
        "agency_name": "ゆりかもめ",
        "agency_url": "",
        "railway_id": "Yurikamome",
        "gtfs_output_file_name": "Yurikamome-Train.gtfs.zip",
    },
    # --------ODPTにないやつ（どっちでもいい）-------- #
    # 東京モノレール
    {
        "agency_id": "tokyomonorail",
        "agency_name": "東京モノレール",
        "agency_url": "",
        "railway_id": "TokyoMonorail",
        "gtfs_output_file_name": "TokyoMonorail-Train.gtfs.zip",
    },
    # 新京成電鉄
    {
        "agency_id": "shinkeisei",
        "agency_name": "新京成電鉄",
        "agency_url": "",
        "railway_id": "ShinKeisei",
        "gtfs_output_file_name": "ShinKeisei-Train.gtfs.zip",
    },
    # 北総鉄道
    {
        "agency_id": "hokuso",
        "agency_name": "北総鉄道",
        "agency_url": "",
        "railway_id": "Hokuso",
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

    for operatorInfo in operatorsInfo:

        # agency.txtの生成
        with open("dist/agency.txt", "w", encoding="UTF-8") as f:
            text = generate_agency_txt(operatorInfo)
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
            text = generate_feed_info_txt(operatorInfo, start_date, end_date)
            f.write(text)

        # routes.txtの生成
        with open("dist/routes.txt", "w", encoding="UTF-8") as f:
            text = generate_routes_txt(operatorInfo)
            f.write(text)

        # zip圧縮
        with zipfile.ZipFile(
            "dist/" + operatorInfo["gtfs_output_file_name"],
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=-1,
        ) as zf:
            for path in glob.glob("dist/*.txt"):
                # zip書き込み
                zf.write(
                    path,
                    arcname=os.path.splitext(operatorInfo["gtfs_output_file_name"])[0]
                    + "/"
                    + os.path.basename(path),
                )

        # テキストファイルを全て削除
        for path in glob.glob("dist/*.txt"):
            os.remove(path)

        # 生成状況表示
        print('"' + operatorInfo["gtfs_output_file_name"] + '" ' + "Generated")


# agency.txtの生成
def generate_agency_txt(operatorInfo: dict) -> str:

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

    headerStr = ",".join(header)

    body = [
        operatorInfo["agency_id"],
        operatorInfo["agency_name"],
        operatorInfo["agency_url"],
        "Asia/Tokyo",
        "ja",
        "",
        "",
        "",
    ]

    bodyStr = ",".join(body)

    return headerStr + "\n" + bodyStr


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

    headerStr = ",".join(header)

    body = []

    # 1番目の"0"は平日の運行区分、2〜8番目はを各曜日の運行区分（0なら非適用、1なら適用）を指している
    body.append(
        "0,1,1,1,1,1,0,0,"
        + start_date.strftime("%Y%m%d")
        + ","
        + end_date.strftime("%Y%m%d")
    )
    # 1番目の"1"は休日の運行区分、2〜8番目はを各曜日の運行区分（0なら非適用、1なら適用）を指している
    body.append(
        "1,0,0,0,0,0,1,1,"
        + start_date.strftime("%Y%m%d")
        + ","
        + end_date.strftime("%Y%m%d")
    )

    bodyStr = "\n".join(body)

    return headerStr + "\n" + bodyStr


# calendar_dates.txtの生成
def generate_calendar_dates_txt(holidays: list) -> str:

    header = [
        "service_id",
        "date",
        "exception_type",
    ]

    headerStr = ",".join(header)

    body = []

    for holiday in holidays:
        # 最初の"0"は平日の運行区分、最後の"2"は運行区分非適用であることを指している
        body.append("0," + holiday.strftime("%Y%m%d") + ",2")
        # 最初の"1"は休日の運行区分、最後の"1"は運行区分適用であることを指している
        body.append("1," + holiday.strftime("%Y%m%d") + ",1")

    bodyStr = "\n".join(body)

    return headerStr + "\n" + bodyStr


# feed_info.txtの生成
def generate_feed_info_txt(
    operatorInfo: dict, start_date: datetime, end_date: datetime
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

    headerStr = ",".join(header)

    body = [
        operatorInfo["agency_name"],
        operatorInfo["agency_url"],
        "ja",
        start_date.strftime("%Y%m%d"),
        end_date.strftime("%Y%m%d"),
        start_date.strftime("%Y%m%d"),
        "",
        "",
    ]

    bodyStr = ",".join(body)

    return headerStr + "\n" + bodyStr


# routes.txtの生成
def generate_routes_txt(operatorInfo: dict) -> str:

    header = [
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

    headerStr = ",".join(header)

    body = []

    # ターゲットとなるJSONのパス
    target_json_path = "mini-tokyo-3d/data/railways.json"

    # JSONをオブジェクトとして読み込み
    with open(target_json_path, "r", encoding="UTF-8") as f:
        railways_obj = json.load(f)

    # route_id
    route_id = 1

    for railway_obj in railways_obj:
        # 部分一致
        if operatorInfo["railway_id"] in railway_obj["id"]:
            route_name = railway_obj["title"]["ja"]
            route_color = railway_obj["color"][1:]  # カラーコードの最初の"#"を取り除く

            route = [
                str(route_id),
                operatorInfo["agency_id"],
                "",
                route_name,
                "",
                "2",  # 鉄道は"2"を指定する
                "",
                route_color,
                "",
            ]

            body.append(",".join(route))
            route_id += 1

    bodyStr = "\n".join(body)

    return headerStr + "\n" + bodyStr


if __name__ == "__main__":
    main()
