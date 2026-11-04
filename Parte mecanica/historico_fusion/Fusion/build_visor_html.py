import os

def generate_html():
    if os.path.exists("/mnt/c/Users/Usuario/Desktop/universidad/clase/TFG/DESARROLLO_TFG/Fusion"):
        base_dir = "/mnt/c/Users/Usuario/Desktop/universidad/clase/TFG/DESARROLLO_TFG/Fusion"
    else:
        base_dir = r"C:\Users\Usuario\Desktop\universidad\clase\TFG\DESARROLLO_TFG\Fusion"
    obj_path = os.path.join(base_dir, "Marco_Real_2020_TFG.obj")
    html_path = os.path.join(base_dir, "visor_3d_fusion.html")

    print(f"Leyendo malla OBJ ({obj_path})...")
    with open(obj_path, 'r', encoding='utf-8') as f:
        obj_content = f.read()

    html_template = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bastidor Real 1:1 - Perfiles 2020 T-Slot y Escuadras de Fundición</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: #16181d;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #ecf0f1;
        }}
        #canvas-container {{
            width: 100vw;
            height: 100vh;
            display: block;
        }}
        #ui-panel {{
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(22, 25, 30, 0.94);
            border: 1px solid #34495e;
            border-radius: 8px;
            padding: 18px 22px;
            box-shadow: 0 4px 25px rgba(0, 0, 0, 0.6);
            max-width: 440px;
            backdrop-filter: blur(10px);
            z-index: 10;
        }}
        h1 {{
            font-size: 15px;
            margin: 0 0 8px 0;
            color: #3498db;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        p {{
            font-size: 13px;
            margin: 4px 0;
            line-height: 1.4;
            color: #bdc3c7;
        }}
        .metric-badge {{
            display: inline-block;
            background: #2c3e50;
            border: 1px solid #4a627a;
            border-radius: 4px;
            padding: 3px 8px;
            font-size: 11px;
            font-weight: bold;
            color: #1abc9c;
            margin: 3px 2px;
        }}
        .badge-warning {{
            background: #7d3c00;
            border-color: #e67e22;
            color: #f39c12;
        }}
        .btn-group {{
            margin-top: 14px;
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
        }}
        button {{
            background: #2980b9;
            color: white;
            border: none;
            padding: 7px 14px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 500;
            transition: all 0.2s;
        }}
        button:hover {{
            background: #3498db;
        }}
        #legend {{
            position: absolute;
            bottom: 20px;
            left: 20px;
            background: rgba(22, 25, 30, 0.94);
            border: 1px solid #34495e;
            border-radius: 6px;
            padding: 12px 16px;
            font-size: 12px;
            z-index: 10;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 5px 0;
        }}
        .color-dot {{
            width: 14px;
            height: 14px;
            border-radius: 3px;
        }}
        #loading {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 16px;
            color: #3498db;
            background: rgba(0,0,0,0.85);
            padding: 16px 28px;
            border-radius: 8px;
            border: 1px solid #34495e;
            z-index: 100;
        }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/OBJLoader.js"></script>
</head>
<body>
    <div id="loading">Cargando B-Rep 1:1 de OpenCASCADE...</div>
    <div id="canvas-container"></div>

    <div id="ui-panel">
        <h1>📐 Bastidor Real 1:1 Fotorrealista</h1>
        <p>Reconstrucción paramétrica exacta según las fotos macro y medidas de taller (28/10/26):</p>
        <div>
            <span class="metric-badge">Perfil: 2020 T-Slot Ranura 6 (45° chaflán exterior)</span>
            <span class="metric-badge">Núcleo M5: Taladro circular de 4.2 mm</span>
            <span class="metric-badge">Escuadras: Fundición 90° con 2 nervios y vaciado 14 mm</span>
            <span class="metric-badge">Columnas: 500 mm (Ancho total 540 mm)</span>
            <span class="metric-badge">Luz interior útil: 500 x 420 mm</span>
            <span class="metric-badge badge-warning">Tornillos: M5 alomados con arandela (refleja tornillos faltantes)</span>
        </div>
        <p style="margin-top: 10px; font-size: 12px; color: #95a5a6;">
            Rotar: clic izq | Mover: clic der | Zoom: rueda del ratón
        </p>
        <div class="btn-group">
            <button onclick="setCameraView('iso')">Isométrica</button>
            <button onclick="setCameraView('corner')">Detalle Esquina</button>
            <button onclick="setCameraView('front')">Frontal</button>
            <button onclick="setCameraView('top')">Cenital</button>
            <button onclick="toggleWireframe()">Malla Alámbrica</button>
        </div>
    </div>

    <div id="legend">
        <div style="font-weight: bold; margin-bottom: 6px; color: #3498db;">Componentes Físicos</div>
        <div class="legend-item"><div class="color-dot" style="background: #d8d8d8; border: 1px solid #999;"></div> Perfil 2020 T-Slot Anodizado</div>
        <div class="legend-item"><div class="color-dot" style="background: #888888; border: 1px solid #555;"></div> Escuadra 90° de Fundición de Aluminio</div>
        <div class="legend-item"><div class="color-dot" style="background: #ffffff; border: 1px solid #333; box-shadow: 0 0 5px #fff;"></div> Tornillos M5 Alomados con Arandela</div>
        <div class="legend-item"><div class="color-dot" style="background: #e67e22; border: 1px solid #d35400;"></div> Orificio libre (Tornillo faltante en taller)</div>
    </div>

    <!-- Geometría CAD B-Rep exportada directamente desde OpenCASCADE -->
    <script type="text/plain" id="cad-obj-data">
{obj_content}
    </script>

    <script>
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x16181d);
        scene.fog = new THREE.FogExp2(0x16181d, 0.0004);

        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 4000);
        camera.position.set(0, 250, 950);

        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        container.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.target.set(0, 250, 0);

        // Iluminación de estudio para realzar ranuras y chaflanes
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
        scene.add(ambientLight);

        const dirLight = new THREE.DirectionalLight(0xffffff, 0.9);
        dirLight.position.set(400, 800, 600);
        dirLight.castShadow = true;
        dirLight.shadow.mapSize.width = 2048;
        dirLight.shadow.mapSize.height = 2048;
        scene.add(dirLight);

        const fillLight = new THREE.DirectionalLight(0x74b9ff, 0.4);
        fillLight.position.set(-500, 300, -400);
        scene.add(fillLight);

        const bottomLight = new THREE.DirectionalLight(0xffeedd, 0.3);
        bottomLight.position.set(0, -300, 200);
        scene.add(bottomLight);

        // Rejilla de suelo de taller
        const grid = new THREE.GridHelper(1000, 20, 0x34495e, 0x222a33);
        grid.position.y = 0;
        scene.add(grid);

        let cadMesh = null;
        let isWireframe = false;

        const matAlum = new THREE.MeshStandardMaterial({{
            color: 0xd8d8d8,
            metalness: 0.85,
            roughness: 0.25,
            polygonOffset: true,
            polygonOffsetFactor: 1,
            polygonOffsetUnits: 1
        }});

        const objText = document.getElementById('cad-obj-data').textContent;
        const loader = new THREE.OBJLoader();
        const obj = loader.parse(objText);

        obj.traverse((child) => {{
            if (child.isMesh) {{
                child.material = matAlum;
                child.castShadow = true;
                child.receiveShadow = true;
            }}
        }});

        cadMesh = obj;
        scene.add(cadMesh);
        document.getElementById('loading').style.display = 'none';

        // Acotaciones 3D
        function addDimension(p1, p2, color) {{
            const geom = new THREE.BufferGeometry().setFromPoints([p1, p2]);
            const mat = new THREE.LineBasicMaterial({{ color: color || 0x3498db, linewidth: 2 }});
            scene.add(new THREE.Line(geom, mat));
        }}
        // Cota exterior 540 mm
        addDimension(new THREE.Vector3(-270, 520, 0), new THREE.Vector3(270, 520, 0), 0x3498db);
        // Cota interior 500 mm
        addDimension(new THREE.Vector3(-250, 250, 0), new THREE.Vector3(250, 250, 0), 0x2ecc71);
        // Cota altura 500 mm
        addDimension(new THREE.Vector3(290, 0, 0), new THREE.Vector3(290, 500, 0), 0xe67e22);

        function setCameraView(view) {{
            if (view === 'iso') {{
                camera.position.set(450, 450, 700);
                controls.target.set(0, 250, 0);
            }} else if (view === 'corner') {{
                // Enfoque a la escuadra superior izquierda para ver ranura, chaflán, nervios y tornillos
                camera.position.set(-200, 530, 80);
                controls.target.set(-240, 490, 0);
            }} else if (view === 'front') {{
                camera.position.set(0, 250, 950);
                controls.target.set(0, 250, 0);
            }} else if (view === 'top') {{
                camera.position.set(0, 950, 0);
                controls.target.set(0, 250, 0);
            }}
            controls.update();
        }}

        function toggleWireframe() {{
            isWireframe = !isWireframe;
            if (cadMesh) {{
                cadMesh.traverse((child) => {{
                    if (child.isMesh) {{
                        child.material.wireframe = isWireframe;
                    }}
                }});
            }}
        }}

        function animate() {{
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }}
        animate();

        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});
    </script>
</body>
</html>
'''
    with open(html_path, 'w', encoding='utf-8') as out:
        out.write(html_template)
    print(f"visor_3d_fusion.html generado con éxito ({os.path.getsize(html_path)} bytes)!")

if __name__ == "__main__":
    generate_html()
