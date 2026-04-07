# Coen366NewsSharing

## Start Servers

``` powershell
Delete existing databases
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
Open NSS_CSharp.slnx
Go to Form1.cs
Change line 13  private bool isServerMode = true; if you are running server or private bool isServerMode = false; if it's a client. (We will bind this switch functionality to a radiobox later so we can change this variable on the UI)
Change line 102 and set the path to pyhton.exe. You can find python.exe using "which python" command on terminal 
Example: string pythonExe = @"C:\Users\user1\AppData\Local\Microsoft\WindowsApps\python.exe";
After starting the server using "python -m server.main" and registering clients you can run the Csharp form.
```
