import pandas as pd
import ast
from collections import Counter

print("Анализ тегов в данных...")

# Load data
df = pd.read_csv('data/RAW_recipes.csv', nrows=10000)
all_tags = []

print(f"Загружено {len(df)} рецептов")

# Extract all tags
for tags_str in df['tags'].dropna():
    try:
        if isinstance(tags_str, str):
            tags = ast.literal_eval(tags_str)
            all_tags.extend(tags)
    except:
        continue

print(f"Найдено {len(all_tags)} тегов всего")

# Count tags
tag_counts = Counter(all_tags)

print("\n=== ТОП-50 САМЫХ ПОПУЛЯРНЫХ ТЕГОВ ===")
for tag, count in tag_counts.most_common(50):
    print(f"{tag}: {count}")

# Find specific categories
print("\n=== КАТЕГОРИИ БЛЮД ===")
meal_tags = [tag for tag in tag_counts.keys() if any(word in tag for word in ['breakfast', 'lunch', 'dinner', 'dessert', 'appetizer', 'snack', 'drink', 'cocktail', 'side-dish'])]
for tag in sorted(meal_tags):
    print(f"{tag}: {tag_counts[tag]}")

print("\n=== КУХНИ МИРА ===")
cuisine_tags = [tag for tag in tag_counts.keys() if any(word in tag for word in ['mexican', 'italian', 'indian', 'thai', 'chinese', 'french', 'asian', 'american', 'mediterranean', 'spanish', 'japanese'])]
for tag in sorted(cuisine_tags):
    print(f"{tag}: {tag_counts[tag]}")

print("\n=== ДИЕТЫ И ЗДОРОВЬЕ ===")
diet_tags = [tag for tag in tag_counts.keys() if any(word in tag for word in ['vegetarian', 'vegan', 'healthy', 'low', 'diet', 'gluten', 'keto', 'diabetic'])]
for tag in sorted(diet_tags):
    print(f"{tag}: {tag_counts[tag]}")