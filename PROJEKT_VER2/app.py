from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from models import db, Project, calculate_materials
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Konfiguracja bazy danych
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            name = request.form.get("name")
            surface_area = float(request.form.get("surface_area"))
            tile_length = float(request.form.get("tile_length"))
            tile_width = float(request.form.get("tile_width"))
            sublayer_thickness = float(request.form.get("sublayer_thickness"))
            base_thickness = float(request.form.get("base_thickness"))
            sand_layer_thickness = float(request.form.get("sand_layer_thickness"))
            excavation_depth = float(request.form.get("excavation_depth"))
            joint_width = float(request.form.get("joint_width"))
            joint_depth = float(request.form.get("joint_depth"))
            border_length = float(request.form.get("border_length"))
            border_subs = float(request.form.get("border_subs"))
            border_earth = float(request.form.get("border_earth"))

            tiles, fugue, sublayer, base, sand, excavation = calculate_materials(
                surface_area, tile_length, tile_width, sublayer_thickness,
                base_thickness, sand_layer_thickness, excavation_depth,
                joint_width, joint_depth, border_length, border_subs, border_earth
            )

            new_project = Project(
                name=name,
                surface_area=surface_area,
                tile_length=tile_length,
                tile_width=tile_width,
                sublayer_thickness=sublayer_thickness,
                base_thickness=base_thickness,
                sand_layer_thickness=sand_layer_thickness,
                excavation_depth=excavation_depth,
                joint_width=joint_width,
                joint_depth=joint_depth,
                border_length=border_length,
                border_subs=border_subs,
                border_earth=border_earth,
                tiles=tiles,
                fugue=fugue,
                sublayer=sublayer,
                base=base,
                sand=sand,
                excavation=excavation
            )
            db.session.add(new_project)
            db.session.commit()
            flash('Projekt został dodany!', 'success')
        except ValueError as e:
            flash(f'Błąd danych: {e}', 'danger')
        except Exception as e:
            flash(f'Wystąpił błąd: {e}', 'danger')

    projects = Project.query.all()
    return render_template("index.html", projects=projects)

@app.route("/edit/<int:project_id>", methods=["GET", "POST"])
def edit(project_id):
    project = Project.query.get_or_404(project_id)

    if request.method == "POST":
        project.name = request.form.get("name")
        project.surface_area = float(request.form.get("surface_area"))
        project.tile_length = float(request.form.get("tile_length"))
        project.tile_width = float(request.form.get("tile_width"))
        project.sublayer_thickness = float(request.form.get("sublayer_thickness"))
        project.base_thickness = float(request.form.get("base_thickness"))
        project.sand_layer_thickness = float(request.form.get("sand_layer_thickness"))
        project.excavation_depth = float(request.form.get("excavation_depth"))
        project.joint_width = float(request.form.get("joint_width"))
        project.joint_depth = float(request.form.get("joint_depth"))
        project.border_length = float(request.form.get("border_length"))
        project.border_subs = float(request.form.get("border_subs"))
        project.border_earth = float(request.form.get("border_earth"))

        project.tiles, project.fugue, project.sublayer, project.base, project.sand, project.excavation = calculate_materials(
            project.surface_area, project.tile_length, project.tile_width,
            project.sublayer_thickness, project.base_thickness,
            project.sand_layer_thickness, project.excavation_depth,
            project.joint_width, project.joint_depth, project.border_length,
            project.border_subs, project.border_earth
        )

        db.session.commit()
        flash('Projekt został zaktualizowany!', 'success')
        return redirect(url_for("index"))

    return render_template("edit.html", project=project)

@app.route("/delete/<int:project_id>", methods=["POST"])
def delete(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Projekt został usunięty!', 'success')
    return redirect(url_for("index"))

# Funkcja generująca PDF
def generate_pdf(project):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.drawString(100, height - 100, f"Projekt: {project.name}")
    p.drawString(100, height - 120, f"Powierzchnia: {project.surface_area} m²")
    p.drawString(100, height - 140, f"Długość Płytki: {project.tile_length} cm")
    p.drawString(100, height - 160, f"Szerokość Płytki: {project.tile_width} cm")
    p.drawString(100, height - 180, f"Grubość Podkładu: {project.sublayer_thickness} cm")
    p.drawString(100, height - 200, f"Grubość Podłoża: {project.base_thickness} cm")
    p.drawString(100, height - 220, f"Grubość Warstwy Piasku: {project.sand_layer_thickness} cm")
    p.drawString(100, height - 240, f"Głębokość Wykopu: {project.excavation_depth} cm")
    p.drawString(100, height - 260, f"Szerokość Fugi: {project.joint_width} cm")
    p.drawString(100, height - 280, f"Głębokość Fugi: {project.joint_depth} cm")
    p.drawString(100, height - 300, f"Długość Obrzeża: {project.border_length} m")
    p.drawString(100, height - 320, f"Podbudowa Obrzeża: {project.border_subs} cm")
    p.drawString(100, height - 340, f"Grubość Warstwy Ziemi: {project.border_earth} cm")

    p.drawString(100, height - 360, f"Ilość Płytek: {project.tiles} szt.")
    p.drawString(100, height - 380, f"Ilość Fugi: {project.fugue} kg")
    p.drawString(100, height - 400, f"Ilość Podkładu: {project.sublayer} m³")
    p.drawString(100, height - 420, f"Ilość Podłoża: {project.base} m³")
    p.drawString(100, height - 440, f"Ilość Piasku: {project.sand} m³")
    p.drawString(100, height - 460, f"Ilość Ziemi: {project.excavation} m³")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer.getvalue()

@app.route("/download_pdf/<int:project_id>")
def download_pdf(project_id):
    project = Project.query.get_or_404(project_id)
    pdf = generate_pdf(project)
    return send_file(io.BytesIO(pdf), as_attachment=True, download_name=f"{project.name}.pdf", mimetype='application/pdf')

if __name__ == "__main__":
    app.run(debug=True)