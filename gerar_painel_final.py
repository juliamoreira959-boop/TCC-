import os
import pyvista as pv
import meshio

# --- CONFIGURAÇÃO ---
ARQUIVO_FEM_INP = "FEMMeshGmsh_mod.inp"         
ARQUIVO_VIB_HTML = "placa_vibracoes_3d.html"     
# --------------------

def gerar_painel():
    if not os.path.exists(ARQUIVO_FEM_INP):
        print(f"❌ ERRO: O arquivo '{ARQUIVO_FEM_INP}' não foi encontrado.")
        return

    print("⏳ Lendo e convertendo a malha estrutural para modelo sólido...")
    try:
        dados_inp = meshio.read(ARQUIVO_FEM_INP)
        mesh_bruta = pv.from_meshio(dados_inp)
        
        # 🌟 FORÇA A MALHA A VIRAR UMA SUPERFÍCIE SÓLIDA PREENCHIDA (TIRA O EFEITO TRANSPARENTE)
        mesh_fem = mesh_bruta.extract_surface()
    except Exception as e:
        print(f"❌ Erro ao ler o arquivo .inp: {e}")
        return

    # Gera o arquivo HTML com preenchimento sólido e cores nítidas
    nome_fem_html = "placa_deformacoes_3d.html"
    pl = pv.Plotter(off_screen=True)
    pl.background_color = "#111827"  
    
    pl.add_mesh(
        mesh_fem, 
        scalars=mesh_fem.points[:, 2],  
        cmap="turbo",         
        style="surface",      # 🌟 Força o preenchimento sólido das faces
        show_edges=True, 
        edge_color="#0b0f19", # Cor de borda escura para dar profundidade
        line_width=1.5,       # 🌟 Aumenta a espessura das linhas para dar nitidez
        lighting=False,       
        scalar_bar_args={
            "title": "Deslocamento (mm)", 
            "color": "white",
            "position_x": 0.85,
            "position_y": 0.15
        } 
    )
    pl.show_axes()
    pl.export_html(nome_fem_html)
    print(f"✅ Arquivo individual de deformações gerado: {nome_fem_html}")

    print("🌐 Criando a interface unificada atualizada...")
    html_painel = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Gêmeo Digital - TCC</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; 
            margin: 0; 
            padding: 0; 
            background-color: #0b0f19; 
            color: #e5e7eb; 
            height: 100vh; 
            display: flex; 
            flex-direction: column; 
            overflow: hidden;
        }}
        
        header {{ 
            background: linear-gradient(135deg, #0f172a, #1e293b);
            border-bottom: 1px solid #334155;
            color: white; 
            padding: 18px 25px; 
            text-align: center; 
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }}
        header h1 {{ margin: 0; font-size: 24px; letter-spacing: 1.5px; font-weight: 700; color: #38bdf8; }}
        header p {{ margin: 6px 0 0 0; font-size: 13px; color: #94a3b8; }}
        
        .container {{ 
            display: flex; 
            flex: 1; 
            max-width: 100%; 
            margin: 20px; 
            gap: 20px; 
            box-sizing: border-box; 
            height: calc(100vh - 130px);
        }}
        
        .sidebar {{ 
            width: 340px; 
            background: #111827; 
            padding: 22px; 
            border-radius: 12px; 
            border: 1px solid #1f2937;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3);
            display: flex; 
            flex-direction: column; 
            gap: 15px; 
            box-sizing: border-box;
            overflow-y: auto;
        }}
        
        .sidebar::-webkit-scrollbar {{ width: 6px; }}
        .sidebar::-webkit-scrollbar-thumb {{ background: #374151; border-radius: 4px; }}
        
        .sidebar h2 {{ 
            font-size: 13px; 
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin: 10px 0 5px 0; 
            color: #94a3b8; 
            border-bottom: 1px solid #374151; 
            padding-bottom: 6px; 
        }}
        
        .viewer-box {{ 
            flex: 1; 
            background: #111827; 
            padding: 20px; 
            border-radius: 12px; 
            border: 1px solid #1f2937;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3);
            display: flex; 
            flex-direction: column; 
            box-sizing: border-box; 
        }}
        
        .btn {{ 
            display: block; 
            width: 100%; 
            padding: 14px; 
            background-color: #1f2937; 
            color: #9ca3af; 
            border: 1px solid #374151; 
            border-radius: 8px; 
            cursor: pointer; 
            text-align: left; 
            font-size: 13px; 
            font-weight: 600; 
            transition: all 0.2s ease; 
        }}
        .btn:hover {{ background-color: #374151; color: white; }}
        .btn.active {{ 
            background-color: #0284c7; 
            color: white; 
            border-color: #38bdf8;
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
        }}
        
        .sensor-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
        
        .sensor-card {{ 
            background: #1f2937; 
            padding: 12px; 
            border-radius: 8px; 
            border-left: 4px solid #4b5563; 
            font-size: 13px; 
            color: #d1d5db;
        }}
        .sensor-card strong {{ color: #94a3b8; font-size: 10px; text-transform: uppercase; display: block; margin-bottom: 3px; }}
        .sensor-card.active {{ 
            border-left-color: #10b981; 
            background: rgba(16, 185, 129, 0.05);
            color: #34d399;
        }}
        
        .fft-list {{
            background: #1f2937;
            padding: 12px 15px;
            border-radius: 8px;
            font-size: 13px;
            font-family: monospace;
            color: #38bdf8;
            line-height: 1.8;
            border: 1px solid #374151;
        }}
        
        .iframe-wrapper {{ flex: 1; width: 100%; border: none; margin-top: 15px; position: relative; border-radius: 8px; overflow: hidden; background: #111827; }}
        iframe {{ width: 100%; height: 100%; border: none; display: none; }}
        iframe.visible {{ display: block; }}
        
        footer {{ text-align: center; padding: 12px; color: #64748b; font-size: 12px; background: #0f172a; border-top: 1px solid #1e293b; }}
    </style>
</head>
<body>

    <header>
        <h1>GÊMEO DIGITAL | TCC</h1>
        <p>Análise Avançada FEM (Método de Elementos Finitos) & Monitoramento Dinâmico</p>
    </header>

    <div class="container">
        <div class="sidebar">
            <h2>Navegação Estrutural</h2>
            <button class="btn active" id="btn-fem" onclick="alternarVisao('fem')">📊 Deformações Globais (DISP)</button>
            <button class="btn" id="btn-vib" onclick="alternarVisao('vib')">🌀 Zonas de Vibração Crítica</button>

            <h2>Leitura de Sensores (SHM)</h2>
            <div class="sensor-grid">
                <div class="sensor-card"><strong>Tempo Coleta</strong>-- s</div>
                <div class="sensor-card active"><strong>Status Estrutura</strong>Conectando...</div>
            </div>
            <div class="sensor-card"><strong>Aceleração X</strong>-- g</div>
            <div class="sensor-card"><strong>Aceleração Y</strong>-- g</div>
            <div class="sensor-card"><strong>Aceleração Z</strong>-- g</div>
            <div class="sensor-card"><strong>Metodologia</strong>FEM (Linear)</div>

            <h2>Espectro de Frequência (FFT)</h2>
            <div class="fft-list">
                
            </div>
        </div>

        <div class="viewer-box">
            <h3 id="txt-titulo" style="margin: 0 0 4px 0; font-size: 18px; color: white; font-weight: 600;">Visualização Atual: Deformações Globais (DISP)</h3>
            <p style="font-size:12px; color:#64748b; margin: 0;">🖱 Use o mouse para rotacionar livremente a casca</p>
            
            <div class="iframe-wrapper">
                <iframe id="iframe-fem" class="visible" src="{nome_fem_html}"></iframe>
                <iframe id="iframe-vib" src="{ARQUIVO_VIB_HTML}"></iframe>
            </div>
        </div>
    </div>

    <footer>
        © 2026 Gêmeo Digital de Infraestruturas Civis Complexas. Desenvolvido com CalculiX, PyVista e Web3D.
    </footer>

    <script>
        function alternarVisao(tipo) {{
            const iframeFem = document.getElementById('iframe-fem');
            const iframeVib = document.getElementById('iframe-vib');
            const btnFem = document.getElementById('btn-fem');
            const btnVib = document.getElementById('btn-vib');
            const txtTitulo = document.getElementById('txt-titulo');

            if (tipo === 'fem') {{
                iframeFem.classList.add('visible');
                iframeVib.classList.remove('visible');
                btnFem.classList.add('active');
                btnVib.classList.remove('active');
                txtTitulo.innerText = "Visualização Atual: Deformações Globais (DISP)";
            }} else {{
                iframeFem.classList.remove('visible');
                iframeVib.classList.add('visible');
                btnFem.classList.remove('active');
                btnVib.classList.add('active');
                txtTitulo.innerText = "Visualização Atual: Zonas de Vibração Crítica";
            }}
        }}
    </script>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_painel)
    print("✅ COMPILADO! Modelo transformado em sólido com sucesso.")

if __name__ == "__main__":
    gerar_painel() # <-- Nome corrigido para casar com a função!
