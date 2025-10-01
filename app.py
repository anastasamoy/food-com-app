import streamlit as st
import pandas as pd
import numpy as np
import os
import ast
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from languages import get_text, LANGUAGES

# Page config
st.set_page_config(
    page_title="Food.com Recipes",
    page_icon="🍳",
    layout="wide"
)

def load_data():
    """Load recipe data from CSV files"""
    data_files = {}
    
    # Look for CSV files in current directory and data folder
    search_paths = [".", "data"]
    
    for path in search_paths:
        if os.path.exists(path):
            for file in os.listdir(path):
                if file.endswith('.csv'):
                    full_path = os.path.join(path, file)
                    data_files[file] = full_path
    
    return data_files

def main():
    # Language selection
    col1, col2 = st.columns([3, 1])
    
    with col2:
        language = st.selectbox(
            "Language / Язык / Jazyk",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: LANGUAGES[x]["language_name"]
        )
    
    with col1:
        st.title(get_text(language, "app_title"))
        st.markdown(get_text(language, "app_subtitle"))
    
    # Load available data files
    data_files = load_data()
    
    if not data_files:
        st.error(get_text(language, "file_not_found"))
        st.markdown(get_text(language, "file_instructions"))
        return
    
    # Sidebar navigation
    st.sidebar.header(get_text(language, "navigation"))
    
    # View mode selection
    view_mode = st.sidebar.radio(
        get_text(language, "view_mode"),
        get_text(language, "view_modes")
    )
    
    # Data file selection
    st.sidebar.header(get_text(language, "data_selection"))
    
    if "📖" in view_mode:  # Recipes mode
        recipe_files = [f for f in data_files.keys() if 'recipe' in f.lower()]
        # Prioritize RAW_recipes.csv
        if 'RAW_recipes.csv' in recipe_files:
            default_idx = recipe_files.index('RAW_recipes.csv')
        else:
            default_idx = 0
            
        if recipe_files:
            selected_file = st.sidebar.selectbox(
                get_text(language, "select_data"),
                recipe_files,
                index=default_idx
            )
            show_recipes(data_files[selected_file], language)
        else:
            st.error(get_text(language, "select_file_sidebar"))
            
    elif "💬" in view_mode:  # Reviews mode
        review_files = [f for f in data_files.keys() if 'interaction' in f.lower()]
        # Prioritize RAW_interactions.csv
        if 'RAW_interactions.csv' in review_files:
            default_idx = review_files.index('RAW_interactions.csv')
        else:
            default_idx = 0
            
        if review_files:
            selected_file = st.sidebar.selectbox(
                get_text(language, "select_data"),
                review_files,
                index=default_idx
            )
            show_reviews(data_files[selected_file], language)
        else:
            st.error(get_text(language, "select_reviews_sidebar"))
            
    elif "📊" in view_mode:  # Analysis mode
        st.sidebar.write("**Available datasets:**")
        for file_name in data_files.keys():
            file_size = os.path.getsize(data_files[file_name]) / (1024*1024)  # MB
            st.sidebar.write(f"• {file_name} ({file_size:.1f} MB)")
        
        selected_file = st.sidebar.selectbox(
            get_text(language, "select_data"),
            list(data_files.keys())
        )
        show_analysis(data_files[selected_file], language)

def show_recipes(file_path, language):
    """Display enhanced recipes interface"""
    st.header(get_text(language, "recipes_title"))
    
    try:
        # Load data with progress bar
        with st.spinner("Loading recipes..."):
            df = pd.read_csv(file_path, nrows=5000)  # Increased limit
        
        # Enhanced filters sidebar
        st.sidebar.subheader("🔍 Recipe Filters")
        
        # Clear filters button
        if st.sidebar.button("🗑️ Clear All Filters"):
            st.rerun()
        
        # Search by name
        search_term = st.sidebar.text_input(
            get_text(language, "recipe_name"),
            placeholder=get_text(language, "name_placeholder")
        )
        
        # Time filter
        if 'minutes' in df.columns:
            min_time, max_time = st.sidebar.slider(
                "⏱️ Cooking time (minutes)",
                int(df['minutes'].min()), 
                int(df['minutes'].max()), 
                (0, 120)
            )
        
        # Ingredients filter
        if 'n_ingredients' in df.columns:
            min_ingr, max_ingr = st.sidebar.slider(
                "🛒 Number of ingredients",
                int(df['n_ingredients'].min()),
                int(df['n_ingredients'].max()),
                (1, 20)
            )
        
        # Enhanced category filters
        if 'tags' in df.columns:
            st.sidebar.subheader("📋 Recipe Categories")
            
            # Meal Type Filter
            meal_types = {
                "🌅 Breakfast": ['breakfast', 'brunch', 'breakfast-eggs'],
                "🥪 Lunch": ['lunch', 'lunch-snacks'],  
                "🍽️ Dinner": ['main-dish', 'dinner-party'],
                "🍰 Desserts": ['desserts', 'frozen-desserts'],
                "🥨 Appetizers": ['appetizers', 'snacks'],
                "🍹 Drinks": ['cocktails', 'beverages'],
                "🥗 Side Dishes": ['side-dishes']
            }
            
            selected_meal_types = st.sidebar.multiselect(
                "🍽️ Meal Types",
                list(meal_types.keys())
            )
            
            # Cuisine Filter  
            st.sidebar.subheader("🌍 World Cuisines")
            cuisines = {
                "🇲🇽 Mexican": ['mexican'],
                "🇮🇹 Italian": ['italian'],
                "🇺🇸 American": ['american', 'north-american'],
                "🇨🇳 Chinese": ['chinese'],
                "🇮🇳 Indian": ['indian'],
                "🇫🇷 French": ['french'],
                "🇹🇭 Thai": ['thai'],
                "🇯🇵 Japanese": ['japanese'],
                "🇪🇸 Spanish": ['spanish'],
                "🌏 Asian": ['asian']
            }
            
            selected_cuisines = st.sidebar.multiselect(
                "🌍 Select Cuisines",
                list(cuisines.keys())
            )
            
            # Diet & Health Filter
            st.sidebar.subheader("🥗 Diet & Health")
            diet_options = {
                "🌱 Vegetarian": ['vegetarian'],
                "🌿 Vegan": ['vegan'],
                "💪 Healthy": ['healthy', 'healthy-2'],
                "🔥 Low-Carb": ['low-carb', 'very-low-carbs'],
                "🧈 Low-Fat": ['low-fat'],
                "🧂 Low-Sodium": ['low-sodium'],
                "❤️ Low-Cholesterol": ['low-cholesterol'],
                "🍯 Diabetic": ['diabetic'],
                "🌾 Gluten-Free": ['gluten-free']
            }
            
            selected_diets = st.sidebar.multiselect(
                "🥗 Dietary Preferences",
                list(diet_options.keys())
            )
            
            # Cooking Method Filter
            st.sidebar.subheader("👩‍🍳 Cooking Methods")
            cooking_methods = {
                "🥘 Slow Cooker": ['crock-pot-slow-cooker'],
                "🔥 Grilling": ['grilling', 'barbecue'],
                "🥧 Baking": ['oven', 'baking'],
                "⚡ Quick & Easy": ['15-minutes-or-less', '30-minutes-or-less', 'easy'],
                "🍳 Beginner": ['beginner-cook', '3-steps-or-less'],
                "💰 Budget": ['inexpensive', '5-ingredients-or-less']
            }
            
            selected_methods = st.sidebar.multiselect(
                "👩‍� Cooking Style",
                list(cooking_methods.keys())
            )
            
            # Occasion Filter
            st.sidebar.subheader("🎉 Special Occasions")
            occasions = {
                "🎄 Christmas": ['christmas'],
                "🎃 Halloween": ['halloween'],  
                "🦃 Thanksgiving": ['thanksgiving'],
                "💕 Valentine's": ['valentines-day'],
                "☘️ St Patrick's": ['st-patricks-day'],
                "🐰 Easter": ['easter'],
                "🎆 4th of July": ['4th-of-july'],
                "🎊 New Year": ['new-years'],
                "🎂 Birthday": ['birthday'],
                "🥳 Party": ['dinner-party', 'party']
            }
            
            selected_occasions = st.sidebar.multiselect(
                "🎉 Occasions",
                list(occasions.keys())
            )
            
            # Seasonal Filter
            st.sidebar.subheader("🌿 Seasonal")
            seasons = {
                "🌸 Spring": ['spring'],
                "☀️ Summer": ['summer'],
                "🍂 Fall": ['fall', 'autumn'],
                "❄️ Winter": ['winter']
            }
            
            selected_seasons = st.sidebar.multiselect(
                "🌿 Seasons",
                list(seasons.keys())
            )
            
            # Difficulty Filter
            st.sidebar.subheader("⭐ Difficulty Level")
            difficulty_levels = {
                "👶 Beginner": ['beginner-cook', '3-steps-or-less', 'easy'],
                "⚡ Quick (15 min)": ['15-minutes-or-less'],
                "🕐 Medium (30 min)": ['30-minutes-or-less'],
                "🕒 Long (60 min)": ['60-minutes-or-less'],
                "👨‍🍳 Advanced": ['intermediate-cook', 'advanced']
            }
            
            selected_difficulty = st.sidebar.multiselect(
                "⭐ Recipe Difficulty",
                list(difficulty_levels.keys())
            )
        
        # Nutrition filters
        if 'nutrition' in df.columns:
            st.sidebar.subheader("📊 Nutrition Filters")
            
            # Extract nutrition data for filtering
            nutrition_data = []
            for nutrition_str in df['nutrition'].dropna().head(1000):
                try:
                    nutrition = ast.literal_eval(nutrition_str)
                    if len(nutrition) >= 7:
                        nutrition_data.append(nutrition)
                except:
                    continue
            
            if nutrition_data:
                nutrition_df = pd.DataFrame(nutrition_data, 
                    columns=['calories', 'fat', 'sugar', 'sodium', 'protein', 'saturated_fat', 'carbs'])
                
                # Calorie filter
                if not nutrition_df['calories'].isna().all():
                    cal_range = st.sidebar.slider(
                        "🔥 Calories",
                        0, 1000, (0, 500)
                    )
        
        # Apply filters
        filtered_df = df.copy()
        
        # Name filter
        if search_term:
            filtered_df = filtered_df[
                filtered_df['name'].str.contains(search_term, case=False, na=False)
            ]
        
        # Time filter
        if 'minutes' in df.columns:
            filtered_df = filtered_df[
                (filtered_df['minutes'] >= min_time) & 
                (filtered_df['minutes'] <= max_time)
            ]
        
        # Ingredients filter
        if 'n_ingredients' in df.columns:
            filtered_df = filtered_df[
                (filtered_df['n_ingredients'] >= min_ingr) & 
                (filtered_df['n_ingredients'] <= max_ingr)
            ]
        
        # Apply category filters
        if 'tags' in df.columns:
            # Combine all selected filters
            all_selected_tags = []
            
            # Add meal type tags
            if selected_meal_types:
                for meal_type in selected_meal_types:
                    all_selected_tags.extend(meal_types[meal_type])
            
            # Add cuisine tags
            if selected_cuisines:
                for cuisine in selected_cuisines:
                    all_selected_tags.extend(cuisines[cuisine])
            
            # Add diet tags
            if selected_diets:
                for diet in selected_diets:
                    all_selected_tags.extend(diet_options[diet])
            
            # Add cooking method tags
            if selected_methods:
                for method in selected_methods:
                    all_selected_tags.extend(cooking_methods[method])
            
            # Add occasion tags
            if selected_occasions:
                for occasion in selected_occasions:
                    all_selected_tags.extend(occasions[occasion])
            
            # Add seasonal tags
            if selected_seasons:
                for season in selected_seasons:
                    all_selected_tags.extend(seasons[season])
            
            # Add difficulty tags
            if selected_difficulty:
                for difficulty in selected_difficulty:
                    all_selected_tags.extend(difficulty_levels[difficulty])
            
            # Apply tag filter if any tags selected
            if all_selected_tags:
                def check_tags(tags_str):
                    if pd.isna(tags_str):
                        return False
                    try:
                        tags = ast.literal_eval(str(tags_str))
                        return any(tag in tags for tag in all_selected_tags)
                    except:
                        return False
                
                filtered_df = filtered_df[filtered_df['tags'].apply(check_tags)]
        
        # Display filter summary and results
        st.subheader(f"🍽️ Found {len(filtered_df):,} recipes out of {len(df):,} total")
        
        # Show active filters summary
        active_filters = []
        if selected_meal_types:
            active_filters.extend([f"📋 {meal}" for meal in selected_meal_types])
        if selected_cuisines:
            active_filters.extend([f"🌍 {cuisine}" for cuisine in selected_cuisines])
        if selected_diets:
            active_filters.extend([f"🥗 {diet}" for diet in selected_diets])
        if selected_methods:
            active_filters.extend([f"👩‍🍳 {method}" for method in selected_methods])
        if selected_occasions:
            active_filters.extend([f"🎉 {occasion}" for occasion in selected_occasions])
        if selected_seasons:
            active_filters.extend([f"🌿 {season}" for season in selected_seasons])
        if selected_difficulty:
            active_filters.extend([f"⭐ {diff}" for diff in selected_difficulty])
        
        if active_filters:
            st.info(f"**Active filters:** {', '.join(active_filters)}")
        
        # Quick stats
        if len(filtered_df) > 0:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                avg_time = filtered_df['minutes'].mean() if 'minutes' in filtered_df.columns else 0
                st.metric("⏱️ Avg Time", f"{avg_time:.0f} min")
            
            with col2:
                avg_ingredients = filtered_df['n_ingredients'].mean() if 'n_ingredients' in filtered_df.columns else 0
                st.metric("🛒 Avg Ingredients", f"{avg_ingredients:.0f}")
            
            with col3:
                avg_steps = filtered_df['n_steps'].mean() if 'n_steps' in filtered_df.columns else 0
                st.metric("👩‍🍳 Avg Steps", f"{avg_steps:.0f}")
            
            with col4:
                if 'nutrition' in filtered_df.columns:
                    # Calculate average calories
                    calories_list = []
                    for nutrition_str in filtered_df['nutrition'].dropna():
                        try:
                            nutrition = ast.literal_eval(nutrition_str)
                            if len(nutrition) > 0:
                                calories_list.append(nutrition[0])
                        except:
                            continue
                    avg_calories = sum(calories_list) / len(calories_list) if calories_list else 0
                    st.metric("🔥 Avg Calories", f"{avg_calories:.0f}")
        
        # Results per page
        results_per_page = st.selectbox("📄 Results per page", [5, 10, 20, 50], index=1)
        
        if len(filtered_df) > 0:
            # Pagination
            total_pages = (len(filtered_df) - 1) // results_per_page + 1
            if total_pages > 1:
                page = st.selectbox(f"Page (1-{total_pages})", range(1, total_pages + 1))
                start_idx = (page - 1) * results_per_page
                end_idx = start_idx + results_per_page
                page_df = filtered_df.iloc[start_idx:end_idx]
            else:
                page_df = filtered_df.head(results_per_page)
            
            # Show recipes
            for idx, recipe in page_df.iterrows():
                with st.expander(f"🍽️ {recipe['name']}"):
                    
                    # Recipe header with stats
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        if 'minutes' in recipe and pd.notna(recipe['minutes']):
                            st.metric("⏱️ Time", f"{recipe['minutes']} min")
                    
                    with col2:
                        if 'n_ingredients' in recipe and pd.notna(recipe['n_ingredients']):
                            st.metric("🛒 Ingredients", recipe['n_ingredients'])
                    
                    with col3:
                        if 'n_steps' in recipe and pd.notna(recipe['n_steps']):
                            st.metric("👩‍🍳 Steps", recipe['n_steps'])
                    
                    with col4:
                        # Rating (if available)
                        st.metric("📊 Recipe ID", recipe.get('id', 'N/A'))
                    
                    st.divider()
                    
                    # Main content
                    col_left, col_right = st.columns([2, 1])
                    
                    with col_left:
                        # Description
                        if 'description' in recipe and pd.notna(recipe['description']):
                            st.markdown("**📝 Description:**")
                            st.write(recipe['description'])
                        
                        # Cooking steps
                        if 'steps' in recipe and pd.notna(recipe['steps']):
                            st.markdown("**👩‍🍳 Cooking Steps:**")
                            try:
                                steps = ast.literal_eval(recipe['steps'])
                                for i, step in enumerate(steps, 1):
                                    st.write(f"{i}. {step}")
                            except:
                                st.write(recipe['steps'])
                        
                        # Ingredients list
                        if 'ingredients' in recipe and pd.notna(recipe['ingredients']):
                            st.markdown("**🛒 Ingredients:**")
                            try:
                                ingredients = ast.literal_eval(recipe['ingredients'])
                                # Display in columns for better layout
                                ing_cols = st.columns(2)
                                for i, ingredient in enumerate(ingredients):
                                    with ing_cols[i % 2]:
                                        st.write(f"• {ingredient}")
                            except:
                                st.write(recipe['ingredients'])
                    
                    with col_right:
                        # Nutrition info
                        if 'nutrition' in recipe and pd.notna(recipe['nutrition']):
                            st.markdown("**📊 Nutrition (per serving):**")
                            try:
                                nutrition = ast.literal_eval(recipe['nutrition'])
                                nutrition_labels = ['Calories', 'Fat (g)', 'Sugar (g)', 
                                                  'Sodium (mg)', 'Protein (g)', 
                                                  'Saturated Fat (g)', 'Carbs (g)']
                                
                                for i, (label, value) in enumerate(zip(nutrition_labels, nutrition)):
                                    if i < len(nutrition):
                                        st.write(f"• **{label}:** {value}")
                            except:
                                st.write("Nutrition data available")
                        
                        # Enhanced Tags/Categories display
                        if 'tags' in recipe and pd.notna(recipe['tags']):
                            st.markdown("**🏷️ Categories:**")
                            try:
                                tags = ast.literal_eval(recipe['tags'])
                                
                                # Categorize tags for better display
                                cuisine_found = []
                                diet_found = []
                                method_found = []
                                occasion_found = []
                                
                                cuisine_keywords = ['mexican', 'italian', 'american', 'chinese', 'indian', 
                                                   'french', 'thai', 'japanese', 'spanish', 'asian']
                                diet_keywords = ['vegetarian', 'vegan', 'healthy', 'low-carb', 'low-fat', 
                                               'low-sodium', 'diabetic', 'gluten-free']
                                method_keywords = ['easy', 'quick', 'slow-cooker', 'oven', 'grilling', 
                                                  'baking', 'beginner-cook']
                                occasion_keywords = ['christmas', 'halloween', 'thanksgiving', 'party', 
                                                    'birthday', 'holiday']
                                
                                for tag in tags:
                                    tag_lower = tag.lower()
                                    if any(keyword in tag_lower for keyword in cuisine_keywords):
                                        cuisine_found.append(tag)
                                    elif any(keyword in tag_lower for keyword in diet_keywords):
                                        diet_found.append(tag)
                                    elif any(keyword in tag_lower for keyword in method_keywords):
                                        method_found.append(tag)
                                    elif any(keyword in tag_lower for keyword in occasion_keywords):
                                        occasion_found.append(tag)
                                
                                # Display categorized tags
                                if cuisine_found:
                                    st.write("🌍 **Cuisine:** " + ", ".join([t.replace('-', ' ').title() for t in cuisine_found[:3]]))
                                if diet_found:
                                    st.write("🥗 **Diet:** " + ", ".join([t.replace('-', ' ').title() for t in diet_found[:3]]))
                                if method_found:
                                    st.write("👩‍🍳 **Method:** " + ", ".join([t.replace('-', ' ').title() for t in method_found[:3]]))
                                if occasion_found:
                                    st.write("🎉 **Occasion:** " + ", ".join([t.replace('-', ' ').title() for t in occasion_found[:2]]))
                                
                                # Show some general tags
                                general_tags = [tag for tag in tags if tag not in cuisine_found + diet_found + method_found + occasion_found]
                                if general_tags:
                                    relevant_general = [tag.replace('-', ' ').title() for tag in general_tags[:5] 
                                                      if tag not in ['preparation', 'time-to-make', 'course', 'main-ingredient']]
                                    if relevant_general:
                                        st.write("📋 **Other:** " + ", ".join(relevant_general))
                                        
                            except Exception as e:
                                st.write("Categories available")
                        
                        # Contributor info
                        if 'contributor_id' in recipe and pd.notna(recipe['contributor_id']):
                            st.write(f"**👤 Contributor:** {recipe['contributor_id']}")
                        
                        if 'submitted' in recipe and pd.notna(recipe['submitted']):
                            st.write(f"**📅 Submitted:** {recipe['submitted']}")
        
        else:
            st.info(get_text(language, "no_recipes"))
            st.write("Try adjusting your filters to see more recipes.")
            
    except Exception as e:
        st.error(f"Error loading recipes: {str(e)}")
        st.write("Please make sure you have selected the correct recipe file (RAW_recipes.csv)")

def show_reviews(file_path, language):
    """Display enhanced reviews interface"""
    st.header(get_text(language, "reviews_title"))
    
    try:
        with st.spinner("Loading reviews..."):
            df = pd.read_csv(file_path, nrows=10000)
        
        # Load recipe data for joining
        recipe_files = [f for f in os.listdir('data') if 'RAW_recipes.csv' in f]
        recipes_df = None
        if recipe_files:
            recipes_df = pd.read_csv(f'data/{recipe_files[0]}', nrows=5000)
        
        # Enhanced filters in sidebar
        st.sidebar.subheader("🔍 Review Filters")
        
        # Rating filter
        if 'rating' in df.columns:
            rating_options = [1, 2, 3, 4, 5]
            selected_ratings = st.sidebar.multiselect(
                "⭐ Rating", 
                rating_options,
                default=[4, 5]
            )
        
        # Date filter
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            min_date = df['date'].min()
            max_date = df['date'].max()
            
            date_range = st.sidebar.date_input(
                "📅 Date range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
        
        # Review length filter
        if 'review' in df.columns:
            df['review_length'] = df['review'].astype(str).str.len()
            min_length = st.sidebar.slider(
                "📝 Minimum review length", 
                0, 500, 50
            )
        
        # Search in reviews
        search_text = st.sidebar.text_input(
            "🔍 Search in reviews",
            placeholder="Enter keywords..."
        )
        
        # Apply filters
        filtered_df = df.copy()
        
        # Rating filter
        if 'rating' in df.columns and selected_ratings:
            filtered_df = filtered_df[filtered_df['rating'].isin(selected_ratings)]
        
        # Date filter
        if 'date' in df.columns and len(date_range) == 2:
            filtered_df = filtered_df[
                (filtered_df['date'] >= pd.Timestamp(date_range[0])) &
                (filtered_df['date'] <= pd.Timestamp(date_range[1]))
            ]
        
        # Review length filter
        if 'review' in df.columns:
            filtered_df = filtered_df[filtered_df['review_length'] >= min_length]
        
        # Text search filter
        if search_text and 'review' in df.columns:
            filtered_df = filtered_df[
                filtered_df['review'].str.contains(search_text, case=False, na=False)
            ]
        
        # Display statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Total Reviews", len(filtered_df))
        
        with col2:
            if 'rating' in filtered_df.columns:
                avg_rating = filtered_df['rating'].mean()
                st.metric("⭐ Average Rating", f"{avg_rating:.2f}")
        
        with col3:
            if 'review' in filtered_df.columns:
                avg_length = filtered_df['review_length'].mean()
                st.metric("📝 Avg Review Length", f"{avg_length:.0f}")
        
        with col4:
            unique_users = filtered_df['user_id'].nunique() if 'user_id' in filtered_df.columns else 0
            st.metric("👥 Unique Users", unique_users)
        
        # Rating distribution chart
        if 'rating' in filtered_df.columns and len(filtered_df) > 0:
            st.subheader("📈 Rating Distribution")
            rating_counts = filtered_df['rating'].value_counts().sort_index()
            
            fig = px.bar(
                x=rating_counts.index, 
                y=rating_counts.values,
                labels={'x': 'Rating', 'y': 'Count'},
                title="Distribution of Ratings"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Pagination for reviews
        st.subheader(f"{get_text(language, 'latest_reviews').format('All')}")
        
        reviews_per_page = st.selectbox("Reviews per page", [10, 25, 50, 100], index=1)
        
        if len(filtered_df) > 0:
            # Sort by date (newest first) or rating
            sort_option = st.selectbox(
                "Sort by", 
                ["Date (Newest)", "Date (Oldest)", "Rating (High)", "Rating (Low)", "Review Length"]
            )
            
            if sort_option == "Date (Newest)" and 'date' in filtered_df.columns:
                filtered_df = filtered_df.sort_values('date', ascending=False)
            elif sort_option == "Date (Oldest)" and 'date' in filtered_df.columns:
                filtered_df = filtered_df.sort_values('date', ascending=True)
            elif sort_option == "Rating (High)" and 'rating' in filtered_df.columns:
                filtered_df = filtered_df.sort_values('rating', ascending=False)
            elif sort_option == "Rating (Low)" and 'rating' in filtered_df.columns:
                filtered_df = filtered_df.sort_values('rating', ascending=True)
            elif sort_option == "Review Length" and 'review' in filtered_df.columns:
                filtered_df = filtered_df.sort_values('review_length', ascending=False)
            
            # Pagination
            total_pages = (len(filtered_df) - 1) // reviews_per_page + 1
            if total_pages > 1:
                page = st.selectbox(f"Page (1-{total_pages})", range(1, total_pages + 1))
                start_idx = (page - 1) * reviews_per_page
                end_idx = start_idx + reviews_per_page
                page_df = filtered_df.iloc[start_idx:end_idx]
            else:
                page_df = filtered_df.head(reviews_per_page)
            
            # Display reviews
            for idx, review in page_df.iterrows():
                with st.expander(f"⭐ Rating: {review.get('rating', 'N/A')} - User: {review.get('user_id', 'Anonymous')}"):
                    
                    # Review header
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if 'rating' in review and pd.notna(review['rating']):
                            rating_stars = "⭐" * int(review['rating'])
                            st.write(f"**Rating:** {rating_stars} ({review['rating']}/5)")
                    
                    with col2:
                        if 'date' in review and pd.notna(review['date']):
                            st.write(f"**Date:** {review['date'].strftime('%Y-%m-%d') if hasattr(review['date'], 'strftime') else review['date']}")
                    
                    with col3:
                        if 'user_id' in review and pd.notna(review['user_id']):
                            st.write(f"**User ID:** {review['user_id']}")
                    
                    # Recipe information (if available)
                    if 'recipe_id' in review and recipes_df is not None:
                        recipe_info = recipes_df[recipes_df['id'] == review['recipe_id']]
                        if not recipe_info.empty:
                            recipe_name = recipe_info.iloc[0]['name']
                            st.write(f"**🍽️ Recipe:** {recipe_name}")
                    
                    # Review text
                    if 'review' in review and pd.notna(review['review']):
                        st.markdown("**📝 Review:**")
                        review_text = str(review['review'])
                        if len(review_text) > 1000:
                            with st.expander("Read full review..."):
                                st.write(review_text)
                        else:
                            st.write(review_text)
                        
                        # Review stats
                        st.caption(f"Review length: {len(review_text)} characters")
                    else:
                        st.write("*No review text provided*")
        
        else:
            st.info("No reviews found matching your criteria.")
            st.write("Try adjusting your filters to see more reviews.")
            
    except Exception as e:
        st.error(f"Error loading reviews: {str(e)}")
        st.write("Please make sure you have selected the correct reviews file (RAW_interactions.csv)")

def show_analysis(file_path, language):
    """Display comprehensive data analysis"""
    st.header(get_text(language, "analysis_title"))
    
    try:
        with st.spinner("Loading data for analysis..."):
            df = pd.read_csv(file_path, nrows=10000)
        
        # Analysis tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Overview", "🔍 Data Quality", "📈 Statistics", "🧮 Distributions", "🔗 Relationships"
        ])
        
        with tab1:
            # Basic overview
            st.subheader("📋 Dataset Overview")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📊 Total Records", f"{len(df):,}")
            
            with col2:
                st.metric("📈 Columns", len(df.columns))
            
            with col3:
                memory_usage = df.memory_usage(deep=True).sum() / 1024**2
                st.metric("💾 Memory Usage", f"{memory_usage:.1f} MB")
            
            with col4:
                duplicates = df.duplicated().sum()
                st.metric("🔍 Duplicates", f"{duplicates:,}")
            
            # File information
            file_name = os.path.basename(file_path)
            st.write(f"**📁 File:** {file_name}")
            st.write(f"**📅 Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            
            # Quick data preview
            st.subheader("👀 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Column types summary
            st.subheader("🏷️ Column Types Summary")
            dtype_counts = df.dtypes.value_counts()
            
            fig_pie = px.pie(
                values=dtype_counts.values,
                names=dtype_counts.index,
                title="Distribution of Column Data Types"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with tab2:
            # Data quality analysis
            st.subheader("🔍 Data Quality Assessment")
            
            # Missing data analysis
            missing_data = df.isnull().sum()
            missing_percent = (missing_data / len(df)) * 100
            
            quality_df = pd.DataFrame({
                'Column': df.columns,
                'Missing Count': missing_data.values,
                'Missing %': missing_percent.values,
                'Data Type': df.dtypes.values,
                'Unique Values': [df[col].nunique() for col in df.columns],
                'Completeness': [(1 - df[col].isnull().mean()) * 100 for col in df.columns]
            })
            
            # Sort by missing percentage
            quality_df = quality_df.sort_values('Missing %', ascending=False)
            
            st.dataframe(quality_df, use_container_width=True)
            
            # Missing data visualization
            if missing_data.sum() > 0:
                fig_missing = px.bar(
                    x=missing_data.index,
                    y=missing_percent.values,
                    title="Missing Data Percentage by Column",
                    labels={'x': 'Columns', 'y': 'Missing %'}
                )
                fig_missing.update_xaxis(tickangle=45)
                st.plotly_chart(fig_missing, use_container_width=True)
            
            # Data completeness heatmap
            st.subheader("🔥 Data Completeness Heatmap")
            completeness = df.notna().astype(int)
            
            if len(df) <= 1000:  # Only for reasonable dataset sizes
                fig_heatmap = px.imshow(
                    completeness.iloc[:100].T,  # Show first 100 rows
                    title="Data Completeness (White=Present, Black=Missing)",
                    aspect='auto'
                )
                st.plotly_chart(fig_heatmap, use_container_width=True)
        
        with tab3:
            # Statistical analysis
            st.subheader("📊 Statistical Summary")
            
            # Numeric columns analysis
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            
            if len(numeric_cols) > 0:
                st.write("**🔢 Numeric Columns Statistics:**")
                numeric_stats = df[numeric_cols].describe()
                st.dataframe(numeric_stats, use_container_width=True)
                
                # Correlation matrix for numeric columns
                if len(numeric_cols) > 1:
                    st.subheader("🔗 Correlation Matrix")
                    corr_matrix = df[numeric_cols].corr()
                    
                    fig_corr = px.imshow(
                        corr_matrix,
                        title="Correlation Matrix of Numeric Variables",
                        color_continuous_scale='RdBu',
                        aspect='auto'
                    )
                    st.plotly_chart(fig_corr, use_container_width=True)
            
            # Categorical columns analysis
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns
            
            if len(categorical_cols) > 0:
                st.write("**📝 Categorical Columns Analysis:**")
                
                for col in categorical_cols[:5]:  # Limit to first 5 categorical columns
                    if df[col].nunique() <= 20:  # Only for columns with reasonable number of unique values
                        st.write(f"**{col}:**")
                        value_counts = df[col].value_counts().head(10)
                        
                        fig_cat = px.bar(
                            x=value_counts.values,
                            y=value_counts.index,
                            orientation='h',
                            title=f"Top Values in {col}",
                            labels={'x': 'Count', 'y': col}
                        )
                        st.plotly_chart(fig_cat, use_container_width=True)
        
        with tab4:
            # Distribution analysis
            st.subheader("📈 Data Distributions")
            
            if len(numeric_cols) > 0:
                # Select column for distribution
                selected_col = st.selectbox(
                    "Select numeric column for distribution analysis:",
                    numeric_cols
                )
                
                if selected_col:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Histogram
                        fig_hist = px.histogram(
                            df,
                            x=selected_col,
                            title=f"Distribution of {selected_col}",
                            nbins=30
                        )
                        st.plotly_chart(fig_hist, use_container_width=True)
                    
                    with col2:
                        # Box plot
                        fig_box = px.box(
                            df,
                            y=selected_col,
                            title=f"Box Plot of {selected_col}"
                        )
                        st.plotly_chart(fig_box, use_container_width=True)
                    
                    # Statistical summary for selected column
                    st.write(f"**Statistics for {selected_col}:**")
                    stats = df[selected_col].describe()
                    
                    stat_cols = st.columns(len(stats))
                    for i, (stat_name, stat_value) in enumerate(stats.items()):
                        with stat_cols[i]:
                            st.metric(stat_name.title(), f"{stat_value:.2f}")
        
        with tab5:
            # Relationships analysis
            st.subheader("🔗 Data Relationships")
            
            if len(numeric_cols) >= 2:
                # Scatter plot analysis
                st.write("**📊 Scatter Plot Analysis:**")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    x_col = st.selectbox("X-axis:", numeric_cols, index=0)
                
                with col2:
                    y_col = st.selectbox("Y-axis:", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
                
                if x_col != y_col:
                    # Create scatter plot
                    sample_size = min(1000, len(df))  # Limit for performance
                    sample_df = df.sample(n=sample_size) if len(df) > sample_size else df
                    
                    fig_scatter = px.scatter(
                        sample_df,
                        x=x_col,
                        y=y_col,
                        title=f"Relationship between {x_col} and {y_col}",
                        opacity=0.6
                    )
                    st.plotly_chart(fig_scatter, use_container_width=True)
                    
                    # Correlation coefficient
                    correlation = df[x_col].corr(df[y_col])
                    st.metric("Correlation Coefficient", f"{correlation:.3f}")
            
            # Advanced insights
            st.subheader("🧠 Advanced Insights")
            
            insights = []
            
            # Check for potential issues
            if duplicates > 0:
                insights.append(f"⚠️ Found {duplicates:,} duplicate rows ({duplicates/len(df)*100:.1f}%)")
            
            # Check missing data
            high_missing = quality_df[quality_df['Missing %'] > 50]
            if len(high_missing) > 0:
                insights.append(f"⚠️ {len(high_missing)} columns have >50% missing data")
            
            # Check data skewness for numeric columns
            for col in numeric_cols[:3]:  # Check first 3 numeric columns
                skewness = df[col].skew()
                if abs(skewness) > 2:
                    insights.append(f"📊 Column '{col}' is highly skewed (skewness: {skewness:.2f})")
            
            # Check for potential outliers
            for col in numeric_cols[:3]:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)][col].count()
                if outliers > 0:
                    insights.append(f"📈 Column '{col}' has {outliers} potential outliers")
            
            if insights:
                st.write("**Key Insights:**")
                for insight in insights:
                    st.write(insight)
            else:
                st.success("✅ Data looks clean with no major issues detected!")
        
    except Exception as e:
        st.error(f"Error analyzing data: {str(e)}")
        st.write(f"File path: {file_path}")
        st.write("Please check that the file exists and is properly formatted.")

if __name__ == "__main__":
    main()