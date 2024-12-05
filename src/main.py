import os
import glob
import zipfile
import datetime

import jpholiday

# ダイヤの有効期間
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

    for operatorInfo in operatorsInfo:

        # agency.txtの生成
        file = open("dist/agency.txt", "w", encoding="UTF-8")
        text = generate_agency_txt(operatorInfo)
        file.write(text)
        file.close()

        # calendar.txtの生成
        file = open("dist/calendar.txt", "w", encoding="UTF-8")
        text = generate_calendar_txt(start_date, end_date)
        file.write(text)
        file.close()

        # calendar_dates.txtの生成
        file = open("dist/calendar_dates.txt", "w", encoding="UTF-8")
        text = generate_calendar_dates_txt(holidays)
        file.write(text)
        file.close()

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


if __name__ == "__main__":
    main()
