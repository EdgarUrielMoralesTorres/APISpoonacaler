from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'osagechandequemybeloved'

API_URL = "https://api.spoonacular.com/recipes/complexSearch"
API_KEY = "b667497123be42b18ef2cdc139b872b2"   


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search_recipe():

    nombre_receta = request.form.get('nombre_receta', '').strip()

    if not nombre_receta:
        flash("Ingresa el nombre del alimento o la receta", "error")
        return redirect(url_for('index'))

    params = {
        "query": nombre_receta,
        "number": 1,
        "addRecipeInformation": True,
        "apiKey": API_KEY
    }

    try:
        respuesta = requests.get(API_URL, params=params)

        if respuesta.status_code == 200:
            data = respuesta.json()

            if data["totalResults"] == 0:
                flash(f'No se encontró "{nombre_receta}"', 'error')
                return redirect(url_for('index'))

            receta = data["results"][0]  

            recipe_info = {
                "titulo": receta["title"],
                "imagen": receta["image"],
                "resumen": receta["summary"],
                "comple": receta["sourceUrl"],
                "tiempo": receta.get("readyInMinutes", "N/A"),
                "porciones": receta.get("servings", "N/A")
            }

            return render_template("resultado.html", receta=recipe_info)

        else:
            flash("Error cona la api", "error")
            return redirect(url_for("index"))

    except requests.exceptions.RequestException:
        flash("Error al buscar la receta", "error")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
