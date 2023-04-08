from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def create_db():
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS recipes (id INTEGER PRIMARY KEY, name TEXT, ingredients TEXT, instructions TEXT)')
    conn.commit()
    conn.close()

def get_all_recipes():
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM recipes')
    recipes = c.fetchall()
    conn.close()
    print(str(recipes) + "from get all recipes")
    return recipes

def add_recipe(name, ingredients, instructions):
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute('INSERT INTO recipes (name, ingredients, instructions) VALUES (?, ?, ?)', (name, ingredients, instructions))
    conn.commit()
    conn.close()

# @app.route('/delete', methods=['POST'])
# def delete():
#     conn = sqlite3.connect('recipes.db')
#     c = conn.cursor()
#     recipe_ids = request.form.getlist('recipe_ids')
#
#     if recipe_ids:
#         for recipe_id in recipe_ids:
#             conn.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
#             conn.commit()
#         flash('Selected recipes have been deleted!', 'success')
#     else:
#         flash('No recipes were selected!', 'warning')
#     conn.close()
#     return redirect('/')



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_recipe', methods=['GET', 'POST'])
def save_recipe():
    if request.method == 'POST':
        name = request.form['name']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        add_recipe(name, ingredients, instructions)
        return redirect('/')
    return render_template('save_recipe.html')

@app.route('/recipes')
def display_recipes():
    recipes = get_all_recipes()
    print(str(recipes) + "from display recipes func")
    return render_template('recipes.html', recipes=recipes)

if __name__ == '__main__':
    create_db()
    app.run(debug=True)
