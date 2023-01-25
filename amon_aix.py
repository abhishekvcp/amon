
import pandas as pd
import re
import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import sys,os
import numpy as np
import seaborn as sns
sns.set_style("whitegrid")






if os.getcwd() not in sys.path : 
    sys.path.append(os.getcwd())

filename = input("\n\n\t\t Owner : Abhishek Panakkaran\n\t\t abhi_nmon2pdf:[nmon file name] : ")
file1 = open(filename, 'r')

day_str = str(datetime.date.today()) # always use date from datetime class 

legends = '.kehsihba'
marker = '@pcv'  
ticks_factor =' : kcabdeef'
facecolors = 'moc.gmail'

day_str = str(pd.datetime.now().date())
pdf_filename = day_str + '_abhi_nmon2pdf_report.pdf'
pdf_filename = filename + '.pdf'
#pp = PdfPages(pdf_filename)

#######################################################################################################################

list_figures = []

#######################################################################################################################

figa, ax = plt.subplots(figsize=(12,6))

ax = sns.boxplot(y=[x for x in range(1,15)])

ax.text(2, 2, "Report name : nmon insights Report\nOwner : Abhishek Panakkaran\nVersion : Beta \nSupport : as-is\n\nemail: abhishek.vcp@gmail.com\n", style ='italic', 
        fontsize = 30, color ="grey") 

ax.text(2, 2, "Nmon-file-insigts", style ='italic', 
        fontsize = 30, color ="grey") 

ax.set(xlim =(0, 16), ylim =(0, 12)) 
ax.set_title("nmon insights :  CPU, MEM, TOP Commands and Process ", 
             fontsize = 25, fontweight ='bold' , color = "green") 
ax.axis('off')

ax.axhline(11,color="green")
ax.annotate("note *data source is *.nmon file schedule like below \n /usr/bin/topas_nmon -F /var/nmon/lparname_23052022.nmon -t -s 900 -c 96 ",xy=(2,1)) # this is for displayinh in small text 


#figa.show()
#figa.savefig(pp, format='pdf')
list_figures.append(figa) # append the title figures list array
matplotlib.pyplot.close(fig=figa)


#######################################################################################################################

def abhi_convert_to_date(object1):
    temp_str = str(object1)
    format1 = "%d-%b-%Y %H:%M:%S"   #23-MAY-2022 00:15:33 https://www.geeksforgeeks.org/python-datetime-strptime-function/
    dt_object = datetime.datetime.strptime(temp_str, format1)
    return(dt_object)

#######################################################################################################################

def abhi_convert_to_float(object1):
    return(float(str(object1)))

#######################################################################################################################

def abhi_top_cpu_command_grapher():
    global list_figures
    global pdf_filename
    global confdf
    global topdf
    
    datatemp1 = topdf.groupby(by=["TDATATIME1"]).agg(total_cpu=("%CPU","sum") )
    datatemp1 = datatemp1.reset_index()

    datatemp2 = topdf.groupby(by=["TDATATIME1","Command"]).agg(total_cpu=("%CPU","sum"))
    datatemp2 = datatemp2.reset_index()
    datatemp2.sort_values(by="total_cpu",ascending=False,inplace=True)



    virtualprocessors_x100 = int(confdf.loc["conf","cpu_virtual"] * 100)
    title_servername = confdf.loc["conf","servername"]

    

    figa , ax2 = plt.subplots(figsize=(12,6))
    
    #sns.lineplot(data=datatemp1, x="TDATATIME1", y="total_cpu", ax=ax1)
    #ax1.axhline(y = virtualprocessors_x100 , color = 'b', linestyle = ':', label = "Total Number of VCPU / CPU * 100")
    #ax1.axhline(y = (virtualprocessors_x100 * 80) / 100 , color = 'r', linestyle = '--', label = "80% threshold")
    #ax1.set_title(title_servername + " Virtual processor consumption in percentage")
    #ax1.set_yticks(range(0,virtualprocessors_x100 + 1,100))
    #ax1.set_xlabel("datetime->")
    #ax1.set_xticklabels(ax1.get_xticklabels(),rotation = 45)
    #ax1.legend()

    sns.lineplot(data=datatemp2, x="TDATATIME1", y="total_cpu",hue="Command", ax=ax2)
    ax2.axhline(y = virtualprocessors_x100 , color = 'b', linestyle = ':', label = "Total Number of VCPU / CPU * 100")
    ax2.axhline(y = (virtualprocessors_x100 * 80) / 100 , color = 'r', linestyle = '--', label = "80% threshold")
    ax2.set_title(title_servername + " Top commands consuming CPU")
    ax2.set_yticks(range(0,virtualprocessors_x100 + 1,100))
    ax2.set_xlabel("datetime->")
    #ax2.set_xticklabels(ax2.get_xticklabels(),rotation = 45)
    #ax2.set_xlabel("hello")
    ax2.legend()
    
    figa.tight_layout() # tight_layout prevent overlapping of x labels between 2 figures
    #plt.tight_layout()
    figa.text(0.95, 0.05,   legends [::-1] + marker[::-1] + facecolors[::-1],
    fontsize=10, color='blue',
    ha='right', va='bottom', alpha=0.5) # adding watermark to charts
    list_figures.append(figa)
    matplotlib.pyplot.close(fig=figa)
    
    #figa.show();
    
    


#######################################################################################################################

def abhi_top_cpu_process_grapher():
    global list_figures
    global pdf_filename
    global confdf
    global topdf
    
    
    virtualprocessors_x100 = int(confdf.loc["conf","cpu_virtual"] * 100)
    title_servername = confdf.loc["conf","servername"]

    figb , (ax1,ax2) = plt.subplots(1,2,figsize=(12,6))
    datatemp3 = topdf.groupby(by=["PID","Command"]).agg(max_cpu=("%CPU",max))
    datatemp3 = datatemp3.reset_index()
    datatemp3 = datatemp3.sort_values(by="max_cpu",ascending=False)

#count of pid by group by commands
    datatemp4 = topdf.groupby(by=["Command"]).agg(number_of_commands=("PID","count")).reset_index().sort_values(by="number_of_commands",ascending=False)


##sns.barplot(data=datatemp3.head(10).sort_values(by="max_cpu",ascending=False),x="PID",y="max_cpu",ax=ax1, hue='Command',orient="v")
    sns.barplot(data=datatemp3.reset_index().head(10),x="PID",y="max_cpu",ax=ax1, hue='Command',orient="v")
    ax1.set_yticks(range(0,virtualprocessors_x100 + 1,100))
    ax1.set_xticklabels(ax1.get_xticklabels(),rotation=80)
    ax1.set_title(title_servername + " (100 == 1 CPU) Top 10 PID with highest CPU consumption")
    ax1.set_xlabel("datetime->")
    ax1.legend()

    sns.barplot(data=datatemp4,x="Command",y="number_of_commands",ax=ax2)
    ax2.set_title(title_servername + " : Number of process by commands")
    ax2.set_xticklabels(ax2.get_xticklabels(),rotation=85)
    ax2.set_xlabel("datetime->")
    ax2.legend()

    figb.tight_layout()
    figb.text(0.95, 0.05,   legends [::-1] + marker[::-1] + facecolors[::-1],
    fontsize=10, color='blue',
    ha='right', va='bottom', alpha=0.5) # adding watermark to charts
    list_figures.append(figb)
    matplotlib.pyplot.close(fig=figb)
    #figb.show();

#######################################################################################################################

def abhi_cpuall_and_lpar_grapher():
    global list_figures
    global pdf_filename
    global confdf
    global cpualldf
    global lpardf
    print(cpualldf.head(3))
    print(lpardf.head(3))
    
    cpu_frame_total = int(confdf.loc["conf","cpu_frame_total"])
    cpu_pool_total = int(confdf.loc["conf","cpu_pool_total"])
    
    
    lpardf['poolused'] = lpardf["poolCPUs"] - lpardf['PoolIdle'] # derive a new metrix
    print(lpardf.info())

    figb , (ax1,ax2) = plt.subplots(2,1,figsize=(12,8))
    
    cpualldf.plot(kind="area",stacked=True,y=["Sys%","User%","Wait%"],ax=ax1,label=["user","system","iowait"],x="TDATATIME1")
    ax1.set_title(title_servername + " :  CPU consumpion % ")
    ax1.axhline(y=100,color="r",linestyle ="-",linewidth=2.5)
    ax1.set_yticks(range(0,101,5))
    
    sns.lineplot(data=lpardf,x="TDATATIME1",y="poolCPUs",ax=ax2,label="Cores Total POOL-CPUs",color="b")
    sns.lineplot(data=lpardf,x="TDATATIME1",y="poolused",ax=ax2,label="Cores Consumed POOL CPU's by all lpars in the same pool",color="g")
    sns.lineplot(data=lpardf,x="TDATATIME1",y="PhysicalCPU",ax=ax2,label="Cores consumed by this LPAR",color="r")
    ax2.set_yticks(range(0,cpu_frame_total + 1 ,2))
    ax2.set_ylabel("cores - >")
    ax2.set_title(title_servername + " :  Cores consumed from pool ")


    #plt.xticks(rotation=90)
    
    figb.tight_layout()
    
    figb.text(0.95, 0.05,   legends [::-1] + marker[::-1] + facecolors[::-1],
    fontsize=10, color='blue',
    ha='right', va='bottom', alpha=0.5) # adding watermark to charts
    list_figures.append(figb)
    matplotlib.pyplot.close(fig=figb)
    
    

#######################################################################################################################



def abhi_memory_grapher():
    global list_figures
    global pdf_filename
    global confdf
    global memnewdf
    
    virtualprocessors_x100 = int(confdf.loc["conf","cpu_virtual"] * 100)
    title_servername = confdf.loc["conf","servername"]

    memnewdf["realmemory"] = memnewdf["Process%"] + memnewdf["System%"] 

    figb , (ax1,ax2) = plt.subplots(2,1,figsize=(12,6))

    #sns.lineplot(data=memnewdf,y= "realmemory", x='TDATATIME1',ax=ax1)
    memnewdf.plot(kind="area",color="r",y="realmemory",x='TDATATIME1',ax=ax1,label="realmemory = process + system")
    
    ax1.set_title(title_servername + " : Real memory% : process + system ")
    ax1.legend()
    ax1.set_xlabel("datetime->")
    ax1.set_yticks(range(0,101,5))

    sns.lineplot(data=memnewdf,y= "Process%", x='TDATATIME1',ax=ax2,color="b",label="processmemory%")
    sns.lineplot(data=memnewdf,y= "System%", x='TDATATIME1',ax=ax2,color='r',label="Systemmemory%")
    sns.lineplot(data=memnewdf,y= "FScache%", x='TDATATIME1',ax=ax2,color='g',label="FileCache-Memory%")
    #sns.lineplot(data=memnewdf,y= "Free%", x='TDATATIME1',ax=ax2,color='g',label="Free%")

    ax2.set_title(title_servername + " :  processMem and systemMEM ")
    ax2.legend()
    ax2.set_xlabel("datetime->")
    ax2.set_yticks(range(0,101,5))
    figb.tight_layout()
    figb.text(0.95, 0.05,   legends [::-1] + marker[::-1] + facecolors[::-1],
    fontsize=10, color='blue',
    ha='right', va='bottom', alpha=0.5) # adding watermark to charts
    list_figures.append(figb)
    matplotlib.pyplot.close(fig=figb)
    #figb.show();


#######################################################################################################################

def abhi_top_memory_command_grapher():
    global list_figures
    global pdf_filename
    global confdf
    global topdf
    
    topdf["ResTotalMB"] = (topdf["ResData"] + topdf["ResText"]) / 1024
    topdf.sort_values(by="ResTotalMB",ascending=False)
    
    #virtualprocessors_x100 = int(confdf.loc["conf","cpu_virtual"] * 100)
    title_servername = confdf.loc["conf","servername"]

    figb , (ax1,ax2) = plt.subplots(1,2,figsize=(12,6))
    datatemp3 = topdf.groupby(by=["PID","Command"]).agg(max_mem=("ResTotalMB",max)).reset_index().sort_values(by="max_mem",ascending=False)
    #datatemp3 = datatemp3.reset_index()
    #datatemp3 = datatemp3.sort_values(by="max_mem",ascending=False)



##sns.barplot(data=datatemp3.head(10).sort_values(by="max_cpu",ascending=False),x="PID",y="max_cpu",ax=ax1, hue='Command',orient="v")
    sns.barplot(data=datatemp3.sort_values(by="max_mem",ascending=False).head(10),x="PID",y="max_mem",ax=ax1, hue='Command',orient="v")
    #ax1.set_yticks(range(0,virtualprocessors_x100 + 1,100))
    ax1.set_xticklabels(ax1.get_xticklabels(),rotation=80)
    ax1.set_title(title_servername + " Top 10 PID with highest Memory consumption in MB")
    ax1.set_xlabel("datetime->")
    ax1.legend()
    
#count of pid by group by commands
    datatemp4 = topdf.groupby(by=["Command"]).agg(number_of_commands=("PID","count")).reset_index().sort_values(by="number_of_commands",ascending=False)


    sns.barplot(data=datatemp4,x="Command",y="number_of_commands",ax=ax2)
    ax2.set_title(title_servername + " : Number of process by commands")
    ax2.set_xticklabels(ax2.get_xticklabels(),rotation=85)
    ax2.set_xlabel("datetime->")
    ax2.legend()

    figb.tight_layout()
    figb.text(0.95, 0.05,   legends [::-1] + marker[::-1] + facecolors[::-1],
    fontsize=10, color='blue',
    ha='right', va='bottom', alpha=0.5) # adding watermark to charts
    list_figures.append(figb)
    matplotlib.pyplot.close(fig=figb)

#######################################################################################################################

def abhi_page_grapher():
    global list_figures
    global pdf_filename
    global confdf
    global pagedf
    
    virtualprocessors_x100 = int(confdf.loc["conf","cpu_virtual"] * 100)
    title_servername = confdf.loc["conf","servername"]

    #memnewdf["realmemory"] = memnewdf["Process%"] + memnewdf["System%"] 

    figb , (ax1,ax2) = plt.subplots(2,1,figsize=(12,4))

   
    sns.lineplot(data=pagedf,y= "pgsin", x='TDATATIME1',ax=ax1,color="b",label="4KB pages pulled from swapspace back to physical memory")
    sns.lineplot(data=pagedf,y= "pgsout", x='TDATATIME1',ax=ax1,color="r",label="4KB pages swapped out to swapfile due to memory contention")
    ax1.set_title(title_servername + " : Swap in and Swap out (look non zero red for memory contention)")
    ax1.legend()
    ax1.set_xlabel("datetime->")
    ax1.set_ylabel("Number of 4KB pages")
    #ax1.set_yticks(range(0,100,5))

    sns.lineplot(data=pagedf,y= "pgin", x='TDATATIME1',ax=ax2,color="b",label="4KB Swap pages + file pages : pulled to physical memory")
    sns.lineplot(data=pagedf,y= "pgout", x='TDATATIME1',ax=ax2,color="r",label="4KB Swap pages + file pages : pushed out from physical memory")
    
    ax2.set_title(title_servername + " :  Total pages (file + swap) in and out (non zero values does not indicate memory contention) ")
    ax2.legend()
    ax2.set_xlabel("datetime->")
    ax2.set_ylabel("Number of 4KB pages")
    #ax2.set_yticks(range(0,100,5))
    figb.tight_layout()
    figb.text(0.95, 0.05,   legends [::-1] + marker[::-1] + facecolors[::-1],
    fontsize=10, color='blue',
    ha='right', va='bottom', alpha=0.5) # adding watermark to charts
    list_figures.append(figb)
    matplotlib.pyplot.close(fig=figb)
    #figb.show();

#######################################################################################################################
def abhi_disk_grapher():
    global diskxferdf
    global diskwritedf
    global diskreaddf
    global diskbusydf
    global list_figures
    
    
    title_servername = confdf.loc["conf","servername"]
    
    figb , ((ax1,ax2,ax3,ax4)) = plt.subplots(4,1,figsize=(12,12))
    
    diskbusydf.describe().loc[["mean"],:].T.sort_values(by="mean",ascending=False).plot(kind="bar",ax=ax1,label="Disk Busy%")
    ax1.set_title(title_servername + " : Average Disk Busy%")
    diskwritedf.describe().loc[["mean"],:].T.sort_values(by="mean",ascending=False).plot(kind="bar",ax=ax2,label="KB write")
    ax2.set_title(title_servername + " : Average Disk write KB")
    diskreaddf.describe().loc[["mean"],:].T.sort_values(by="mean",ascending=False).plot(kind="bar",ax=ax3,label="KB read")
    ax3.set_title(title_servername + " : Average Disk read KB")
    diskxferdf.describe().loc[["mean"],:].T.sort_values(by="mean",ascending=False).plot(kind="bar",ax=ax4,label="Total IN+OUT Transfer IO")
    ax4.set_title(title_servername + " :Average Disk Transfer Total (read IO + Write IO)")
    
    
    
    figb.tight_layout()
    figb.text(0.95, 0.05,   legends [::-1] + marker[::-1] + facecolors[::-1],
    fontsize=10, color='blue',
    ha='right', va='bottom', alpha=0.5) # adding watermark to charts
    list_figures.append(figb)
    matplotlib.pyplot.close(fig=figb)
    


#######################################################################################################################

def abhi_jfsfilesystem_grapher():
    global list_figures
    global jfsfiledf
    
    
    title_servername = confdf.loc["conf","servername"]
    
    figb , ((ax1)) = plt.subplots(1,1,figsize=(12,8))
    
    jfsfiletempdf = jfsfiledf.loc[:,jfsfiledf.columns.str.startswith("/")].describe().loc[["max"],:].T.sort_values(by="max",ascending=False)
    
    jfsfiletempdf[jfsfiletempdf['max'] > 85].plot(kind="bar",figsize=(12,12),ax=ax1)
    ax1.set_title(title_servername + " : Filesystem max consumtion : greater than 85%")
    
    #jfsfiletempdf[jfsfiletempdf['max'] < 20].plot(kind="barh",ax=ax2)
    #ax2.set_title(title_servername + " : Filesystem max consumtion : Less than 20%")
    print("abhi jfsfile")
    
    figb.tight_layout()
    figb.text(0.95, 0.05,   legends [::-1] + marker[::-1] + facecolors[::-1],
    fontsize=10, color='blue',
    ha='right', va='bottom', alpha=0.5) # adding watermark to charts
    list_figures.append(figb)
    matplotlib.pyplot.close(fig=figb)
    
    


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

def abhi_parser_module(csv_filename,starting_text):
    global zzzzdf
    global confdf
    global custom_delimiter
    global Lines
    
    tempfile = open(f"{csv_temp_dir}/{csv_filename}", 'w')
    for thisline in Lines:
        if thisline.startswith(starting_text): #CPU_ALL LPAR
        #print(thisline.strip())
            tempfile.writelines(thisline)
    tempfile.close()
    df = pd.read_csv(f"{csv_temp_dir}/{csv_filename}",skiprows=0,sep = custom_delimiter)
    old_colname= str(df.columns[1])
    df.rename(columns = {old_colname:'TXXX'}, inplace = True) # this is for creating a common fieldname before merging 2 csv
    df = pd.merge(df, zzzzdf, on="TXXX")
    df.index = df["TDATATIME"]
    df.rename(columns = {"TDATATIME":'TDATATIME1'}, inplace = True)
    #lpardf.set_index("TDATATIME",inplace=True)
    print(df.info())
    #df.head()
    return df

#######################################################################################################################




Lines = file1.readlines()
csv_temp_dir = "csv_temp_dir"
os.makedirs(csv_temp_dir, exist_ok = True) # create a new directory

print("##" * 100,"\n BBBL - AIX configuration\n")

bbblfile = open(f'{csv_temp_dir}/configuration-bbbl.csv', 'w')
for thisline in Lines:
    if thisline.startswith("BBBL"):
        #print(thisline.strip())
        bbblfile.writelines(thisline)
custom_delimiter = thisline[4] # linux has delimoter ";" aix has "," so we need to pick from the file
bbblfile.close()
bbbldf = pd.read_csv(f'{csv_temp_dir}/configuration-bbbl.csv',names=["BBBL","NBR","metric","conf"])
bbbldf.set_index("metric",inplace=True)
print(bbbldf.info())
#print(bbbldf)

configuration_dict = {

'servername' : bbbldf.loc['lparname','conf'],
'cpu_frame_total' : int(bbbldf.loc['CPU in sys','conf']),
'cpu_frame_total' : int(bbbldf.loc['CPU in sys','conf']),
'cpu_pool_total' : int(bbbldf.loc['Pool CPU','conf']),
'cpu_virtual' : int(bbbldf.loc['Virtual CPU','conf']),
'cpu_entitlement' : float(bbbldf.loc['Entitled Capacity','conf']),
'memory_installedGB' : int(int(bbbldf.loc['online Memory','conf']) / 1024 )
                        }
confdf = pd.DataFrame(configuration_dict,index=["conf"])
print(confdf.info())
print(confdf)

title_servername = confdf.loc["conf","servername"]
pp = PdfPages(title_servername + pdf_filename)



print("##" * 100,"\nZZZZ - Time\n")

zzzzfile = open(f'{csv_temp_dir}/zzzz.csv', 'w')
for thisline in Lines:
    if thisline.startswith("ZZZZ"):
        #print(thisline.strip())
        zzzzfile.writelines(thisline)
custom_delimiter = thisline[4] # linux has delimoter ";" aix has "," so we need to pick from the file
custom_delimiter =","
zzzzfile.close()
zzzzdf = pd.read_csv(f"{csv_temp_dir}/zzzz.csv",skiprows=0,names=["ZZZZ","TXXX","TTIME","TDATE"],sep = custom_delimiter)
zzzzdf["TDATATIME"] = zzzzdf["TDATE"] + " " + zzzzdf["TTIME"]
zzzzdf["TDATATIME"] = zzzzdf["TDATATIME"].apply(abhi_convert_to_date)
print(zzzzdf.info())
#print(zzzzdf.head())


print("##" * 100,"\nTopdf\n")

# read the file which starts with "TOP" . slip the first line

topfile = open(f'{csv_temp_dir}/top.csv', 'w')
for thisline in Lines:
    if thisline.startswith("TOP"):
        #print(thisline.strip())
        topfile.writelines(thisline)
topfile.close()
topdf = pd.read_csv(f"{csv_temp_dir}/top.csv",skiprows=1,sep = custom_delimiter)
#old_colname= str(topdf.columns[1])
topdf.rename(columns = {"Time":'TXXX'}, inplace = True)
topdf.rename(columns = {"+PID":'PID'}, inplace = True)
topdf = pd.merge(topdf, zzzzdf, on="TXXX")
#topdf.set_index("TDATATIME",inplace=True)
topdf.index = topdf["TDATATIME"]
topdf.rename(columns = {"TDATATIME":'TDATATIME1'}, inplace = True)
print(topdf.info())
topdf.to_csv(f"{csv_temp_dir}/topfinal.csv")
topdf.head()


print("##" * 100)

lpardf = abhi_parser_module("lpar.csv","LPAR")
cpualldf = abhi_parser_module("cpuall.csv","CPU_ALL")
memnewdf = abhi_parser_module("memnew.csv","MEMNEW")
pagedf = abhi_parser_module("page.csv","PAGE")



diskxferdf = abhi_parser_module("diskxfer.csv","DISKXFER")
diskbusydf = abhi_parser_module("diskbusy.csv","DISKBUSY")


'''
Diskwerite and Diskread also has Diskwritesrvc and diskreadsrvc parsed from the nmon file
So after parsing we need to filter out only Diskwrite
diskwritedf also has a problem all columns are parsed as object. 
We need to exclude columns not stating with "hd*" before chnverting entire dataframe as float / numeris

'''
diskwritedf = abhi_parser_module("diskwrite.csv","DISKWRITE")
diskwritedf = diskwritedf[diskwritedf['DISKWRITE'] == 'DISKWRITE']
diskwritedf = diskwritedf.loc[:,diskwritedf.columns.str.startswith('hdisk')]
diskwritedf = diskwritedf.apply(pd.to_numeric, errors='coerce')

'''
Diskwerite and Diskread also has Diskwritesrvc and diskreadsrvc parsed from the nmon file
So after parsing we need to filter out only Diskwrite
diskwritedf also has a problem all columns are parsed as object. 
We need to exclude columns not stating with "hd*" before chnverting entire dataframe as float / numeris

'''

diskreaddf = abhi_parser_module("diskread.csv","DISKREAD")
diskreaddf = diskreaddf[diskreaddf['DISKREAD'] == 'DISKREAD'] # DISKREAD annd DISKREADSRVC is parsed from some nmon .filter
diskreaddf = diskreaddf.loc[:,diskreaddf.columns.str.startswith('hdisk')]
diskreaddf = diskreaddf.apply(pd.to_numeric, errors='coerce')


jfsfiledf = abhi_parser_module("jfsfile.csv","JFSFILE")

diskxferdf.head()

abhi_cpuall_and_lpar_grapher()
abhi_top_cpu_command_grapher()
abhi_top_cpu_process_grapher()
abhi_memory_grapher()
abhi_top_memory_command_grapher()
abhi_page_grapher()
abhi_disk_grapher()
#abhi_jfsfilesystem_grapher()

for figures in list_figures:
    figures.savefig(pp, format='pdf')  

pp.close()

print("completed. Check pdf file in the current directory")
    
