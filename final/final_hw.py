import json

with open("bankruptcy_messages.json", "r", encoding="utf-8") as file:
    messages = json.load(file)

with open("organizations.json", "r", encoding="utf-8") as file:
    organizations = json.load(file)

with open("priority_cases.txt", "r", encoding="utf-8") as file:
    priority_cases = file.read().splitlines()

print("Количество сообщений:", len(messages))
print("Количество организаций:", len(organizations))
print("Количество приоритетных дел:", len(priority_cases))

organizations_by_inn = {}

for org in organizations:
    organizations_by_inn[org["inn"]] = org

linked_messages = []
validation_errors = []

for message in messages:
    publisher_inn = message.get("publisher_inn", "").strip()

    if not publisher_inn:
        validation_errors.append({
            "error_type": "missing_inn",
            "message": message
        })
        continue

    if publisher_inn not in organizations_by_inn:
        validation_errors.append({
            "error_type": "unknown_inn",
            "message": message
        })
        continue

    linked_message = {
        "publisher_inn": publisher_inn,
        "organization_name": organizations_by_inn[publisher_inn]["name"],
        "region": organizations_by_inn[publisher_inn]["region"],
        "msg_text": message.get("msg_text"),
        "date_published": message.get("date_published"),
        "type": message.get("type"),
        "case_number": message.get("case_number")
    }

    linked_messages.append(linked_message)

print("Связанных сообщений:", len(linked_messages))
print("Ошибок валидации:", len(validation_errors))

import re
from datetime import datetime

month_map = {
    "января": "01",
    "февраля": "02",
    "марта": "03",
    "апреля": "04",
    "мая": "05",
    "июня": "06",
    "июля": "07",
    "августа": "08",
    "сентября": "09",
    "октября": "10",
    "ноября": "11",
    "декабря": "12"
}


def parse_date(date_string):
    if not date_string:
        return None

    date_string = str(date_string).strip()

    formats = [
        "%d.%m.%Y",
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
        "%d/%m/%Y %H:%M"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt).strftime("%Y-%m-%d")
        except:
            pass

    for month_name in month_map:
        if month_name in date_string.lower():
            parts = date_string.lower().replace("г.", "").split()
            if len(parts) >= 3:
                day = parts[0]
                month = month_map[parts[1]]
                year = parts[2]
                return f"{year}-{month}-{day.zfill(2)}"

    return None


def extract_amount(text):
    if not text:
        return None

    text = text.lower().replace(" ", "")

    patterns = [
        r"(\d+[.,]?\d*)млнруб",
        r"(\d+[.,]?\d*)тыс\.?руб",
        r"(\d[\d\s]*[.,]?\d*)руб"
    ]

    original_text = text.replace(",", ".")

    match = re.search(r"(\d+[.]?\d*)млнруб", original_text)
    if match:
        return float(match.group(1)) * 1_000_000

    match = re.search(r"(\d+[.]?\d*)тыс\.?руб", original_text)
    if match:
        return float(match.group(1)) * 1_000

    match = re.search(r"(\d+[.]?\d*)руб", original_text)
    if match:
        return float(match.group(1))

    return None


processed_messages = []

for item in linked_messages:
    new_item = item.copy()

    parsed_date = parse_date(item["date_published"])
    amount = extract_amount(item["msg_text"])
    is_priority = item["case_number"] in priority_cases

    new_item["parsed_date"] = parsed_date
    new_item["amount"] = amount
    new_item["is_priority"] = is_priority

    if parsed_date is None:
        validation_errors.append({
            "error_type": "invalid_date",
            "message": item
        })

    processed_messages.append(new_item)

print("Обработанных сообщений:", len(processed_messages))
print("Ошибок после проверки дат:", len(validation_errors))
print("Приоритетных сообщений:", len([x for x in processed_messages if x['is_priority']]))

type_counts = {}
region_counts = {}
priority_type_counts = {}
total_amount = 0

for item in processed_messages:
    msg_type = item["type"] if item["type"] else "Не указан"
    region = item["region"] if item["region"] else "Не указан"

    type_counts[msg_type] = type_counts.get(msg_type, 0) + 1
    region_counts[region] = region_counts.get(region, 0) + 1

    if item["is_priority"]:
        priority_type_counts[msg_type] = priority_type_counts.get(msg_type, 0) + 1

    if item["amount"] is not None:
        total_amount += item["amount"]

analysis_results = {
    "total_messages": len(messages),
    "linked_messages": len(linked_messages),
    "processed_messages": len(processed_messages),
    "validation_errors_count": len(validation_errors),
    "priority_messages_count": len([x for x in processed_messages if x["is_priority"]]),
    "message_types": type_counts,
    "regions": region_counts,
    "priority_message_types": priority_type_counts,
    "total_amount": total_amount
}

with open("analysis_results.json", "w", encoding="utf-8") as file:
    json.dump(analysis_results, file, ensure_ascii=False, indent=4)

with open("validation_errors.json", "w", encoding="utf-8") as file:
    json.dump(validation_errors, file, ensure_ascii=False, indent=4)

with open("summary_report.txt", "w", encoding="utf-8") as file:
    file.write("СВОДНЫЙ ОТЧЕТ ПО АНАЛИЗУ СООБЩЕНИЙ О БАНКРОТСТВЕ\n")
    file.write("=" * 50 + "\n\n")
    file.write(f"Всего сообщений: {len(messages)}\n")
    file.write(f"Связанных сообщений: {len(linked_messages)}\n")
    file.write(f"Обработанных сообщений: {len(processed_messages)}\n")
    file.write(f"Ошибок валидации: {len(validation_errors)}\n")
    file.write(f"Приоритетных сообщений: {len([x for x in processed_messages if x['is_priority']])}\n")
    file.write(f"Общая сумма требований/долгов: {total_amount}\n\n")

    file.write("Количество сообщений по типам:\n")
    for key, value in type_counts.items():
        file.write(f"- {key}: {value}\n")

    file.write("\nКоличество сообщений по регионам:\n")
    for key, value in region_counts.items():
        file.write(f"- {key}: {value}\n")

    file.write("\nКоличество приоритетных сообщений по типам:\n")
    for key, value in priority_type_counts.items():
        file.write(f"- {key}: {value}\n")

print("Файл analysis_results.json сохранен")
print("Файл validation_errors.json сохранен")
print("Файл summary_report.txt сохранен")
