# Coen366NewsSharing


## Run

``` powershell
cd Coen366NewsSharing
python -m server.main
```

## Test (new terminal)

``` powershell
cd Coen366NewsSharing/ NSS_CSharp
open NSS_CSharp.slnx
go to Form1.cs
change line 62 and set the path to pyhton.exe. You can find python.exe using "which python" command on terminal 
example: string pythonExe = @"C:\Users\user1\AppData\Local\Microsoft\WindowsApps\python.exe";
After starting the server using "python -m server.main" you can run the c sharp form.
only use the top section of the form and register button (that's the only implemented function for now) which is "User Info / Connection"

---------------------------------------
An example usage to test the connection:

Name: Alice
TCP Port: 5000
Server IP: 127.0.0.1
IP: 127.0.0.1
UDP Port: 6000
Server TCP: 10000

----------------------------------------
click Register
```

## Start Servers

``` powershell
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
python -m create_client ClientName 192.168.1.100

# Without server IP (defaults to 127.0.0.1)
python -m create_client ClientName
----------------------------------------
```