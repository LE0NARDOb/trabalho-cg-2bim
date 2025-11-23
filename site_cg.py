import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Trabalho CG", layout="wide")

st.title("Trabalho de Computação Gráfica")
st.markdown("""
**Aluno:** [Seu Nome Aqui]
**Objetivo:** Aplicação de processamento de imagens.
""")

st.divider()

st.header("1. Entrada de Imagem")
arquivo = st.file_uploader("Escolha uma imagem (JPG, PNG, BMP)", type=["jpg", "jpeg", "png", "bmp"])

if arquivo is not None:
    img_original = Image.open(arquivo)
    
    largura_base_display = 600
    if img_original.width < 600:
        largura_base_display = img_original.width

    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(img_original, width=largura_base_display, caption="Imagem Original")
    with col2:
        st.info(f"Dimensões Originais: {img_original.width} x {img_original.height} pixels")

    st.divider()

    st.header("2. Redução da Imagem")
    
    fatores = [0.75, 0.50, 0.25]
    
    for fator in fatores:
        nova_w = int(img_original.width * fator)
        nova_h = int(img_original.height * fator)
        img_red = img_original.resize((nova_w, nova_h))
        
        largura_visual = int(largura_base_display * fator)
        
        st.write(f"**Redução {int(fator*100)}%** ({nova_w}x{nova_h})")
        st.image(img_red, width=largura_visual)

    st.divider()

    st.header("3. Conversão de Formato (WEBP)")
    
    buffer_webp = io.BytesIO()
    img_original.save(buffer_webp, format="WEBP")
    tamanho_webp = buffer_webp.tell()
    
    st.write(f"Tamanho do arquivo convertido: **{tamanho_webp} bytes** ({tamanho_webp/1024:.2f} KB)")
    
    st.download_button(
        label="📥 Baixar Imagem em WEBP",
        data=buffer_webp.getvalue(),
        file_name="imagem_convertida.webp",
        mime="image/webp"
    )

    st.divider()

    st.header("4. e 5. Operações Geométricas e de Cores")
    
    col_esp, col_cinza = st.columns(2)
    
    with col_esp:
        st.subheader("Espelhamento Vertical")
        img_espelhada = ImageOps.flip(img_original)
        st.image(img_espelhada, use_container_width=True)
        
    with col_cinza:
        st.subheader("Tons de Cinza")
        img_cinza = img_original.convert("L")
        st.image(img_cinza, use_container_width=True)

    st.divider()

    st.header("6. Histograma e Estatísticas")
    
    img_array = np.array(img_original)
    
    fig, ax = plt.subplots(figsize=(10, 4))
    stats_data = []
    
    if len(img_array.shape) == 3:
        cores_nome = ['Red', 'Green', 'Blue']
        cores_plot = ['r', 'g', 'b']
        
        for i, cor in enumerate(cores_nome):
            canal = img_array[:, :, i]
            
            stats_data.append({
                "Canal": cor,
                "Mínimo": int(np.min(canal)),
                "Máximo": int(np.max(canal)),
                "Média": f"{np.mean(canal):.2f}",
                "Mediana": int(np.median(canal)),
                "Desvio Padrão": f"{np.std(canal):.2f}"
            })
            
            ax.hist(canal.ravel(), bins=256, color=cores_plot[i], alpha=0.5, label=cor)
    else:
        ax.hist(img_array.ravel(), bins=256, color='gray', alpha=0.5)
        stats_data.append({"Canal": "Cinza", "Média": f"{np.mean(img_array):.2f}"})

    ax.set_title("Histograma RGB")
    ax.set_xlabel("Valor do Pixel")
    ax.set_ylabel("Frequência")
    ax.legend()
    
    col_graf, col_tab = st.columns([3, 2])
    with col_graf:
        st.pyplot(fig)
    with col_tab:
        st.write("### Estatísticas")
        st.dataframe(stats_data, hide_index=True)

    st.divider()

    st.header("7. Dados Técnicos da Imagem")
    
    modo = img_original.mode
    bits_pixel = 0
    n_canais = 0
    
    if modo == 'RGB':
        bits_pixel, n_canais = 24, 3
    elif modo == 'RGBA':
        bits_pixel, n_canais = 32, 4
    elif modo == 'L':
        bits_pixel, n_canais = 8, 1
        
    st.json({
        "Profundidade de Cor": f"{bits_pixel} bits ({int(bits_pixel/max(1, n_canais))} bits por canal)",
        "Número de Canais": n_canais,
        "Modo de Cor": modo,
        "Dimensões (LxA)": f"{img_original.width} x {img_original.height}",
        "Tamanho em Memória (Buffer)": f"{img_original.width * img_original.height * max(1, n_canais)} bytes"
    })

else:
    st.info("Faça o upload de uma imagem acima.")