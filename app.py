
# Análise Estatística de Dados Textuais - NLP - Streamlit
# Autor: Felipe Toledo
# Para a disciplina de Tópicos em NLP, do curso de graduação em Ciência de Dados e Inteligência Artificial do IESB.

# Importando as bibliotecas necessárias

import streamlit as st

import re
import nltk

from collections import Counter
from itertools import islice

import matplotlib.pyplot as plt
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


# Baixar os stopwords
nltk.download('stopwords')

st.title("Análise Estatística de texto")

def read_pdf(file):
    import pdfplumber
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def read_docx(file):
    import docx2txt
    text = docx2txt.process(file)
    return text

uploaded_file = st.sidebar.file_uploader("Escolha um arquivo (.txt, .pdf, .docx)", type=['txt', 'pdf', 'docx'], accept_multiple_files=False)

text_disabled = uploaded_file is not None # Desabilita o campo de texto se um arquivo for carregado
text = st.sidebar.text_area('Ou, insira o texto:',  disabled=text_disabled, height=130)

if st.sidebar.button('Carregar texto',  disabled=text_disabled):
    if text == '':
        st.sidebar.write(f':red[Insira um texto válido!]')
    else:
        st.sidebar.write(f':green[Texto carregado com sucesso!]')

st.sidebar.divider()
st.sidebar.caption('🧑‍💻 Made by [**Felipe Toledo**](https://github.com/SnowsToledo)')

if uploaded_file is not None:
    # To read file as bytes:
    if uploaded_file.type == 'application/pdf':
        text = ''
        with st.spinner('Carregando arquivo...'):
            text = read_pdf(uploaded_file)
    elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        with st.spinner('Carregando arquivo...'):
            text = ''
            text = read_docx(uploaded_file)
    elif uploaded_file.type == 'text/plain':
        text = uploaded_file.read().decode("utf-8")


# Exibe mensagem se não houver texto definido
if not text:
    st.write('##### 👈 Faça upload ou digite um texto para começar!')
    st.stop()

if not text:
    st.stop()

def padronizar_texto(frase: str)-> str:
    """
    Transforma o texto para minúsculo para padronizar
    :param frase: frase a ser padronizada
    :return: frase padronizada
    """
    return frase.lower()

def remover_digitos(frase: str)-> str:
    """
    Remove os digitos por não ser importante para gente
    :param frase: frase para remover os digitos
    :return: frase sem os digitos
    """
    return re.sub(r'\d','', frase)

def remover_pontuacao(frase: str)-> str:
    """
    Remove a pontuação
    :param frase: frase para remover a pontuação
    :return: frase sem a pontuação
    """
    return re.sub(r'[^\w\s]','', frase)


def remover_espacos(frase: str)-> str:
    """
    Remove os espaços a mais e '\n'
    :param frase: frase para remover os espaços
    :return: frase sem os espaços
    """
    return re.sub(r'\s+', ' ', frase)

def tokenizar_palavras(frase: str)-> list:
    """
    Tokeniza as palavras
    :param frase: frase para tokenizar
    :return: lista de palavras
    """
    return re.findall('\w+', frase)

def remover_stopwords(tokens: list)-> list:
    """
    Remove as stopwords
    :param tokens: lista de tokens
    :return: lista de tokens sem stopwords
    """
    # 
    # nltk.download('stopwords')
    stopwords = nltk.corpus.stopwords.words('portuguese')
    return [item for item in tokens if (item not in stopwords) and (len(item) > 2)]

def filtrar_counter(tokens: list, num: int)-> list:
    """
    Filtra as palavras mais frequentes de um Counter
    :param count: Counter com as palavras e a contagem de cada palavra
    :param num: número de palavras mais frequentes a serem retornadas
    :return: lista de palavras mais frequentes
    """
    return Counter(tokens).most_common(num)

def separar_tokens_count(count: Counter)-> list:
    """
    Separa os tokens e a contagem de cada token em duas listas diferentes
    :param count: Counter com os tokens e a contagem de cada token
    :return: lista de tokens e lista de contagem
    """
    words_tokens = [palavra[0] for palavra in count]
    freq_tokens = [palavra[1] for palavra in count]
    return words_tokens, freq_tokens

def fazer_grafico_barras(count: Counter, title: str ="Contagem das palavras mais repetidas")-> None:
    """
    Fazer gráfico de barras
    :param count: Counter com os tokens e a contagem de cada token
    :param title: título do gráfico
    """
    words_tokens, freq_tokens = separar_tokens_count(count)

    fig=go.Figure(go.Bar(x=words_tokens,
                        y=freq_tokens, text=freq_tokens, textposition='outside'))
    fig.update_layout(
        autosize=False,
        width=1000,
        height=500,
        title_text=title)
    fig.update_xaxes(tickangle = -45)
    st.plotly_chart(fig)

def fazer_bigramas(tokens: list)-> list:
    """
    Fazer bigramas
    :param tokens: lista de tokens
    :return: lista de bigramas
    """
    return [*map(' '.join, zip(tokens, islice(tokens, 1, None)))]

def fazer_nuvem_palavras(tokens: list)-> None:
    """
    Fazer nuvem de palavras
    :param tokens: lista de tokens
    """
    # concatenar as palavras
    all_tokens = " ".join(s for s in tokens)

    wordcloud = WordCloud(background_color="#f5f5f5").generate(all_tokens)

    # mostrar a imagem final
    fig, ax = plt.subplots(figsize=(10,6))
    plt.axis("off")
    ax.imshow(wordcloud, interpolation='bilinear')
    plt.tight_layout()
    st.pyplot(fig)

def limpeza_transformacao(text: str)-> list:
    return remover_stopwords(tokenizar_palavras(remover_espacos(remover_pontuacao(padronizar_texto(remover_digitos(text))))))

def fazer_graficos(str_tokenized_sem_stopwords: list)-> None:
    """
    Fazer gráficos de barras e nuvem de palavras
    :param str_tokenized_sem_stopwords: lista de tokens sem stopwords
    :param title: título do gráfico
    """
    fazer_grafico_barras(filtrar_counter(str_tokenized_sem_stopwords, 20))
    fazer_grafico_barras(filtrar_counter(fazer_bigramas(str_tokenized_sem_stopwords), 5), "Bigramas mais repetidos")
    fazer_nuvem_palavras(str_tokenized_sem_stopwords)

text_clean = limpeza_transformacao(text)



st.write('### Resultado da Análise Estatística do Texto')

with st.container():
    col1, col2, col3 = st.columns(3, border=True, vertical_alignment="center")
    col1.metric("Palavras", len(text.split()))
    col2.metric("Caracteres", len(text))
    col3.metric("Vocabulário Único", len(set(text.split())))
    

with st.expander("📄 Ver conteúdo do arquivo"):
    # Cria duas colunas para exibição dos resultados
    col1, col2 = st.columns(2)

    # Exibição do Texto Original
    col1.text_area('Texto Original', text, height=300)

    # Exibição do Texto Limpo
    col2.text_area('Texto Processado', text_clean, height=300)

fazer_graficos(text_clean)