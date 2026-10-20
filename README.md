# KaziLink Tanzania

Mfumo wa kutafuta ajira, internship na nafasi za kujitolea unaowalenga vijana na wahitimu wapya Tanzania. Mradi huu ni MVP inayotumia Django na SQLite ili iwe rahisi kuanza na kujaribu kwenye kompyuta yako.

## Vipengele

- Usajili na kuingia kwa waombaji na waajiri.
- Utafutaji wa ajira, internship, kujitolea na fursa za kujishikiza kwa eneo, kampuni na maneno muhimu.
- Ulinganishaji wa ujuzi wa mwombaji na vigezo vya nafasi kwa asilimia.
- Kutuma maombi na kufuatilia hali ya maombi.
- Dashboard tofauti kwa mwombaji na mwajiri.
- Arifa za nafasi zinazolingana na ujuzi na mabadiliko ya maombi.
- CV builder yenye mwonekano wa kuchapisha au kuhifadhi kama PDF.
- Django admin kwa usimamizi wa taarifa.

## Mahitaji

- Python 3.10 au mpya zaidi.
- `pip`.

## Kuanza kwenye Windows

Fungua PowerShell ndani ya folder la mradi kisha endesha:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Fungua `http://127.0.0.1:8000/`. Django admin inapatikana `http://127.0.0.1:8000/admin/`.

## Muundo wa folder

```text
Smart Jobs and Internship Matching System/
├── config/                 # Mipangilio na URL za Django
├── matching/               # Models, forms, views na ulinganishaji
├── static/
│   ├── css/app.css         # Muonekano wa mfumo
│   └── js/app.js           # Mwingiliano wa menyu
├── templates/
│   ├── matching/           # Kurasa za kazi, dashboard na CV
│   └── registration/       # Kuingia na kujisajili
├── manage.py
└── requirements.txt
```

## Matumizi

1. Jisajili kama **Mtafuta kazi** au **Mwajiri**.
2. Mwombaji ajaze wasifu, hasa ujuzi uliotenganishwa kwa koma, elimu na uzoefu.
3. Mwajiri ajaze taarifa za taasisi na achapishe nafasi. Jaza vigezo vya nafasi kwa maneno yanayolingana na ujuzi (kwa mfano `Python, SQL, Excel`) ili mapendekezo ya ulinganifu yawe sahihi.
4. Waombaji wanaweza kuomba nafasi; waajiri husasisha hali ya maombi kupitia dashboard.
5. Mwombaji anaweza kujenga CV na kutumia kitufe cha kuchapisha kuchagua **Save as PDF**.

## Maelezo ya usanidi

SQLite hutumika kwa urahisi wa kuanza. Kwa deployment, weka `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, na `DJANGO_ALLOWED_HOSTS` kupitia environment variables, tumia HTTPS, na pangilia database ya production pamoja na ukusanyaji wa static files.
