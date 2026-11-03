# pa-marketplace-funnel

Небольшой петпроект: воронка объявлений + простой A/B на pandas.

События: `view_item` → `contact` → `deal`. У варианта B конверсия в контакт чуть выше — это видно z-тестом.

## Запуск

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.main
```

Появится `data/raw/events.csv` и папка `reports/` (csv + картинки).

## Файлы

- `src/generate_data.py` — синтетика
- `src/funnel.py` — воронка и разрезы
- `src/ab_test.py` — A/B по contact/view
- `src/main.py` — считает всё и кладёт в reports
