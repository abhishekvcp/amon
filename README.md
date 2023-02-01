# amon
<h3>
<p>This python script produces a pdf file reading through a .nmon file for AIX servers></p>

![image](https://user-images.githubusercontent.com/46884901/216034351-f2fb2415-be38-4816-9adc-42bf6f9448e7.png)
![image](https://user-images.githubusercontent.com/46884901/216034503-cd208744-0792-4576-8879-49b558c7c2c5.png)
![image](https://user-images.githubusercontent.com/46884901/216034589-37dd14f5-ae54-4575-805e-3e7463d04c5d.png)
![image](https://user-images.githubusercontent.com/46884901/216034648-444c01b3-8052-4a96-9a10-a21a43eaacaa.png)
![image](https://user-images.githubusercontent.com/46884901/216034699-a73fca41-64f3-4fd6-b499-639498369655.png)
![image](https://user-images.githubusercontent.com/46884901/216034761-e833f85b-d1e7-4f19-aac4-d5106f2e5f36.png)
</h3>
<h4>
<ol>Produces a pdf output file file</ol>
<ol>Produces top CPU and Memory consuming commands / process </ol>
<ol>Produces below csv files in the temporary subdirectory csv_temp_dir </ol>
</h4>
<h5>
<ol>configuration-bbbl.csv</ol>
<ol>cpuall.csv</ol>
<ol>diskbusy.csv</ol>
<ol>diskread.csv</ol>
<ol>diskwrite.csv</ol>
<ol>diskxfer.csv</ol>
<ol>jfsfile.csv</ol>
<ol>lpar.csv</ol>
<ol>memnew.csv</ol>
<ol>page.csv</ol>
<ol>top.csv</ol>
<ol>topfinal.csv</ol>
<ol>zzzz.csv</ol>

</h5>

python parser for aIX .nmon file visualization. <br>Run the script amon_aix.py <br>Supply input filewait for 2 mins

method1 : Run manually 
![image](https://user-images.githubusercontent.com/46884901/216031772-eb6e9a5c-4265-4caf-89c4-4dacc343a568.png)

![image](https://user-images.githubusercontent.com/46884901/216031896-43ddae08-1f01-458e-a719-f21a70dd4549.png)


Method 2 : Run via automation : passing nmon file as a parameter 

![image](https://user-images.githubusercontent.com/46884901/216031669-388d0647-e617-4587-8420-d4f9120b37dd.png)

<br>
-----------------------------------------SETUP VENV steps-----------------------------------------------------------------
<br>
python3 -m venv amon
<br>
cd amon
<br>
source bin/activate [linux]
<br>
Scripts/activate[Windows]
<br>
pip install -r amon_requirements.txt
<br>
-----------------------------------------SETUP VENV-----------------------------------------------------------------

Contact : abhishek.vcp@gmail.com
mob : 9740722880
