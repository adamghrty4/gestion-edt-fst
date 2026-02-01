import json
import csv
from datetime import datetime


class Exportateur:

    @staticmethod
    def exporter(seances, path):
        data = []

        for s in seances:
            data.append({
                "cours": s.cours.nom,
                "type": s.cours.type_seance,
                "enseignant": str(s.enseignant),
                "groupe": s.groupe.nom,
                "salle": s.salle.nom if s.salle else None,
                "jour": s.creneau.jour,
                "debut": s.creneau.debut,
                "fin": s.creneau.fin
            })

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def exporter_csv(seances, path):
        headers = ["cours", "type", "enseignant", "groupe", "salle", "jour", "debut", "fin"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for s in seances:
                writer.writerow({
                    "cours": s.cours.nom,
                    "type": s.cours.type_seance,
                    "enseignant": str(s.enseignant),
                    "groupe": s.groupe.nom,
                    "salle": s.salle.nom if s.salle else "",
                    "jour": s.creneau.jour,
                    "debut": s.creneau.debut,
                    "fin": s.creneau.fin
                })

    @staticmethod
    def exporter_html(seances, path):
        data = []
        enseignants = set()
        groupes = set()
        salles = set()
        jours = set()
        types = set()
        for s in seances:
            entry = {
                "cours": s.cours.nom,
                "type": s.cours.type_seance,
                "enseignant": str(s.enseignant),
                "groupe": s.groupe.nom,
                "salle": s.salle.nom if s.salle else "",
                "jour": s.creneau.jour,
                "debut": s.creneau.debut,
                "fin": s.creneau.fin
            }
            data.append(entry)
            enseignants.add(entry["enseignant"])
            groupes.add(entry["groupe"])
            salles.add(entry["salle"])
            jours.add(entry["jour"])
            types.add(entry["type"])
        def opt_list(items):
            return "".join([f"<option value='{i}'>{i}</option>" for i in sorted([x for x in items if x])])
        
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        html = f"""<html><head><meta charset='utf-8'><title>EDT FST Tanger</title>
<style>
:root {{ --primary: #0056b3; --secondary: #f8f9fa; --accent: #ffc107; --text: #333; --border: #dee2e6; }}
body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 0; margin: 0; background: #f4f6f9; color: var(--text); }}
header {{ background: var(--primary); color: white; padding: 20px 40px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
h1 {{ margin: 0; font-size: 24px; font-weight: 600; }}
.meta {{ font-size: 14px; opacity: 0.9; margin-top: 5px; }}
.container {{ max-width: 1400px; margin: 20px auto; padding: 0 20px; }}
.card {{ background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); padding: 20px; margin-bottom: 20px; }}
.toolbar {{ display: flex; gap: 15px; flex-wrap: wrap; align-items: center; padding-bottom: 20px; border-bottom: 1px solid var(--border); margin-bottom: 20px; }}
select, input {{ padding: 10px 15px; border: 1px solid var(--border); border-radius: 6px; font-size: 14px; background: white; min-width: 150px; outline: none; transition: border-color 0.2s; }}
select:focus, input:focus {{ border-color: var(--primary); box-shadow: 0 0 0 3px rgba(0,86,179,0.1); }}
table {{ border-collapse: separate; border-spacing: 0; width: 100%; border-radius: 8px; overflow: hidden; border: 1px solid var(--border); }}
th, td {{ padding: 12px 16px; border-bottom: 1px solid var(--border); text-align: left; }}
th {{ background: #e9ecef; font-weight: 600; color: #495057; text-transform: uppercase; font-size: 12px; letter-spacing: 0.5px; }}
tr:last-child td {{ border-bottom: none; }}
tr:hover {{ background-color: rgba(0,86,179,0.02); }}
.badge {{ display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; }}
.badge-CM {{ background: #e3f2fd; color: #0d47a1; }}
.badge-TD {{ background: #fff3e0; color: #e65100; }}
.badge-TP {{ background: #e8f5e9; color: #1b5e20; }}
.actions {{ display: flex; gap: 10px; margin-top: 20px; justify-content: flex-end; }}
button, .btn {{ padding: 10px 20px; border: none; border-radius: 6px; cursor: pointer; font-weight: 500; transition: all 0.2s; text-decoration: none; display: inline-flex; align-items: center; font-size: 14px; }}
.btn-primary {{ background: var(--primary); color: white; }}
.btn-primary:hover {{ background: #004494; }}
.btn-secondary {{ background: white; border: 1px solid var(--border); color: var(--text); }}
.btn-secondary:hover {{ background: var(--secondary); }}
.btn-reset {{ color: #dc3545; background: #fff; border: 1px solid #dc3545; }}
.btn-reset:hover {{ background: #dc3545; color: white; }}
@media print {{
    body {{ background: white; }}
    .toolbar, .actions, .no-print {{ display: none !important; }}
    .card {{ box-shadow: none; padding: 0; }}
    table {{ border: 1px solid #ddd; }}
}}
</style>
</head>
<body>
<header>
    <h1>🎓 Université Abdelmalek Essaâdi - FST Tanger</h1>
    <div class='meta'>Système de Gestion des Emplois du Temps (Licence) | Mis à jour le {now}</div>
</header>
<div class='container'>
    <div class='card'>
        <div class='toolbar'>
            <select id='f_enseignant'><option value=''>👤 Tous les Enseignants</option>{opt_list(enseignants)}</select>
            <select id='f_groupe'><option value=''>🎓 Toutes les Filières</option>{opt_list(groupes)}</select>
            <select id='f_salle'><option value=''>🏫 Toutes les Salles</option>{opt_list(salles)}</select>
            <select id='f_jour'><option value=''>📅 Tous les Jours</option>{opt_list(jours)}</select>
            <select id='f_type'><option value=''>🏷️ Type</option>{opt_list(types)}</select>
            <input id='f_search' placeholder='🔍 Rechercher un cours...' style="flex-grow:1" />
            <button id='btn_reset' class="btn btn-reset">✖ Réinitialiser</button>
        </div>
        <table>
            <thead><tr><th>Cours</th><th>Type</th><th>Enseignant</th><th>Groupe</th><th>Salle</th><th>Jour</th><th>Début</th><th>Fin</th></tr></thead>
            <tbody id='tbody'></tbody>
        </table>
        <div class='actions'>
             <button onclick='location.reload()' class='btn btn-secondary'>🔄 Actualiser</button>
             <a href='edt_final.csv' class='btn btn-secondary' download>📥 Export CSV</a>
             <button onclick='window.print()' class='btn btn-primary'>🖨️ Imprimer / PDF</button>
        </div>
    </div>
</div>
<script>
const data={json.dumps(data, ensure_ascii=False)};
const tbody=document.getElementById('tbody');
const fE=document.getElementById('f_enseignant');
const fG=document.getElementById('f_groupe');
const fS=document.getElementById('f_salle');
const fJ=document.getElementById('f_jour');
const fT=document.getElementById('f_type');
const fQ=document.getElementById('f_search');

function render(){{
    tbody.innerHTML='';
    const q=(fQ.value||'').toLowerCase();
    const filtered = data.filter(d=>(!fE.value||d.enseignant===fE.value)&&(!fG.value||d.groupe===fG.value)&&(!fS.value||d.salle===fS.value)&&(!fJ.value||d.jour===fJ.value)&&(!fT.value||d.type===fT.value)&&(d.cours.toLowerCase().includes(q)||d.enseignant.toLowerCase().includes(q)));
    
    if(filtered.length === 0) {{
        tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;padding:30px;color:#888">Aucun cours trouvé pour ces critères.</td></tr>';
        return;
    }}

    filtered.forEach(d=>{{
        const tr=document.createElement('tr');
        const badgeClass = 'badge badge-' + d.type;
        tr.innerHTML=`<td><strong>${{d.cours}}</strong></td><td><span class='${{badgeClass}}'>${{d.type}}</span></td><td>${{d.enseignant}}</td><td><span class='badge' style='background:#eee'>${{d.groupe}}</span></td><td>${{d.salle}}</td><td>${{d.jour}}</td><td>${{d.debut}}</td><td>${{d.fin}}</td>`;
        tbody.appendChild(tr)
    }})
}}
[fE,fG,fS,fJ,fT,fQ].forEach(e=>e.onchange=e.oninput=render);
document.getElementById('btn_reset').onclick=()=>{{[fE,fG,fS,fJ,fT].forEach(x=>x.value='');fQ.value='';render()}};
render();
</script></body></html>"""
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
