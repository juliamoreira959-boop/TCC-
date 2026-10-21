import os
import pyvista as pv
import meshio

# --- CONFIGURAÇÃO ---
# Se o seu arquivo principal for o "FEMMeshGmsh.inp", basta mudar o nome na linha abaixo
ARQUIVO_ENTRADA = "FEMMeshGmsh_mod.inp"  
# --------------------

def criar_modelo_vibracoes():
    # Usamos uma variável local para evitar o erro de declaração global do Python
    arquivo = ARQUIVO_ENTRADA
    
    if not os.path.exists(arquivo):
        if os.path.exists("FEMMeshGmsh_mod.inp"):
            arquivo = "FEMMeshGmsh_mod.inp"
        else:
            print(f"❌ ERRO: Arquivo .inp não encontrado na pasta.")
            return

    print(f"⏳ Lendo a malha estrutural de '{arquivo}' via meshio...")
    
    try:
        # O meshio lê os nós e elementos nativos do arquivo .inp
        mesh_dados = meshio.read(arquivo)
        
        # Converte diretamente para a malha tridimensional do PyVista
        mesh = pv.from_meshio(mesh_dados)
    except Exception as e:
        print(f"❌ Erro na conversão da malha: {e}")
        return
        
    pl = pv.Plotter()
    pl.background_color = "#fdfdfd"
    
    print("🎨 Renderizando o modelo tridimensional completo para o TCC...")
    
    pl.add_mesh(
        mesh, 
        color="#b0b0b0",
        show_edges=True, 
        edge_color="#111111",     
        line_width=0.5,             
        opacity=0.95,		      
        ambient=0.45,                 
        diffuse=0.65,                
        specular=0.25,
        specular_power=20
    )
    
    pl.show_axes()
    pl.enable_trackball_style()
    
    nome_site = "placa_vibracoes_3d.html"
    print(f"💾 Exportando modelo dinâmico para: {nome_site}...")
    pl.export_html(nome_site)
    print("✅ CONCLUÍDO! Arquivo 3D interativo gerado com sucesso!")
    
    print("🖥️ Abrindo visualizador interativo...")
    pl.show()

if __name__ == "__main__":
    criar_modelo_vibracoes()
