import requests
import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)


def get_weather_yandex(lat, lon, api_key):
    headers = {
        'X-Yandex-Weather-Key': api_key
    }
    url = f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # 📍 Проверка структуры
        if not isinstance(data, dict):
            print("❌ Ответ не является JSON-объектом.")
            return

        # 🌍 Информация о местоположении
        info = data.get('info', {})
        tzinfo = info.get('tzinfo', {})
        tz_name = tzinfo.get('name', 'Неизвестный часовой пояс')
        location = f"{lat}°N, {lon}°E"  # Если нет названия города — используем координаты

        # 🌤️ Текущая погода (fact)
        fact = data.get('fact', {})
        temp = fact.get('temp', '—')
        feels_like = fact.get('feels_like', '—')
        condition = fact.get('condition', '—')
        humidity = fact.get('humidity', '—')
        wind_speed = fact.get('wind_speed', '—')
        wind_dir = fact.get('wind_dir', '—')
        wind_gust = fact.get('wind_gust', '—')
        cloudness = fact.get('cloudness', '—')
        is_thunder = fact.get('is_thunder', False)

        # 📅 Текущее время
        now_dt_str = data.get('now_dt', '—')
        if now_dt_str != '—':
            try:
                from datetime import datetime, timezone, timedelta
                now_dt = datetime.fromisoformat(now_dt_str.replace('Z', '+00:00'))
                local_tz = timezone(timedelta(seconds=tzinfo.get('offset', 0)))
                local_time = now_dt.astimezone(local_tz)
                time_str = local_time.strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                time_str = now_dt_str
        else:
            time_str = '—'

        # 🖨️ Вывод текущей погоды
        print("=" * 60)
        print("🌤️  ПОГОДА СЕЙЧАС")
        print("=" * 60)
        print(f"📍 Местоположение: {location} (часовой пояс: {tz_name})")
        print(f"🕒 Текущее время: {time_str}")
        print(f"🌡️  Температура: {temp}°C (ощущается как {feels_like}°C)")
        print(f"☁️  Состояние: {condition}")
        print(f"💧 Влажность: {humidity}%")
        print(f"💨 Ветер: {wind_speed} м/с, порывы до {wind_gust} м/с, направление: {wind_dir}")
        cloudness_pct = cloudness * 100 if isinstance(cloudness, (int, float)) else '—'
        print(f"☁️  Облачность: {cloudness_pct}%")
        print(f"⚡ Гроза: {'Да' if is_thunder else 'Нет'}")
        print("=" * 60)

        # 📅 Прогноз на сегодня (если есть)
        forecasts = data.get('forecasts', [])
        if forecasts:
            today_forecast = forecasts[0]  # Первый элемент — сегодня
            print("\n🌤️  ПРОГНОЗ НА СЕГОДНЯ")
            print("-" * 60)
            parts = today_forecast.get('parts', {})
            for part_name in ['morning', 'day', 'evening', 'night']:
                part = parts.get(part_name, {})
                if not part:
                    continue
                temp_min = part.get('temp_min', '—')
                temp_max = part.get('temp_max', '—')
                part_condition = part.get('condition', '—')
                print(f"🔹 {part_name.capitalize()}: {temp_min}°C — {temp_max}°C, {part_condition}")
        else:
            print("\n⚠️  Прогноз на сегодня недоступен.")

    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при запросе к API: {e}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")


if __name__ == "__main__":
    print("🌤️ Привет! Введите координаты, чтобы узнать погоду через Yandex.")
    try:
        lat = float(input("Широта: "))
        lon = float(input("Долгота: "))
    except ValueError:
        print("❌ Введите числа!")
        exit()

    API_KEY = os.getenv("YANDEX_WEATHER_API_KEY")
    get_weather_yandex(lat, lon, API_KEY)
