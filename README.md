
### 🌍 Multi-language Support
- **English** - Primary interface language
- **Slovak** (Slovensky) - Complete translation
- **Russian** (Русский) - Complete translation
- **Dynamic switching** - Real-time language change without reload

### 📊 Key Features Implemented

#### **1. Recipe Explorer**
- Search by recipe name, cooking time, ingredients count
- Expandable recipe cards with full details
- Ingredients listing with formatting
- Cooking steps display
- Nutritional information parsing
- Tags and categories

#### **2. Reviews System**
- User reviews with star ratings
- Filter by minimum rating
- Review text display
- User and date information

#### **3. Data Analysis**
- Dataset statistics and metrics
- Column information and data types
- Missing values analysis
- Data preview functionality

#### **4. User Experience**
- Responsive sidebar navigation
- Real-time search and filtering
- Expandable/collapsible sections
- Clean, intuitive interface

### 🔧 Development Process

#### **Phase 1: Setup & Foundation**
- Environment setup with virtual environment
- Streamlit application structure
- Basic data loading and display

#### **Phase 2: Core Features**
- Recipe browsing interface
- Review system implementation
- Data analysis tools

#### **Phase 3: Enhancement**
- Multi-language support system
- Improved UI/UX design
- Advanced filtering and search
- Project documentation

### 📈 Data Source & Structure

**Dataset:** [Food.com Recipes and User Interactions](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions)

#### **Main Files:**
- `RAW_recipes.csv` - Human-readable recipe data
- `RAW_interactions.csv` - User reviews and ratings
- `PP_recipes.csv` - Preprocessed data for ML
- `PP_users.csv` - Preprocessed user data

#### **Key Columns in RAW_recipes.csv:**
- `name` - Recipe title
- `ingredients` - List of ingredients
- `steps` - Cooking instructions
- `nutrition` - Nutritional values
- `minutes` - Cooking time
- `tags` - Recipe categories

### 🎯 Future Enhancements

#### **Planned Features:**
- Advanced data visualizations with Plotly
- Recipe recommendation system
- User favorite recipes
- Export functionality
- Advanced search filters
- Recipe images integration

#### **Technical Improvements:**
- Database integration (SQLite/PostgreSQL)
- Caching optimization for large datasets
- User authentication system
- REST API development

### 👥 Development Team

This project was developed as a demonstration of:
- Full-stack web application development with Python
- Data science and analysis capabilities
- Multi-language internationalization
- User-centered design principles

### 📝 License & Attribution

- **Dataset**: Food.com via Kaggle
- **Application**: Open source for educational purposes
- **Technologies**: Streamlit, Pandas, Python

---

*Last Updated: September 2024*
""",

        "sk": """
## 🚀 Prehľad projektu

**Food.com Recipes Explorer** je komplexná webová aplikácia vytvorená na preskúmanie a analýzu datasetu Food.com, ktorý obsahuje viac ako 230 000 receptov a 1 milión používateľských recenzií.

### 🛠️ Technická implementácia

#### **Frontend & Framework:**
- **Streamlit** - Python webový framework pre tvorbu interaktívnych webových aplikácií
- **Pandas** - Manipulácia a analýza dát
- **Plotly** - Interaktívne vizualizácie (pripravené pre budúce grafy)

#### **Backend & Spracovanie dát:**
- **Python 3.9+** - Hlavný programovací jazyk
- **Pandas** - Parsovanie CSV a transformácia dát
- **Pathlib** - Operácie so súborovým systémom

#### **Architektúra:**