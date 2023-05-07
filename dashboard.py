import subprocess
import pandas as pd

# Return data as dataframe based on shell file name
def getInfo (bashFile):
    # Save shell file into txt
    file_ = open('./shellResponse/' + bashFile +'.txt', 'w+')
    out_file = open('./shellResponse/' + bashFile+'.csv', 'w')
    subprocess.call(['sh', './shellScripts/'+bashFile+'.sh'], stdout=file_)
    file_.close()
    # Convert txt result in csv separated by comma
    subprocess.run(['sed',"s/ \+/,/g",'./shellResponse/' + bashFile + '.txt'], stdout=out_file)
    # Read csv and return as a dataframe
    df = pd.read_csv('./shellResponse/'+bashFile+'.csv', sep=",", header=0, on_bad_lines='skip')
    return (df)

print(getInfo('memoryUsage'))

