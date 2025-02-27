Make sure to download the requirements.txt file if you plan on using the GUI

KEY NOTE: the header is exactly 34,816 bytes long

pip install -r requirements.txt



-- PYTHON SCRIPT --
Open CMD and cd rfiqd_flattening_python_script master file

Run the shell script and feed in the original RFIQD file as a parameter.

for example:
python Reduce_RFIQD_size.py "D:\DV2 Pilot Original - Working\Recorded IQ Data\2023-10-17_13-18-50_CTR-7.9GHz_SP-100MHz-NEX18100414\2023-10-17_13-18-50.741.rfiqd"


The Output folder in the Repo is the default location. Add --outdir "D:/output/directory"
if you would like to Specify the location

The program supports multiple files, add as many as you would like to reduce the file size.

for example:
python Reduce_RFIQD_size.py "D:\DV2 Pilot Original - Working\Recorded IQ Data\2023-10-17_13-18-50_CTR-7.9GHz_SP-100MHz-NEX18100414\2023-10-17_13-18-50.741.rfiqd" 
"D:\DV2 Pilot Original - Working\Recorded IQ Data\2023-10-17_13-18-50_CTR-7.9GHz_SP-100MHz-NEX18100414\2023-10-17_13-19-01.193.rfiqd"
 --outdir "D:\Repos\testing-tools-devops-pipeline\rfiqd_flattening_python_script\Output\test"




-- SHELL SCRIPT --

To reduce the RFIQD file size, follow the steps below:

Open GitBash and cd rfiqd_flattening_python_script master file

Run the shell script and feed in the original RFIQD file as a parameter.


for example:
./Reduce_RFIQD_size.sh "D:/path/to/your/original/RFIQD_File.rfiqd"

Once run, a new file will appear in the Output folder in the root directory.

The Output folder in the Repo is the default location. Add --outdir "D:/output/directory"
if you would like to Specify the location

The program supports multiple files, add as many as you would like to reduce the file size.

for example:
./Reduce_RFIQD_size.sh "D:/path/1/RFIQD_File.rfiqd" "D:/path/2/RFIQD_File.rfiqd" --outdir "D:/output/directory"
This will process two RFIQD files and output them to "D:/output/directory"



-- BATCH SCRIPT --
Open CMD and cd rfiqd_flattening_python_script master file

Run the shell script and feed in the original RFIQD file as a parameter.

for example:
Reduce_RFIQD_size.bat "D:\DV2 Pilot Original - Working\Recorded IQ Data\2023-10-17_13-18-50_CTR-7.9GHz_SP-100MHz-NEX18100414\2023-10-17_13-18-50.741.rfiqd"


The Output folder in the Repo is the default location. Add --outdir "D:/output/directory"
if you would like to Specify the location

The program supports multiple files, add as many as you would like to reduce the file size.

for example:
Reduce_RFIQD_size.bat "D:\DV2 Pilot Original - Working\Recorded IQ Data\2023-10-17_13-18-50_CTR-7.9GHz_SP-100MHz-NEX18100414\2023-10-17_13-18-50.741.rfiqd" 
"D:\DV2 Pilot Original - Working\Recorded IQ Data\2023-10-17_13-18-50_CTR-7.9GHz_SP-100MHz-NEX18100414\2023-10-17_13-19-01.193.rfiqd"
 --outdir "D:\Repos\testing-tools-devops-pipeline\rfiqd_flattening_python_script\Output\test"