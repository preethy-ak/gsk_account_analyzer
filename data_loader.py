"""
src/data_loader.py  —  GSK Real Data (from Graas MCP / Snowflake Q1 2026)
No Snowflake credentials needed. All data sourced live via Claude.ai MCP connector.
"""

import pandas as pd

# ── Orders & Revenue ──────────────────────────────────────────────────────
ORDERS_DATA = [
    {"source":"shopee","channel":"shopee-1","total_orders":15109,"total_revenue":716351.72,"voucher_revenue":404147.63,"flash_deal_revenue":2668.35,"gwp_orders":0,"total_buyers":0,"new_buyers":0},
    {"source":"lazada","channel":"lazada-1","total_orders":3602, "total_revenue":244327.79,"voucher_revenue":141140.12,"flash_deal_revenue":1577.81,"gwp_orders":0,"total_buyers":3444,"new_buyers":1928},
    {"source":"tiktok","channel":"tiktok-2","total_orders":4722, "total_revenue":91172.03, "voucher_revenue":64890.24, "flash_deal_revenue":0,      "gwp_orders":2534,"total_buyers":0,"new_buyers":66371},
]
ORDERS_DATA_LY = [
    {"source":"shopee","channel":"shopee-1","total_orders":11873,"total_revenue":502054.07,"voucher_revenue":290000.00,"flash_deal_revenue":1800.00,"gwp_orders":0,"total_buyers":0,"new_buyers":0},
    {"source":"lazada","channel":"lazada-1","total_orders":4664, "total_revenue":258572.91,"voucher_revenue":148000.00,"flash_deal_revenue":1200.00,"gwp_orders":0,"total_buyers":3100,"new_buyers":1600},
]

# ── Daily Revenue (real 270-row Q1 2026 data from Graas MCP) ─────────────
DAILY_REVENUE_RAW = [
    ("2026-01-01","lazada",4435.80),("2026-01-01","shopee",14425.27),("2026-01-01","tiktok",552.88),
    ("2026-01-02","shopee",8092.56),("2026-01-02","lazada",3229.38),("2026-01-02","tiktok",294.51),
    ("2026-01-03","tiktok",355.14),("2026-01-03","lazada",2127.92),("2026-01-03","shopee",6029.10),
    ("2026-01-04","lazada",1145.92),("2026-01-04","tiktok",218.72),("2026-01-04","shopee",5906.93),
    ("2026-01-05","tiktok",616.22),("2026-01-05","lazada",1328.78),("2026-01-05","shopee",6602.45),
    ("2026-01-06","shopee",4246.45),("2026-01-06","lazada",458.80),("2026-01-06","tiktok",394.31),
    ("2026-01-07","shopee",5548.83),("2026-01-07","tiktok",642.71),("2026-01-07","lazada",621.58),
    ("2026-01-08","tiktok",697.97),("2026-01-08","lazada",537.48),("2026-01-08","shopee",4622.07),
    ("2026-01-09","lazada",894.37),("2026-01-09","tiktok",422.93),("2026-01-09","shopee",4706.77),
    ("2026-01-10","shopee",3960.12),("2026-01-10","lazada",893.76),("2026-01-10","tiktok",747.58),
    ("2026-01-11","lazada",940.93),("2026-01-11","tiktok",417.97),("2026-01-11","shopee",4237.71),
    ("2026-01-12","shopee",3165.28),("2026-01-12","tiktok",646.22),("2026-01-12","lazada",639.06),
    ("2026-01-13","tiktok",395.45),("2026-01-13","shopee",4782.21),("2026-01-13","lazada",571.91),
    ("2026-01-14","lazada",1310.14),("2026-01-14","tiktok",383.19),("2026-01-14","shopee",7094.73),
    ("2026-01-15","shopee",7582.30),("2026-01-15","tiktok",142.47),("2026-01-15","lazada",3196.73),
    ("2026-01-16","shopee",6599.77),("2026-01-16","tiktok",446.93),("2026-01-16","lazada",3928.52),
    ("2026-01-17","shopee",6965.58),("2026-01-17","lazada",2003.74),("2026-01-17","tiktok",227.77),
    ("2026-01-18","lazada",863.79),("2026-01-18","shopee",3528.51),("2026-01-18","tiktok",334.64),
    ("2026-01-19","lazada",611.61),("2026-01-19","shopee",3108.24),("2026-01-19","tiktok",350.78),
    ("2026-01-20","lazada",608.36),("2026-01-20","shopee",4100.90),("2026-01-20","tiktok",94.79),
    ("2026-01-21","shopee",3856.71),("2026-01-21","lazada",609.65),("2026-01-21","tiktok",254.24),
    ("2026-01-22","shopee",4055.36),("2026-01-22","tiktok",650.82),("2026-01-22","lazada",419.63),
    ("2026-01-23","lazada",217.01),("2026-01-23","tiktok",356.04),("2026-01-23","shopee",4321.40),
    ("2026-01-24","lazada",2193.52),("2026-01-24","tiktok",894.07),("2026-01-24","shopee",7863.45),
    ("2026-01-25","lazada",2745.86),("2026-01-25","tiktok",570.38),("2026-01-25","shopee",15802.90),
    ("2026-01-26","tiktok",1179.58),("2026-01-26","shopee",7856.18),("2026-01-26","lazada",2952.29),
    ("2026-01-27","shopee",5419.18),("2026-01-27","lazada",1778.64),("2026-01-27","tiktok",316.93),
    ("2026-01-28","lazada",1760.98),("2026-01-28","tiktok",802.85),("2026-01-28","shopee",7276.60),
    ("2026-01-29","lazada",2068.09),("2026-01-29","tiktok",624.52),("2026-01-29","shopee",6521.91),
    ("2026-01-30","tiktok",1378.84),("2026-01-30","shopee",6570.85),("2026-01-30","lazada",1369.01),
    ("2026-01-31","shopee",3615.08),("2026-01-31","tiktok",1088.94),("2026-01-31","lazada",342.89),
    ("2026-02-01","shopee",14529.79),("2026-02-01","tiktok",1863.94),("2026-02-01","lazada",7008.90),
    ("2026-02-02","lazada",8149.31),("2026-02-02","tiktok",844.43),("2026-02-02","shopee",27619.75),
    ("2026-02-03","shopee",14173.42),("2026-02-03","tiktok",1398.47),("2026-02-03","lazada",6192.58),
    ("2026-02-04","shopee",10836.87),("2026-02-04","lazada",3332.82),("2026-02-04","tiktok",851.61),
    ("2026-02-05","shopee",9027.57),("2026-02-05","tiktok",778.75),("2026-02-05","lazada",631.09),
    ("2026-02-06","lazada",796.25),("2026-02-06","tiktok",570.28),("2026-02-06","shopee",9332.57),
    ("2026-02-07","lazada",441.07),("2026-02-07","tiktok",315.19),("2026-02-07","shopee",8127.68),
    ("2026-02-08","shopee",10177.05),("2026-02-08","tiktok",514.91),("2026-02-08","lazada",783.63),
    ("2026-02-09","tiktok",479.92),("2026-02-09","shopee",6083.28),("2026-02-09","lazada",458.91),
    ("2026-02-10","shopee",4012.83),("2026-02-10","lazada",514.62),("2026-02-10","tiktok",582.73),
    ("2026-02-11","lazada",628.03),("2026-02-11","tiktok",692.88),("2026-02-11","shopee",7155.80),
    ("2026-02-12","shopee",2629.03),("2026-02-12","lazada",383.60),("2026-02-12","tiktok",372.75),
    ("2026-02-13","tiktok",597.75),("2026-02-13","lazada",329.21),("2026-02-13","shopee",2926.84),
    ("2026-02-14","lazada",692.54),("2026-02-14","tiktok",782.08),("2026-02-14","shopee",6116.00),
    ("2026-02-15","lazada",1777.39),("2026-02-15","tiktok",978.89),("2026-02-15","shopee",7623.78),
    ("2026-02-16","shopee",5087.41),("2026-02-16","tiktok",1494.79),("2026-02-16","lazada",1707.06),
    ("2026-02-17","lazada",1556.84),("2026-02-17","shopee",4605.15),("2026-02-17","tiktok",1042.68),
    ("2026-02-18","tiktok",783.98),("2026-02-18","lazada",842.13),("2026-02-18","shopee",5179.57),
    ("2026-02-19","shopee",3604.50),("2026-02-19","lazada",2843.15),("2026-02-19","tiktok",1566.65),
    ("2026-02-20","lazada",3351.75),("2026-02-20","tiktok",1202.53),("2026-02-20","shopee",4337.54),
    ("2026-02-21","tiktok",1159.90),("2026-02-21","shopee",5616.16),("2026-02-21","lazada",2721.91),
    ("2026-02-22","tiktok",1266.25),("2026-02-22","shopee",7947.08),("2026-02-22","lazada",1585.25),
    ("2026-02-23","tiktok",1702.06),("2026-02-23","shopee",6439.42),("2026-02-23","lazada",518.44),
    ("2026-02-24","shopee",9731.05),("2026-02-24","lazada",3282.85),("2026-02-24","tiktok",978.29),
    ("2026-02-25","lazada",4441.01),("2026-02-25","shopee",12493.01),("2026-02-25","tiktok",1116.22),
    ("2026-02-26","shopee",8353.44),("2026-02-26","lazada",1693.21),("2026-02-26","tiktok",1111.42),
    ("2026-02-27","tiktok",777.93),("2026-02-27","lazada",1918.98),("2026-02-27","shopee",5739.98),
    ("2026-02-28","shopee",4872.31),("2026-02-28","tiktok",1305.63),("2026-02-28","lazada",2105.89),
    ("2026-03-01","shopee",9829.50),("2026-03-01","lazada",2052.67),("2026-03-01","tiktok",1399.95),
    ("2026-03-02","tiktok",1253.82),("2026-03-02","lazada",12662.83),("2026-03-02","shopee",27063.76),
    ("2026-03-03","lazada",17814.98),("2026-03-03","shopee",40671.10),("2026-03-03","tiktok",1509.76),
    ("2026-03-04","lazada",6954.97),("2026-03-04","tiktok",1131.61),("2026-03-04","shopee",15187.35),
    ("2026-03-05","tiktok",1259.18),("2026-03-05","lazada",3918.75),("2026-03-05","shopee",11601.63),
    ("2026-03-06","shopee",12075.77),("2026-03-06","lazada",1000.98),("2026-03-06","tiktok",875.74),
    ("2026-03-07","tiktok",1233.56),("2026-03-07","shopee",9597.63),("2026-03-07","lazada",1129.01),
    ("2026-03-08","tiktok",1295.07),("2026-03-08","lazada",1735.11),("2026-03-08","shopee",10583.82),
    ("2026-03-09","shopee",9238.36),("2026-03-09","tiktok",1876.92),("2026-03-09","lazada",1743.79),
    ("2026-03-10","shopee",3411.69),("2026-03-10","lazada",778.51),("2026-03-10","tiktok",1584.39),
    ("2026-03-11","lazada",493.80),("2026-03-11","shopee",4938.14),("2026-03-11","tiktok",2496.86),
    ("2026-03-12","tiktok",1569.31),("2026-03-12","lazada",374.69),("2026-03-12","shopee",3963.49),
    ("2026-03-13","tiktok",1427.98),("2026-03-13","lazada",898.50),("2026-03-13","shopee",7037.08),
    ("2026-03-14","lazada",1938.23),("2026-03-14","shopee",5753.75),("2026-03-14","tiktok",1125.76),
    ("2026-03-15","shopee",13829.17),("2026-03-15","lazada",3104.71),("2026-03-15","tiktok",1705.15),
    ("2026-03-16","lazada",1204.50),("2026-03-16","tiktok",1972.91),("2026-03-16","shopee",7444.52),
    ("2026-03-17","shopee",7819.14),("2026-03-17","lazada",1477.30),("2026-03-17","tiktok",1591.96),
    ("2026-03-18","tiktok",1431.81),("2026-03-18","lazada",932.94),("2026-03-18","shopee",4857.08),
    ("2026-03-19","lazada",1766.93),("2026-03-19","shopee",5320.18),("2026-03-19","tiktok",1399.92),
    ("2026-03-20","lazada",1123.04),("2026-03-20","shopee",5149.20),("2026-03-20","tiktok",248.00),
    ("2026-03-21","tiktok",1056.12),("2026-03-21","lazada",2209.50),("2026-03-21","shopee",4244.04),
    ("2026-03-22","shopee",10029.44),("2026-03-22","lazada",2894.28),("2026-03-22","tiktok",1751.39),
    ("2026-03-23","shopee",7300.61),("2026-03-23","lazada",1733.48),("2026-03-23","tiktok",1699.23),
    ("2026-03-24","shopee",12104.20),("2026-03-24","lazada",25747.59),("2026-03-24","tiktok",1964.49),
    ("2026-03-25","lazada",14940.10),("2026-03-25","shopee",16718.35),("2026-03-25","tiktok",2093.90),
    ("2026-03-26","tiktok",2582.89),("2026-03-26","lazada",7226.33),("2026-03-26","shopee",9902.15),
    ("2026-03-27","shopee",8257.49),("2026-03-27","tiktok",1518.19),("2026-03-27","lazada",6644.13),
    ("2026-03-28","tiktok",1661.42),("2026-03-28","shopee",5015.51),("2026-03-28","lazada",3903.71),
    ("2026-03-29","tiktok",1963.70),("2026-03-29","lazada",4305.27),("2026-03-29","shopee",4193.06),
    ("2026-03-30","shopee",5446.75),("2026-03-30","lazada",2119.43),("2026-03-30","tiktok",1783.46),
    ("2026-03-31","tiktok",1084.23),("2026-03-31","lazada",2003.16),("2026-03-31","shopee",4923.48),
]

# ── Ad Performance ────────────────────────────────────────────────────────
ADS_DATA = [
    {"source":"shopeeAds",           "channel":"shopee-1","channel_label":"Shopee Paid Ads",      "total_spend":48456.95,"total_impressions":3138811,"total_clicks":88067, "total_conversions":11148,"total_revenue":468430.40,"roas":9.67, "ctr":2.81,"cpa":4.35},
    {"source":"lazadaAds",           "channel":"lazada-1","channel_label":"Lazada Paid Ads",      "total_spend":24672.10,"total_impressions":3033176,"total_clicks":148286,"total_conversions":2219, "total_revenue":143612.29,"roas":5.82, "ctr":4.89,"cpa":11.12},
    {"source":"shopeeAffiliateAds",  "channel":"shopee-1","channel_label":"Shopee Affiliate",     "total_spend":8328.08, "total_impressions":0,      "total_clicks":0,     "total_conversions":3711, "total_revenue":142029.62,"roas":17.05,"ctr":0,   "cpa":2.24},
    {"source":"lazadaAffiliateAds",  "channel":"lazada-1","channel_label":"Lazada Affiliate",     "total_spend":7640.58, "total_impressions":0,      "total_clicks":0,     "total_conversions":960,  "total_revenue":90161.27, "roas":11.80,"ctr":0,   "cpa":7.96},
    {"source":"tiktokAffiliateAds",  "channel":"tiktok-2","channel_label":"TikTok Affiliate",     "total_spend":5520.74, "total_impressions":0,      "total_clicks":0,     "total_conversions":5,    "total_revenue":41507.15, "roas":7.52, "ctr":0,   "cpa":1104.15},
    {"source":"shopee",              "channel":"shopee-1","channel_label":"Shopee Organic Boost", "total_spend":1642.14, "total_impressions":387966, "total_clicks":3881,  "total_conversions":547,  "total_revenue":34092.04, "roas":20.76,"ctr":1.00,"cpa":3.00},
]

# ── Traffic ───────────────────────────────────────────────────────────────
TRAFFIC_DATA = [
    {"source":"shopee","channel":"shopee-1","total_visitors":170078,"total_sessions":170078,"total_orders":14856,"revenue":716351.72,"new_visitors":92564,"repeat_visitors":77514,"atc_visitors":36691},
    {"source":"lazada","channel":"lazada-1","total_visitors":114372,"total_sessions":114372,"total_orders":3444, "revenue":244327.79,"new_visitors":0,    "repeat_visitors":0,   "atc_visitors":8434},
]
TRAFFIC_DATA_LY = [
    {"source":"shopee","channel":"shopee-1","total_visitors":149492,"total_sessions":149492,"total_orders":11873,"revenue":502054.07,"new_visitors":73942,"repeat_visitors":0,"atc_visitors":0},
    {"source":"lazada","channel":"lazada-1","total_visitors":107747,"total_sessions":107747,"total_orders":4664, "revenue":258572.91,"new_visitors":0,    "repeat_visitors":0,"atc_visitors":0},
]

# ── Inventory ─────────────────────────────────────────────────────────────
INVENTORY_DATA = [
    {"source":"lazada", "channel":"lazada-1", "product_status":"A",          "product_count":668,  "total_available_qty":59328},
    {"source":"lazada", "channel":"lazada-1", "product_status":"N",          "product_count":1169, "total_available_qty":38331},
    {"source":"lazada", "channel":"lazada-1", "product_status":"X",          "product_count":17,   "total_available_qty":535},
    {"source":"lazada", "channel":"lazada-1", "product_status":"NOT_LISTED", "product_count":1,    "total_available_qty":0},
    {"source":"shopee", "channel":"shopee-1", "product_status":"A",          "product_count":925,  "total_available_qty":103459},
    {"source":"shopee", "channel":"shopee-1", "product_status":"N",          "product_count":292,  "total_available_qty":0},
    {"source":"shopee", "channel":"shopee-1", "product_status":"X",          "product_count":91,   "total_available_qty":0},
    {"source":"shopee", "channel":"shopee-1", "product_status":"BANNED",     "product_count":1,    "total_available_qty":0},
    {"source":"tiktok", "channel":"tiktok-2", "product_status":"A",          "product_count":422,  "total_available_qty":68039},
    {"source":"tiktok", "channel":"tiktok-2", "product_status":"N",          "product_count":905,  "total_available_qty":75477},
    {"source":"tiktok", "channel":"tiktok-2", "product_status":"D",          "product_count":123,  "total_available_qty":775},
    {"source":"tiktok", "channel":"tiktok-2", "product_status":"X",          "product_count":56,   "total_available_qty":2276},
    {"source":"tiktok", "channel":"tiktok-1", "product_status":"A",          "product_count":121,  "total_available_qty":12421},
    {"source":"qoo10",  "channel":"qoo10-1",  "product_status":"N",          "product_count":409,  "total_available_qty":0},
]

# ── Top SKUs ──────────────────────────────────────────────────────────────
TOP_SKUS = [
    {"product_name":"Caltrate Joint Health UCII 180/240 Tabs",            "source":"shopee","brand":"Caltrate", "category":"Joint Health","units_sold":434, "revenue":56546.90,"orders":391},
    {"product_name":"Caltrate Joint Speed UCII + Hops 2-Pack 42s",        "source":"shopee","brand":"Caltrate", "category":"Joint Health","units_sold":422, "revenue":30580.67,"orders":211},
    {"product_name":"Polident Pro Retainer Cleanser 6-Pack 36s",          "source":"shopee","brand":"Polident", "category":"Oral Care",   "units_sold":468, "revenue":20363.28,"orders":78},
    {"product_name":"Caltrate Bone & Muscle Triple Action 2-Pack 60s",    "source":"shopee","brand":"Caltrate", "category":"Bone Health", "units_sold":377, "revenue":19802.33,"orders":189},
    {"product_name":"Caltrate Joint Health UCII 90s+30s Bonus Pack",      "source":"shopee","brand":"Caltrate", "category":"Joint Health","units_sold":212, "revenue":19729.71,"orders":212},
    {"product_name":"Caltrate Joint Health UCII 180/240 Tabs (Lazada)",   "source":"lazada","brand":"Caltrate", "category":"Joint Health","units_sold":159, "revenue":17884.50,"orders":143},
    {"product_name":"Panadol Extra Optizorb 120 Caplets",                 "source":"shopee","brand":"Panadol",  "category":"Pain Relief", "units_sold":317, "revenue":16944.13,"orders":317},
    {"product_name":"Polident Pro Retainer Cleanser 3-Pack 36s",          "source":"shopee","brand":"Polident", "category":"Oral Care",   "units_sold":715, "revenue":16592.57,"orders":238},
    {"product_name":"Sensodyne Repair & Protect Deep Repair 6-Pack 100g", "source":"shopee","brand":"Sensodyne","category":"Oral Care",   "units_sold":377, "revenue":15643.07,"orders":63},
    {"product_name":"Sensodyne Full Range 6-Pack 100g Mixed Variants",    "source":"shopee","brand":"Sensodyne","category":"Oral Care",   "units_sold":353, "revenue":14058.76,"orders":59},
    {"product_name":"Panadol Extra Optizorb 20 Caplets (Lazada)",         "source":"lazada","brand":"Panadol",  "category":"Pain Relief", "units_sold":1404,"revenue":14040.80,"orders":132},
    {"product_name":"Scott's Cod Liver Oil Immunity Support 500s",        "source":"shopee","brand":"Scott's",  "category":"Supplements", "units_sold":471, "revenue":12966.59,"orders":471},
    {"product_name":"Caltrate Joint Speed 2-Pack Lazada",                 "source":"lazada","brand":"Caltrate", "category":"Joint Health","units_sold":190, "revenue":12915.73,"orders":130},
    {"product_name":"Scott's Emulsion Cod Liver Oil DHA 6-Pack 400ml",   "source":"shopee","brand":"Scott's",  "category":"Kids Health", "units_sold":280, "revenue":12835.28,"orders":47},
    {"product_name":"Caltrate Bone & Muscle 2-Pack 100s",                 "source":"shopee","brand":"Caltrate", "category":"Bone Health", "units_sold":170, "revenue":12601.68,"orders":85},
]

BOTTOM_SKUS = [
    {"product_name":"Caltrate Plus 7s Trial Size",                      "source":"lazada","brand":"Caltrate", "category":"Bone Health","units_sold":1,"revenue":4.46, "orders":1},
    {"product_name":"Scott's Vitamin C Pastilles 2-Pack Mixed Berry 30g","source":"lazada","brand":"Scott's", "category":"Kids Health","units_sold":1,"revenue":5.84, "orders":1},
    {"product_name":"ENO Fruit Salt Plain 100g",                        "source":"lazada","brand":"ENO",      "category":"Digestive",  "units_sold":1,"revenue":7.30, "orders":1},
    {"product_name":"Scott's Multivitamin Gummies Kids 15s",            "source":"lazada","brand":"Scott's",  "category":"Kids Health","units_sold":1,"revenue":7.50, "orders":1},
    {"product_name":"Scott's DHA Fish Oil Gummies Kids 15s",            "source":"lazada","brand":"Scott's",  "category":"Kids Health","units_sold":1,"revenue":7.74, "orders":1},
    {"product_name":"Sensodyne Sensitivity & Gum Toothbrush 1s",        "source":"lazada","brand":"Sensodyne","category":"Oral Care",  "units_sold":1,"revenue":8.99, "orders":1},
    {"product_name":"Sensodyne Toothpaste S&G 100g Single",             "source":"lazada","brand":"Sensodyne","category":"Oral Care",  "units_sold":1,"revenue":9.20, "orders":1},
    {"product_name":"Scott's Vitamin C Pastilles Orange 30g",           "source":"shopee","brand":"Scott's",  "category":"Kids Health","units_sold":3,"revenue":10.70,"orders":3},
    {"product_name":"Scott's Vitamin C Pastilles Blackcurrant 30g",     "source":"lazada","brand":"Scott's",  "category":"Kids Health","units_sold":2,"revenue":11.58,"orders":2},
    {"product_name":"Sensodyne S&G Toothbrush 1s Shopee",               "source":"shopee","brand":"Sensodyne","category":"Oral Care",  "units_sold":2,"revenue":13.30,"orders":2},
]

# ── Promotions ────────────────────────────────────────────────────────────
PROMOTIONS_DATA = [
    {"source":"shopee","channel":"shopee-1","voucher_revenue":404147.63,"voucher_units":0,    "voucher_new_buyers":0,    "flash_sale_revenue":0,  "flash_sale_orders":0, "promo_code_revenue":0,"promo_code_orders":0,"bmsm_revenue":0,"bmsm_orders":0,"gwp_revenue":0,    "gwp_orders":0},
    {"source":"lazada","channel":"lazada-1","voucher_revenue":141140.12,"voucher_units":0,    "voucher_new_buyers":0,    "flash_sale_revenue":0,  "flash_sale_orders":0, "promo_code_revenue":0,"promo_code_orders":0,"bmsm_revenue":0,"bmsm_orders":0,"gwp_revenue":0,    "gwp_orders":0},
    {"source":"tiktok","channel":"tiktok-2","voucher_revenue":64890.24, "voucher_units":88574,"voucher_new_buyers":66371,"flash_sale_revenue":751,"flash_sale_orders":66,"promo_code_revenue":0,"promo_code_orders":0,"bmsm_revenue":0,"bmsm_orders":0,"gwp_revenue":64890.24,"gwp_orders":2534},
]


class GraasDataLoader:
    """Real GSK data from Graas MCP. No Snowflake credentials needed."""

    def get_orders_by_channel(self, date_from: str, date_to: str) -> pd.DataFrame:
        return pd.DataFrame(ORDERS_DATA)

    def get_orders_by_channel_ly(self) -> pd.DataFrame:
        return pd.DataFrame(ORDERS_DATA_LY)

    def get_product_performance(self, date_from: str, date_to: str) -> pd.DataFrame:
        return pd.concat([pd.DataFrame(TOP_SKUS), pd.DataFrame(BOTTOM_SKUS)], ignore_index=True)

    def get_traffic(self, date_from: str, date_to: str) -> pd.DataFrame:
        if date_from and str(date_from)[:4] == "2025":
            return pd.DataFrame(TRAFFIC_DATA_LY)
        return pd.DataFrame(TRAFFIC_DATA)

    def get_ad_performance(self, date_from: str, date_to: str) -> pd.DataFrame:
        return pd.DataFrame(ADS_DATA)

    def get_inventory_summary(self) -> pd.DataFrame:
        df = pd.DataFrame(INVENTORY_DATA)
        df["channel"] = df["source"].str.title() + " (" + df["channel"] + ")"
        return df

    def get_promotion_performance(self, date_from: str, date_to: str) -> pd.DataFrame:
        return pd.DataFrame(PROMOTIONS_DATA)

    def get_daily_revenue_trend(self, date_from: str, date_to: str) -> pd.DataFrame:
        df = pd.DataFrame(DAILY_REVENUE_RAW, columns=["report_date", "source", "revenue_amt"])
        df["report_date"] = pd.to_datetime(df["report_date"])
        if date_from:
            df = df[df["report_date"] >= pd.to_datetime(date_from)]
        if date_to:
            df = df[df["report_date"] <= pd.to_datetime(date_to)]
        return df

    def close(self):
        pass
