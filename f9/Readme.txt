BIOS Setup Automation Tool v1.8
Author: Jason Chen

Based on 2819547 25.0 FI_Hardware_Preparation_of_HP_ProLiant_Servers_TOP

Supported Hardware:
HP BL460 G9
BL460 G10
DL380 G10

Supported OS:
WSOE (Windows)
LSOE (Linux)
VSOE (VMware)
SSOE (Suse)

How to use:
1. Login to iLO web console (Recommend to run on jumpstation)
2. Open remote console by using Java Web Start 
3. Maximize console window, reset server
4. Fill hardware,OS,Server Name, Click 'Go' and let go

Known Issue:
* Only support run one instance at one time
* Only support Java Web Start console
* SAN connection is not disabled in BIOS by this tool
* If lantency to iLO is high, screen shot may capture the wrong picture
* It could take seconds to recognize image