import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh 
import plost
import subprocess
from threading import Thread


cpuUsage = pd.DataFrame()
processList = pd.DataFrame()
memoryUsage = pd.DataFrame()
memory = pd.DataFrame()
idleCpu = pd.DataFrame()
threadsTotal = pd.DataFrame()

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

threadProcessList = Thread(target=updateData)
threadProcessList.start()
threadProcessList.join()

st_autorefresh(interval=2*1000, key='dataframerefresh')
# Row A
st.markdown('### Dashboard do Sistema Operacional')
col1, col2, col3, col4 = st.columns(4)
col1.metric("Uso da CPU", cpuUsage.columns[1])
col1.metric("Tempo médio de ociosidade", str(round(float(idleCpu.columns[2]),1)) + "%")
col2.metric("Uso de Memória", str(round(((int(memoryUsage.iloc[0][1])/int(memoryUsage.columns[1]))*100),1)) + "%")
col2.metric("Memória Livre", str(100 - round(((int(memoryUsage.iloc[0][1])/int(memoryUsage.columns[1]))*100),1)) + "%")
col3.metric("Memória Física", str(int(memory.iloc[0][1])/1000) + "Mb")
col3.metric("Memória Virtual", str(int(memory.iloc[1][1])/1000) + "Mb")
col4.metric("Número de Processos", str(len(processList)))
col4.metric("Número de Threads", str(threadsTotal.columns[0]))

st.dataframe(processList)
print(processList.columns)

result = st.button("Abrir processo")
if result:
    result = not st.button("Fechar processo")
    # Row B
    #seattle_weather = pd.read_csv('../operational-system-dashboard/shellResponse/memoryUsage.csv')
    stocks = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/stocks_toy.csv')

    c1, c2 = st.columns((7,3))
    with c2:
        st.markdown('### Donut chart')
        plost.donut_chart(
            data=stocks,
            theta=donut_theta,
            color='company',
            legend='bottom', 
            use_container_width=True)

    # Row C
    st.markdown('### Line chart')
    st.line_chart(seattle_weather, x = 'date', y = plot_data, height = plot_height)
