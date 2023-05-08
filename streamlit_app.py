import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh 
import plost
import subprocess
from threading import Thread
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

# Construção e build do dashboard usando Streamlit
# Requisição de dados feita por subprocess executando arquivos bash dentro da pasta shellScripts

st.set_page_config(
    layout='wide'
)

# Inicialização de dados
cpuUsage = pd.DataFrame()
processList = pd.DataFrame()
memoryUsage = pd.DataFrame()
memory = pd.DataFrame()
idleCpu = pd.DataFrame()
threadsTotal = pd.DataFrame()
threadsList = pd.DataFrame()

# Update de dados
def updateData ():
    global processList
    processList = getInfo('processList')
    global memoryUsage
    memoryUsage = getInfo('memoryUsage')
    global memory
    memory = getInfo('memory')
    global cpuUsage
    cpuUsage = getInfo('cpuUsage')
    global idleCpu
    idleCpu = getInfo("cpuIdle")
    global threadsTotal
    threadsTotal = getInfo("threadTotal")
    global threadsList
    threadsList = getInfo("threadsList")

# Componente de tabela interativa
# Retirado de : https://github.com/streamlit/example-app-interactive-table/blob/main/streamlit_app.py
def aggrid_interactive_table(df: pd.DataFrame):
    """Creates an st-aggrid interactive table based on a dataframe.
    Args:
        df (pd.DataFrame]): Source dataframe
    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )

    options.configure_side_bar()
    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme='streamlit',
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )

    return selection

# Função
def getInfo (bashFile):
    # Save shell file into txt
    file_ = open('./shellResponse/' + bashFile +'.txt', 'w+')
    out_file = open('./shellResponse/' + bashFile+'.csv', 'w')
    subprocess.call(['sh', './shellScripts/'+bashFile+'.sh'], stdout=file_)
    file_.close()
    # Convert txt result in csv separated by comma
    subprocess.run(['sed',"s/ \+/,/g",'./shellResponse/' + bashFile + '.txt'], stdout=out_file)
    # Read csv and return as a dataframe
    df = pd.read_csv('./shellResponse/'+bashFile+'.csv', sep=",", on_bad_lines='skip')
    return (df)

def getProcessInfo (pid):
    file_ = open('./shellResponse/threadList.txt', 'w+')
    subprocess.run(['ps -T -p', pid], stdout=out_file)
    out_file = open('./shellResponse/' + bashFile+'.csv', 'w')
    subprocess.run(['sed',"s/ \+/,/g",'./shellResponse/' + bashFile + '.txt'], stdout=out_file)

threadProcessList = Thread(target=updateData)
threadProcessList.start()
threadProcessList.join()

# Garante auto update
st_autorefresh(interval=2*1000, key='dataframerefresh')
# Row A
memoriaLivre = (memoryUsage.iloc[0][1])
memoriaEmUso = (memoryUsage.iloc[1][1])
st.markdown('### Visão Geral do Sistema')
col1, col2, col3,col4= st.columns(4)
col1.metric("Uso da CPU", cpuUsage.columns[1])
col1.metric("Tempo médio de ociosidade", str(round(float(idleCpu.columns[2]),1)) + "%")
col1.metric("Memória Física", str(int(memory.iloc[0][1])/1000) + "Mb")
col1.metric("Memória Virtual", str(int(memory.iloc[1][1])/1000) + "Mb")
col1.metric("Número de Processos", str(len(processList)))
col1.metric("Número de Threads", str(threadsTotal.columns[0]))

d = {'Type': ['used','free','shared','buff/cache','available'], "Value": [memory.iloc[0][2],memory.iloc[0][3],memory.iloc[0][4],memory.iloc[0][5],memory.iloc[0][6]]}
dfMemory = pd.DataFrame(data=d)
with col2.container():
    st.markdown("Uso de Memória")
    plost.donut_chart(
        data=dfMemory, color='Type', legend='bottom', theta='Value',
    )

threadsList = threadsList.drop(columns=["Unnamed: 0"])
col4.markdown("Lista de Threads")
col4.dataframe(threadsList)
col3.markdown("Lista de Processos")
col3.dataframe(processList)