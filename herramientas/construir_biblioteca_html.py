# -*- coding: utf-8 -*-
"""Genera biblioteca.html a partir de biblioteca.xlsx y /fichas.

Uso (desde la carpeta de la biblioteca):  python herramientas/construir_biblioteca_html.py
Necesita openpyxl (python -m pip install openpyxl). No usa internet.
"""
import datetime
import json
import os
import re
import sys

import openpyxl

RAIZ = os.getcwd()
XLSX = os.path.join(RAIZ, "biblioteca.xlsx")
PLANTILLA = os.path.join(RAIZ, "herramientas", "biblioteca_plantilla.html")
SALIDA = os.path.join(RAIZ, "biblioteca.html")
CAMBIOS = os.path.join(RAIZ, "herramientas", "cambios_estado.json")  # opcional: [{"id","de","a","fecha"}]


def seccion(md, titulo):
    m = re.search(r"^## " + re.escape(titulo) + r".*?\n(.*?)(?=^## |\Z)", md, re.S | re.M)
    return m.group(1).strip() if m else ""


def main():
    ws = openpyxl.load_workbook(XLSX, data_only=True)["biblioteca"]
    cab = [c.value for c in ws[1]]
    docs, avisos = [], []
    for fila in ws.iter_rows(min_row=2, values_only=True):
        d = dict(zip(cab, fila))
        if not d.get("id"):
            continue
        ruta = os.path.join(RAIZ, d["ficha"])
        if not os.path.exists(ruta):
            avisos.append("Falta la ficha de %s: %s" % (d["id"], d["ficha"]))
            continue
        md = open(ruta, encoding="utf-8").read()
        resumen = [l.strip() for l in seccion(md, "Resumen").split("\n") if l.strip()][:3]
        eventos = []
        for l in seccion(md, "Fechas clave").split("\n"):
            m = re.match(r"^-\s*(\d{4}-\d{2}(?:-\d{2})?)\s*:\s*(.+)$", l.strip())
            if m:
                eventos.append({"f": m.group(1), "t": m.group(2).strip()})
        docs.append({
            "id": d["id"], "tipo": d["tipo"], "ambito": d["ambito"], "organismo": d["organismo"],
            "titulo": d["titulo"], "fecha": str(d["fecha"]), "estado": d["estado"], "vinculante": d["vinculante"],
            "temas": [t.strip() for t in str(d["temas"]).split(";") if t.strip()],
            "resumen": resumen or [str(d["resumen"])], "archivo": d["archivo"], "ficha": d["ficha"],
            "url": d["url"], "fecha_consulta": str(d["fecha_consulta"]), "fecha_alta": str(d["fecha_alta"]),
            "notas": d.get("notas") or "", "eventos": eventos, "ficha_md": md,
        })
    cambios = json.load(open(CAMBIOS, encoding="utf-8")) if os.path.exists(CAMBIOS) else []
    datos = {"actualizado": datetime.date.today().isoformat(), "docs": docs, "cambios_estado": cambios}
    js = json.dumps(datos, ensure_ascii=False).replace("</", "<\\/").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    html = open(PLANTILLA, encoding="utf-8").read().replace("/*DATOS*/", js)
    open(SALIDA, "w", encoding="utf-8", newline="\n").write(html)
    print("biblioteca.html: %d documentos, %d fechas clave" % (len(docs), sum(len(x["eventos"]) for x in docs)))
    for a in avisos:
        print("AVISO:", a)
    return 1 if avisos else 0


if __name__ == "__main__":
    sys.exit(main())
