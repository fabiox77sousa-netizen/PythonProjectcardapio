import streamlit as st
import urllib.parse

# Configurações de Estilo e Página
st.set_page_config(page_title="Top Burger - Cardápio", page_icon="🍔")

st.markdown("""
    <style>
    .main { background-color: #121212; color: white; }
    .stCheckbox { font-size: 18px; }
    .footer { text-align: center; color: #888; padding: 20px; }
    .price { color: #2ecc71; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔥 TOP BURGER")
st.subheader("Faça seu pedido online!")
st.write("---")

# --- AVISO PARA O CLIENTE ACHAR O CARRINHO ---
st.info("👈 **ATENÇÃO:** Para ver seu carrinho e finalizar o pedido, clique na setinha no canto superior esquerdo da tela!")

# --- TRUQUE PARA DEIXAR A SETINHA VERMELHA E PULSANDO ---
st.markdown(
    """
    <style>
    /* Muda a cor e o fundo da setinha de abrir o menu */
    [data-testid="collapsedControl"] {
        color: white !important;
        background-color: #ff4b4b !important;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(255, 75, 75, 0.5);
        animation: pulse 1.5s infinite;
    }
    
    /* Cria a animação de pulsar */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.15); }
        100% { transform: scale(1); }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- BANCO DE DADOS DO CARDÁPIO ---
lanches = {
    "Top Burguer": {"preco": 25.00,
                    "ingr": "Carne, calabresa, salsicha, bacon, presunto, ovo, queijo, salada e batata palha"},
    "X-Frango": {"preco": 18.00, "ingr": "Frango desfiado, queijo, alface, tomate, pepino e batata palha"},
    "X-Buguer": {"preco": 15.00, "ingr": "Carne, queijo, alface, tomate, pepino e batata palha"},
    "X-Eggs Bacon": {"preco": 20.00, "ingr": "Carne, ovo, queijo, bacon, alface, tomate, pepino e batata palha"},
    "X-Eggs": {"preco": 16.00, "ingr": "Carne, ovo, queijo, alface, tomate, pepino e batata palha"},
    "X-Bacon": {"preco": 19.00, "ingr": "Carne, queijo, bacon, alface, tomate, pepino e batata palha"},
    "X-Eggs Frango": {"preco": 20.00, "ingr": "Frango desfiado, ovo, queijo, alface, tomate, pepino e batata palha"},
    "X-Salada": {"preco": 16.00, "ingr": "Carne, presunto, queijo, alface, tomate, pepino e batata palha"},
    "X-Eggs Calabresa": {"preco": 20.00,
                         "ingr": "Carne, ovo, queijo, calabresa, alface, tomate, pepino e batata palha"},
    "X-Big-Dog": {"preco": 17.00, "ingr": "Carne, ovo, salsicha, queijo, alface, tomate, pepino e batata palha"},
    "X-Tudo": {"preco": 40.00,
               "ingr": "2 Pães, carne, calabresa, salsicha, bacon, presunto, ovo, frango, queijo, salada e batata palha"},
    "X-Calabresa": {"preco": 18.00, "ingr": "Carne, queijo, calabresa, alface, tomate, pepino e batata palha"},
    "X-Hot-Dog": {"preco": 12.00, "ingr": "Salsicha, queijo, alface, tomate, pepino e batata palha"},
}

bebidas = {
    "Suco Natural (300ml)": 6.00,
    "Coca Cola (600ml)": 10.00,
    "Coca Cola (1L)": 13.00,
    "Coca Cola (1,5L)": 15.00
}

# --- INTERFACE DE SELEÇÃO ---
carrinho = []
total = 0.0

st.header("🍔 Escolha seus Lanches")
for nome, info in lanches.items():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**{nome}**")
        st.caption(info['ingr'])
    with col2:
        qtd = st.number_input(f"R$ {info['preco']:.2f}", min_value=0, step=1, key=nome)
        if qtd > 0:
            carrinho.append(f"{qtd}x {nome}")
            total += info['preco'] * qtd
    st.write("---")

st.header("🥤 Bebidas")
for nome, preco in bebidas.items():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(nome)
    with col2:
        qtd_b = st.number_input(f"R$ {preco:.2f}", min_value=0, step=1, key=nome)
        if qtd_b > 0:
            carrinho.append(f"{qtd_b}x {nome}")
            total += preco * qtd_b

st.header("🎁 Adicional Grátis")
adicional = st.radio("Escolha um:", ["Nenhum", "Cheddar", "Purê de Batata", "Cebola Caramelizada"])

# --- RESUMO E WHATSAPP ---
st.sidebar.title("🛒 Seu Pedido")
if total > 0:
    st.sidebar.markdown("---")
    st.sidebar.subheader("🚚 Dados da Entrega")
    endereco = st.sidebar.text_area("Endereço completo (Rua, nº, Bairro, Referência):")
    
    forma_pagamento = st.sidebar.selectbox(
        "Forma de pagamento:", 
        ["Pix", "Cartão de Crédito", "Cartão de Débito", "Dinheiro"]
    )
    
    # --- NOVA LÓGICA DO TROCO ---
    troco_para = "" # Cria a variável vazia por padrão
    if forma_pagamento == "Dinheiro":
        troco_para = st.sidebar.text_input("Troco para quanto? (Deixe em branco se não precisar)")
    # ----------------------------

    st.sidebar.markdown("---")

    for item in carrinho:
        st.sidebar.write(item)
        
    if adicional != "Nenhum":
        st.sidebar.write(f"Adicional: {adicional}")
        
    st.sidebar.write("**Taxa de Entrega: R$ 4,00**")
    total_final = total + 4.0
    st.sidebar.subheader(f"Total: R$ {total_final:.2f}")

    # Montar Mensagem do WhatsApp
    msg = f"Olá! Gostaria de fazer um pedido:\n\n"
    msg += "\n".join(carrinho)

    if adicional != "Nenhum":
        msg += f"\nAdicional grátis: {adicional}"

    msg += f"\n\n📍 *Endereço:* {endereco if endereco else 'Não informado'}"
    msg += f"\n💳 *Pagamento:* {forma_pagamento}"
    
    # --- ADICIONA O TROCO NA MENSAGEM SÓ SE FOR DINHEIRO E TIVER PREENCHIDO ---
    if forma_pagamento == "Dinheiro" and troco_para:
        msg += f"\n💵 *Troco para:* R$ {troco_para}"
    
    msg += f"\n\nSubtotal: R$ {total:.2f}"
    msg += f"\nTaxa de entrega: R$ 4.00"
    msg += f"\n*Total a pagar: R$ {total_final:.2f}*"

    # --- PARTE FINAL CORRIGIDA E ALINHADA ---
    msg_codificada = urllib.parse.quote(msg)
    link_zap = f"https://wa.me/559183452301?text={msg_codificada}"

    st.sidebar.link_button("✅ FINALIZAR NO WHATSAPP", link_zap, use_container_width=True)

else:
    st.sidebar.warning("Seu carrinho está vazio. Escolha um lanche! 😋")


st.markdown("<br><hr><center>Top Burger - Santa Izabel-PA</center>", unsafe_allow_html=True)
