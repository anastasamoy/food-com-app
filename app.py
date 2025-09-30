# app.py
import streamlit as st
import pandas as pd
import os
from pathlib import Path
from languages import LANGUAGES, get_text

# Настройка страницы
st.set_page_config(
    page_title="Food.com - Recipes Database",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Инициализация языка
    if 'language' not in st.session_state:
        st.session_state.language = "en"
    
    # Показываем страницу приветствия если первый запуск
    if 'first_visit' not in st.session_state:
        show_welcome_page()
        return
    
    # Основное приложение
    run_main_app()

def show_welcome_page():
    """Страница приветствия и выбора языка"""
    st.title("🍳 Welcome to Food.com Recipes Explorer!")
    
    # Выбор языка
    lang_option = st.radio(
        "Please select your language / Prosím vyberte váš jazyk / Пожалуйста, выберите ваш язык:",
        ["English", "Slovensky", "Русский"]
    )
    
    lang_map = {"English": "en", "Slovensky": "sk", "Русский": "ru"}
    selected_lang = lang_map[lang_option]
    
    # Показываем описание на выбранном языке
    st.header("📖 About this application" if selected_lang == "en" else 
              "📖 O tejto aplikácii" if selected_lang == "sk" else 
              "📖 О приложении")
    
    welcome_texts = {
        "en": """
        **Food.com Recipes Explorer** is an interactive web application that allows you to explore:
        
        🍽️ **Recipe Collection** - Browse 230,000+ recipes with ingredients and cooking steps
        💬 **User Reviews** - Read 1,000,000+ reviews and ratings  
        📊 **Data Analysis** - Analyze dataset structure and statistics
        
        **Main Features:**
        - Search recipes by name, cooking time, and ingredients
        - Read user reviews with ratings
        - View nutritional information
        - Multi-language interface
        
        **Data Source:** [Food.com Recipes and Interactions](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions)
        
        To get started, make sure you have the CSV files in the application folder and click the button below!
        """,
        "sk": """
        **Food.com Recipes Explorer** je interaktívna webová aplikácia, ktorá vám umožňuje preskúmať:
        
        🍽️ **Zbierku receptov** - Prehliadajte 230 000+ receptov s ingredienciami a krokmi varenia
        💬 **Recenzie používateľov** - Čítajte 1 000 000+ recenzií a hodnotení
        📊 **Analýzu dát** - Analyzujte štruktúru dátových súborov a štatistiky
        
        **Hlavné funkcie:**
        - Hľadanie receptov podľa názvu, času varenia a ingrediencií
        - Čítanie recenzií používateľov s hodnoteniami
        - Zobrazenie výživových informácií
        - Viacjazyčné rozhranie
        
        **Zdroj dát:** [Food.com Recipes and Interactions](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions)
        
        Ak chcete začať, uistite sa, že máte CSV súbory v priečinku aplikácie a kliknite na tlačidlo nižšie!
        """,
        "ru": """
        **Food.com Recipes Explorer** - это интерактивное веб-приложение, которое позволяет исследовать:
        
        🍽️ **Коллекцию рецептов** - Просматривайте 230 000+ рецептов с ингредиентами и шагами приготовления
        💬 **Отзывы пользователей** - Читайте 1 000 000+ отзывов и оценок
        📊 **Анализ данных** - Анализируйте структуру datasets и статистику
        
        **Основные функции:**
        - Поиск рецептов по названию, времени приготовления и ингредиентам
        - Чтение отзывов пользователей с оценками
        - Просмотр информации о пищевой ценности
        - Многоязычный интерфейс
        
        **Источник данных:** [Food.com Recipes and Interactions](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions)
        
        Чтобы начать, убедитесь что CSV файлы находятся в папке с приложением и нажмите кнопку ниже!
        """
    }
    
    st.markdown(welcome_texts[selected_lang])
    
    # Кнопка начала работы
    if st.button("Get Started / Začať / Начать" if selected_lang == "en" else
                 "Začať" if selected_lang == "sk" else "Начать"):
        st.session_state.first_visit = True
        st.session_state.language = selected_lang
        st.rerun()

def run_main_app():
    """Основное приложение после выбора языка"""
    lang = st.session_state.language
    t = lambda key: get_text(lang, key)
    
    # Заголовок приложения
    st.title(t("app_title"))
    st.markdown(t("app_subtitle"))
    
    # Переключатель языка в верхнем правом углу
    col1, col2, col3 = st.columns([3, 1, 1])
    with col3:
        new_lang = st.selectbox(
            "🌐 Language / Jazyk / Язык",
            ["en", "sk", "ru"],
            index=["en", "sk", "ru"].index(lang),
            format_func=lambda x: LANGUAGES[x]["language_name"]
        )
        if new_lang != lang:
            st.session_state.language = new_lang
            st.rerun()
    
    # Поиск CSV файлов
    csv_files = find_csv_files()
    
    if not csv_files:
        st.error(t("file_not_found"))
        st.info(t("file_instructions"))
        return
    
    # Основное приложение
    render_app(csv_files, t)

def find_csv_files():
    """Находит все CSV файлы"""
    csv_files = {}
    for file in Path(".").glob("*.csv"):
        csv_files[file.name] = str(file)
    
    data_dir = Path("data")
    if data_dir.exists():
        for file in data_dir.glob("*.csv"):
            csv_files[file.name] = str(file)
    
    return csv_files

def render_app(csv_files, t):
    """Основной интерфейс приложения"""
    
    # Боковая панель
    with st.sidebar:
        render_sidebar(csv_files, t)
    
    # Основной контент
    render_main_content(t)

def render_sidebar(csv_files, t):
    """Боковая панель с навигацией"""
    st.header(t("navigation"))
    
    # Выбор режима
    app_mode = st.radio(
        t("view_mode"),
        t("view_modes"),
        index=0
    )
    
    st.session_state.app_mode = app_mode
    
    st.header(t("data_selection"))
    
    # Приоритетные файлы для пользователя
    priority_files = {
        "RAW_recipes.csv": "📖 " + ("Recipes" if t("language_name") == "English" else "Recepty" if t("language_name") == "Slovensky" else "Рецепты"),
        "RAW_interactions.csv": "💬 " + ("Reviews" if t("language_name") == "English" else "Recenzie" if t("language_name") == "Slovensky" else "Отзывы"), 
    }
    
    available_priority_files = {k: v for k, v in priority_files.items() if k in csv_files}
    
    if available_priority_files:
        selected_file = st.selectbox(
            t("select_data"),
            list(available_priority_files.keys()),
            format_func=lambda x: available_priority_files[x]
        )
        st.session_state.selected_file = csv_files[selected_file]
        st.session_state.selected_file_name = selected_file
    
    # Информация
    st.header(t("about_data"))
    st.info(t("data_info"))

def render_main_content(t):
    """Основной контент в зависимости от режима"""
    if not hasattr(st.session_state, 'app_mode'):
        return
    
    if st.session_state.app_mode == t("view_modes")[0]:  # Recipes
        show_recipes_mode(t)
    elif st.session_state.app_mode == t("view_modes")[1]:  # Reviews
        show_reviews_mode(t)
    else:  # Analysis
        show_analysis_mode(t)

def show_recipes_mode(t):
    """Режим просмотра рецептов"""
    st.header(t("recipes_title"))
    
    if not hasattr(st.session_state, 'selected_file'):
        st.warning(t("select_file_sidebar"))
        return
    
    # Загрузка данных
    df = load_data(st.session_state.selected_file)
    if df is None:
        return
    
    # Фильтры для рецептов
    st.subheader(t("search_recipes"))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_name = st.text_input(t("recipe_name"), placeholder=t("name_placeholder"))
    
    with col2:
        max_time = st.number_input(t("max_time"), min_value=0, max_value=1000, value=120)
    
    with col3:
        max_ingredients = st.number_input(t("max_ingredients"), min_value=1, max_value=50, value=15)
    
    # Применение фильтров
    filtered_df = df.copy()
    
    if search_name:
        filtered_df = filtered_df[filtered_df['name'].str.contains(search_name, case=False, na=False)]
    
    if 'minutes' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['minutes'] <= max_time]
    
    if 'n_ingredients' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['n_ingredients'] <= max_ingredients]
    
    # Показ результатов
    st.subheader(f"{t('found_recipes')} {len(filtered_df)}")
    
    if len(filtered_df) == 0:
        st.info(t("no_recipes"))
        return
    
    # Показ рецептов в карточках
    for idx, recipe in filtered_df.head(20).iterrows():
        with st.expander(f"🍳 {recipe.get('name', 'No name')}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                if 'minutes' in recipe:
                    st.write(f"**{t('cooking_time')}** {recipe['minutes']} " + ("minutes" if t("language_name") == "English" else "minút" if t("language_name") == "Slovensky" else "минут"))
                
                if 'n_ingredients' in recipe:
                    st.write(f"**{t('ingredients_count')}** {recipe['n_ingredients']}")
                
                if 'n_steps' in recipe:
                    st.write(f"**{t('steps_count')}** {recipe['n_steps']}")
                
                # Ингредиенты
                if 'ingredients' in recipe and pd.notna(recipe['ingredients']):
                    st.subheader(t("ingredients_title"))
                    try:
                        ingredients = eval(recipe['ingredients']) if isinstance(recipe['ingredients'], str) else recipe['ingredients']
                        for ing in ingredients[:10]:
                            st.write(f"- {ing}")
                        if len(ingredients) > 10:
                            st.write(f"... " + ("and" if t("language_name") == "English" else "a" if t("language_name") == "Slovensky" else "и") + f" {len(ingredients) - 10} " + ("more ingredients" if t("language_name") == "English" else "ďalších ingrediencií" if t("language_name") == "Slovensky" else "ингредиентов"))
                    except:
                        st.write("Unable to read ingredients" if t("language_name") == "English" else "Nepodarilo sa prečítať ingrediencie" if t("language_name") == "Slovensky" else "Не удалось прочитать ингредиенты")
            
            with col2:
                if 'nutrition' in recipe and pd.notna(recipe['nutrition']):
                    st.subheader(t("nutrition_title"))
                    try:
                        nutrition = eval(recipe['nutrition']) if isinstance(recipe['nutrition'], str) else recipe['nutrition']
                        nutrients = [
                            t('calories') if 'calories' in t else 'Calories', 
                            t('fat') if 'fat' in t else 'Fat',
                            t('sugar') if 'sugar' in t else 'Sugar', 
                            t('sodium') if 'sodium' in t else 'Sodium',
                            t('protein') if 'protein' in t else 'Protein',
                            t('saturated_fat') if 'saturated_fat' in t else 'Saturated fat'
                        ]
                        if len(nutrition) >= 6:
                            for i, (nutrient, value) in enumerate(zip(nutrients, nutrition[:6])):
                                st.write(f"{nutrient}: {value}")
                    except:
                        st.write("Unable to read nutrition" if t("language_name") == "English" else "Nepodarilo sa prečítať výživové hodnoty" if t("language_name") == "Slovensky" else "Не удалось прочитать пищевую ценность")
            
            # Шаги приготовления
            if 'steps' in recipe and pd.notna(recipe['steps']):
                st.subheader(t("cooking_steps"))
                try:
                    steps = eval(recipe['steps']) if isinstance(recipe['steps'], str) else recipe['steps']
                    for i, step in enumerate(steps[:5], 1):
                        st.write(f"{i}. {step}")
                    if len(steps) > 5:
                        st.write(f"... " + ("and" if t("language_name") == "English" else "a" if t("language_name") == "Slovensky" else "и") + f" {len(steps) - 5} " + ("more steps" if t("language_name") == "English" else "ďalších krokov" if t("language_name") == "Slovensky" else "шагов"))
                except:
                    st.write("Unable to read cooking steps" if t("language_name") == "English" else "Nepodarilo sa prečítať kroky varenia" if t("language_name") == "Slovensky" else "Не удалось прочитать шаги приготовления")
            
            # Теги
            if 'tags' in recipe and pd.notna(recipe['tags']):
                try:
                    tags = eval(recipe['tags']) if isinstance(recipe['tags'], str) else recipe['tags']
                    if tags:
                        st.write(f"**{t('tags')}**", ", ".join(tags[:8]))
                except:
                    pass

def show_reviews_mode(t):
    """Режим чтения отзывов"""
    st.header(t("reviews_title"))
    
    if not hasattr(st.session_state, 'selected_file'):
        st.warning(t("select_reviews_sidebar"))
        return
    
    df = load_data(st.session_state.selected_file)
    if df is None:
        return
    
    # Фильтры для отзывов
    st.subheader(t("filters"))
    
    col1, col2 = st.columns(2)
    
    with col1:
        min_rating = st.slider(t("min_rating"), 1, 5, 3)
    
    with col2:
        review_count = st.slider(t("reviews_count"), 1, 50, 10)
    
    # Применение фильтров
    filtered_df = df.copy()
    
    if 'rating' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['rating'] >= min_rating]
    
    # Показ отзывов
    st.subheader(t("latest_reviews").format(min_rating))
    
    for idx, review in filtered_df.head(review_count).iterrows():
        rating_emoji = "⭐" * int(review.get('rating', 0))
        
        with st.container():
            st.markdown(f"### {rating_emoji} {t('rating')} {review.get('rating', 'N/A')}")
            
            if 'review' in review and pd.notna(review['review']):
                st.write(review['review'])
            else:
                st.write(t("no_review_text"))
            
            col1, col2 = st.columns(2)
            with col1:
                if 'date' in review:
                    st.caption(f"{t('date')} {review['date']}")
            with col2:
                if 'user_id' in review:
                    st.caption(f"{t('user')} {review['user_id']}")
            
            st.divider()

def show_analysis_mode(t):
    """Режим анализа данных"""
    st.header(t("analysis_title"))
    
    if not hasattr(st.session_state, 'selected_file'):
        st.warning(t("select_analysis_sidebar"))
        return
    
    df = load_data(st.session_state.selected_file)
    if df is None:
        return
    
    # Основная статистика
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(t("total_records"), df.shape[0])
    with col2:
        st.metric(t("columns"), df.shape[1])
    with col3:
        st.metric(t("data_size"), f"{df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    with col4:
        st.metric(t("duplicates"), df.duplicated().sum())
    
    # Информация о столбцах
    st.subheader(t("data_structure"))
    
    col_info = pd.DataFrame({
        t('column'): df.columns,
        t('data_type'): df.dtypes,
        t('completeness'): (df.count() / len(df) * 100).round(1).astype(str) + '%',
        t('unique'): df.nunique()
    })
    
    st.dataframe(col_info, use_container_width=True, hide_index=True)
    
    # Быстрый просмотр данных
    st.subheader(t("data_preview"))
    st.dataframe(df.head(10), use_container_width=True)

def load_data(file_path):
    """Загружает данные с кэшированием"""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"❌ Error loading data: {e}" if st.session_state.language == "en" else 
                 f"❌ Chyba pri načítaní dát: {e}" if st.session_state.language == "sk" else
                 f"❌ Ошибка загрузки данных: {e}")
        return None

if __name__ == "__main__":
    main()