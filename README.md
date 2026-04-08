# Coen366NewsSharing

## Start Servers

``` powershell
First, delete existing databases 
----------------------------------------
### If IPs are unknown, discover then configure

# Terminal 1 - Start Server A (it will wait for input)
python -m server.main A

# Terminal 2 - Start Server B first (similar prompt)
python -m server.main B 

# Now you can feed the IP addresses at each prompt
----------------------------------------
```

## Start Clients

``` powershell
----------------------------------------
# With server IP specified
python -m create_client [ClientName] [Server IP] 
```
## Test (new terminal)

``` powershell
cd Coen366NewsSharing/ NSS_CSharp
Change line 304 and set the path to pyhton.exe. You can find python.exe using "which python" command on terminal 
Example: string pythonExe = @"C:\Users\user1\AppData\Local\Microsoft\WindowsApps\python.exe";
After starting the server using "python -m server.main" and registering clients you can run the Csharp form.

```
## Running the Form
``` powershell
Go to Coen366NewsSharing\NSS_CSharp\bin\Release
run the NSS.exe with the following arguments:
 "NSS.exe client" if this computer is a client
 "NSS.exe server A" if this computer is a the server A
 "NSS.exe server B" if this computer is a the server B
```

## Running the traffic_runner.py
``` powershell
Linux: python3 traffic_runner.py [server IP] [Server UDP Port]
Windows: python.exe .\traffic_runner.py [server IP] [Server UDP Port]
```
