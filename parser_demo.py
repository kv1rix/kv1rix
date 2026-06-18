import asyncio
import aiohttp
import pandas as pd

TEST_URLS = [
    "https://example-hr-service.ru",
    "https://example-hr-service.ru",
    "https://example-hr-service.ru",
]

async def fetch_applicant_data(session, url, vacancy_id):
    """Имитация быстрого асинхронного сбора данных с сервера"""
    print(f"[ПАРСЕР] Скачиваю данные откликов с: {url}...")
    await asyncio.sleep(0.5)

    return [
        {"vacancy_id": vacancy_id, "name": "Иванова А.А.", "score": 92, "skills": "ОСНО, НДС, 1С", "experience": "5 лет"},
        {"vacancy_id": vacancy_id, "name": "Петров П.П.", "score": 74, "skills": "1С, УСН, Кадры", "experience": "2 года"},
        {"vacancy_id": vacancy_id, "name": "Сидорова С.С.", "score": 88, "skills": "Производство, ОСНО, Excel", "experience": "4 года"},
    ]

async def main():
    print("🚀 Запуск асинхронного парсера откликов...")
    all_results = []
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, url in enumerate(TEST_URLS):
            task = fetch_applicant_data(session, url, vacancy_id=100 + i)
            tasks.append(task)

        pages_data = await asyncio.gather(*tasks)
        for page in pages_data:
            all_results.extend(page)
            
    print(f"\n[УСПЕХ] Сбор завершен. Всего обработано позиций: {len(all_results)}")
    
    df = pd.DataFrame(all_results)
    output_file = "applicants_report.xlsx"
    df.to_excel(output_file, index=False)
    print(f"💾 Данные успешно отформатированы и сохранены в файл: {output_file}")

if __name__ == "__main__":
    asyncio.run(main())
