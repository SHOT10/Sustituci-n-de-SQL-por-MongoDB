from pymongo import MongoClient

# Configuración de la conexión a MongoDB
# Cambia 'usuario', 'contraseña', 'localhost' y 'puerto' según tus credenciales.
MONGO_URL = "mongodb://usuario:contraseña@localhost:27017/"

db_client = None
try:
    db_client = MongoClient(MONGO_URL)
    db = db_client["recetas_db"]  # Base de datos
    recipes_collection = db["recipes"]  # Colección de recetas
    print("Connected to MongoDB successfully.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit()

# Funciones de la lógica de la aplicación
def add_recipe():
    try:
        name = input("Enter recipe name: ").strip()
        if not name:
            print("Recipe name cannot be empty.")
            return

        ingredients = input("Enter ingredients (comma-separated): ").strip()
        if not ingredients:
            print("Ingredients cannot be empty.")
            return

        steps = input("Enter steps (separated by periods): ").strip()
        if not steps:
            print("Steps cannot be empty.")
            return

        recipe = {
            "name": name,
            "ingredients": ingredients.split(","),
            "steps": steps.split(".")
        }

        recipes_collection.insert_one(recipe)
        print("Recipe added successfully.")
    except Exception as e:
        print(f"Error while adding recipe: {e}")

def update_recipe():
    try:
        name = input("Enter the name of the recipe to update: ").strip()
        if not name:
            print("Recipe name cannot be empty.")
            return

        recipe = recipes_collection.find_one({"name": name})
        if not recipe:
            print("Recipe not found.")
            return

        new_name = input("Enter new recipe name (leave blank to keep current): ").strip()
        new_ingredients = input("Enter new ingredients (leave blank to keep current): ").strip()
        new_steps = input("Enter new steps (leave blank to keep current): ").strip()

        updates = {}
        if new_name:
            updates["name"] = new_name
        if new_ingredients:
            updates["ingredients"] = new_ingredients.split(",")
        if new_steps:
            updates["steps"] = new_steps.split(".")

        if updates:
            recipes_collection.update_one({"name": name}, {"$set": updates})
            print("Recipe updated successfully.")
        else:
            print("No updates made.")
    except Exception as e:
        print(f"Error while updating recipe: {e}")

def delete_recipe():
    try:
        name = input("Enter the name of the recipe to delete: ").strip()
        if not name:
            print("Recipe name cannot be empty.")
            return

        result = recipes_collection.delete_one({"name": name})
        if result.deleted_count:
            print("Recipe deleted successfully.")
        else:
            print("Recipe not found.")
    except Exception as e:
        print(f"Error while deleting recipe: {e}")

def list_recipes():
    try:
        recipes = recipes_collection.find()
        if recipes.count():
            print("\nList of Recipes:")
            for recipe in recipes:
                print(f"- {recipe['name']}")
        else:
            print("No recipes found.")
    except Exception as e:
        print(f"Error while listing recipes: {e}")

def view_recipe():
    try:
        name = input("Enter the name of the recipe to view: ").strip()
        if not name:
            print("Recipe name cannot be empty.")
            return

        recipe = recipes_collection.find_one({"name": name})
        if not recipe:
            print("Recipe not found.")
            return

        print("\nIngredients:")
        print(", ".join(recipe["ingredients"]))
        print("\nSteps:")
        print(". ".join(recipe["steps"]))
    except Exception as e:
        print(f"Error while viewing recipe: {e}")

def main():
    while True:
        print("\nRecipe Book")
        print("1. Add New Recipe")
        print("2. Update Recipe")
        print("3. Delete Recipe")
        print("4. List Recipes")
        print("5. View Recipe")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            add_recipe()
        elif choice == '2':
            update_recipe()
        elif choice == '3':
            delete_recipe()
        elif choice == '4':
            list_recipes()
        elif choice == '5':
            view_recipe()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
