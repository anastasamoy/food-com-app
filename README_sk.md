
### 🌍 Viacjazyčná podpora
- **Angličtina** - Hlavný jazyk rozhrania
- **Slovenčina** - Úplný preklad
- **Ruština** - Úplný preklad
- **Dynamické prepínanie** - Zmena jazyka v reálnom čase bez obnovenia

### 📊 Kľúčové implementované funkcie

#### **1. Prehliadač receptov**
- Vyhľadávanie podľa názvu, času varenia, počtu ingrediencií
- Rozbaliteľné karty receptov s úplnými detailmi
- Zoznam ingrediencií s formátovaním
- Zobrazenie krokov varenia
- Parsovanie výživových informácií
- Tagy a kategórie

#### **2. Systém recenzií**
- Recenzie používateľov s hviezdičkovým hodnotením
- Filter podľa minimálneho hodnotenia
- Zobrazenie textu recenzie
- Informácie o používateľovi a dátume

#### **3. Analýza dát**
- Štatistiky a metriky datasetu
- Informácie o stĺpcoch a typoch dát
- Analýza chýbajúcich hodnôt
- Funkcia náhľadu dát

#### **4. Užívateľský zážitok**
- Responzívna bočná navigácia
- Vyhľadávanie a filtrovanie v reálnom čase
- Rozbaliteľné/zbaviteľné sekcie
- Čisté, intuitívne rozhranie

### 🔧 Vývojový proces

#### **Fáza 1: Nastavenie & Základy**
- Nastavenie prostredia s virtuálnym prostredím
- Štruktúra Streamlit aplikácie
- Základné načítanie a zobrazenie dát

#### **Fáza 2: Hlavné funkcie**
- Rozhranie pre prehliadanie receptov
- Implementácia systému recenzií
- Nástroje na analýzu dát

#### **Fáza 3: Vylepšenia**
- Systém viacjazyčnej podpory
- Vylepšený dizajn UI/UX
- Pokročilé filtrovanie a vyhľadávanie
- Dokumentácia projektu

### 📈 Zdroj dát & Štruktúra

**Dataset:** [Food.com Recipes and User Interactions](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions)

#### **Hlavné súbory:**
- `RAW_recipes.csv` - ľudsky čitateľné dáta receptov
- `RAW_interactions.csv` - Recenzie a hodnotenia používateľov
- `PP_recipes.csv` - Predspracované dáta pre ML
- `PP_users.csv` - Predspracované dáta používateľov

#### **Kľúčové stĺpce v RAW_recipes.csv:**
- `name` - Názov receptu
- `ingredients` - Zoznam ingrediencií
- `steps` - Inštrukcie varenia
- `nutrition` - Výživové hodnoty
- `minutes` - Čas varenia
- `tags` - Kategórie receptov

### 🎯 Budúce vylepšenia

#### **Plánované funkcie:**
- Pokročilé vizualizácie dát s Plotly
- Systém odporúčania receptov
- Obľúbené recepty používateľov
- Exportná funkcionalita
- Pokročilé vyhľadávacie filtre
- Integrácia obrázkov receptov

#### **Technické vylepšenia:**
- Integrácia databázy (SQLite/PostgreSQL)
- Optimalizácia vyrovnávacej pamäte pre veľké datasety
- Systém autentifikácie používateľov
- Vývoj REST API

### 👥 Vývojový tím

Tento projekt bol vyvinutý ako ukážka:
- Vývoja full-stack webových aplikácií s Pythonom
- Schopností dátovej vedy a analýzy
- Internacionalizácie s viacjazyčnou podporou
- Princípov dizajnu zameraného na používateľa

### 📝 Licencia & Atribúcia

- **Dataset**: Food.com cez Kaggle
- **Aplikácia**: Open source pre vzdelávacie účely
- **Technológie**: Streamlit, Pandas, Python

---

*Naposledy aktualizované: September 2024*
""",

        "ru": """
## 🚀 Обзор проекта

**Food.com Recipes Explorer** - это комплексное веб-приложение, созданное для исследования и анализа набора данных Food.com, содержащего более 230 000 рецептов и 1 миллион пользовательских отзывов.

### 🛠️ Техническая реализация

#### **Фронтенд и Фреймворк:**
- **Streamlit** - Python веб-фреймворк для создания интерактивных веб-приложений
- **Pandas** - Манипуляция и анализ данных
- **Plotly** - Интерактивная визуализация (готово для будущих графиков)

#### **Бэкенд и Обработка данных:**
- **Python 3.9+** - Основной язык программирования
- **Pandas** - Парсинг CSV и преобразование данных
- **Pathlib** - Операции с файловой системой

#### **Архитектура:**