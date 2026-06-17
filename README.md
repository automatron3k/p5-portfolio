# p5-portfolio

Mis sketches de p5.js (The Coding Train + The Nature of Code), versionados y
publicados en <https://javierlaborde.com/p5js/>.

## Estructura

```
libs/p5.min.js          p5 local compartido (offline, sin CDN)
template/               sketch starter para copiar
sketches/<proyecto>/<nombre>/
    index.html          carga ../../../libs/p5.min.js + sketch.js
    sketch.js           tu código
    meta.json           título, fecha, tags, source
index.html              galería (lee manifest.json)
build.py                escanea sketches/ -> manifest.json
deploy/                 docker-compose + Caddy snippet para la VM
```

## Nuevo sketch

```bash
cp -r template sketches/thecodingtrain/mi-sketch
# pega tu código en sketches/thecodingtrain/mi-sketch/sketch.js
# edita meta.json
python3 build.py
git add . && git commit -m "Add mi-sketch" && git push
```

El push dispara el deploy automático a la VM.

## Correr local

```bash
python3 -m http.server 8000
# abre http://localhost:8000/  (galería)
# o un sketch:  http://localhost:8000/sketches/thecodingtrain/mi-sketch/
```

## Deploy (one-time setup en la VM)

Ver `deploy/`. Resumen:

1. `git clone <repo> /opt/p5js` en la VM.
2. `docker compose -f /opt/p5js/deploy/docker-compose.yml up -d`
3. Aplicar `deploy/Caddyfile.snippet` al Caddyfile y recargar Caddy.
4. En GitHub: secrets `VM_HOST`, `VM_USER`, `VM_SSH_KEY` para el deploy auto.
