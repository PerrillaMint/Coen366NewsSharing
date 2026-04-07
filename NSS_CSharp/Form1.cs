using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Windows.Forms;

namespace NSS
{
    public partial class Form1 : Form
    {

        private bool isServerMode = true;   // true = server side active, false = client side active
        private bool isServerA = true;      // true = Server A, false = Server B



        private Process _pythonProcess;
        private bool _updatingCombo = false;
       

        public Form1()
        {
            InitializeComponent();
        }

        private void InitializeServerSide()
        {
            string serverId = isServerA ? "A" : "B";
            SendCommand($"INIT_SERVER {serverId}");
        }
        private void ApplyClientInit(string line)
        {
            string[] parts = line.Split('|');

            // CLIENT-INIT|name|ip|tcpPort|udpPort|serverIp|serverTcp
            if (parts.Length < 7)
                return;

            if (!isServerMode)
            {
                name_1_tb.Text = parts[1];
                ip_1_tb.Text = parts[2];
                tcpPort_1_tb.Text = parts[3];
                udpPort_1_tb.Text = parts[4];
                serverIp_1_tb.Text = parts[5];
                serverTcp_1_tb.Text = parts[6];

                name_1_tb.ReadOnly = true;
                ip_1_tb.ReadOnly = true;
                tcpPort_1_tb.ReadOnly = true;
                udpPort_1_tb.ReadOnly = true;
                serverIp_1_tb.ReadOnly = true;
                serverTcp_1_tb.ReadOnly = true;
            }
        }
        private void InitializeClientSide()
        {
            string serverId = isServerA ? "A" : "B";
            string serverIp = "192.168.0.58";   // your Linux server IP for now

            SendCommand($"INIT_SERVER {serverId} {serverIp}");
        }
       

        private void InitializeActiveSide()
        {
            if (isServerMode)
                InitializeServerSide();
            else
                InitializeClientSide();
        }
       
        private void Form1_Load(object sender, EventArgs e)
        {
            InitializeSubjects();
            StartPythonBridge();


        }

        private void InitializeSubjects()
        {
            subject_1_cb.Items.Clear();

            subject_1_cb.Items.Add("Sports");
            subject_1_cb.Items.Add("Entertainment");
            subject_1_cb.Items.Add("Health");
            subject_1_cb.Items.Add("Science");
            subject_1_cb.Items.Add("Technology");
            subject_1_cb.Items.Add("Politics");
            subject_1_cb.Items.Add("Business");

           
        }

        private void StartPythonBridge()
        {

            try
            {
                string pythonExe = @"C:\Users\blue\AppData\Local\Microsoft\WindowsApps\python.exe";
                string scriptPath = Path.Combine(Application.StartupPath, @"C:\Users\blue\Desktop\Coen366NewsSharing\client_app.py");

                var psi = new ProcessStartInfo

                {
                    FileName = pythonExe,
                    Arguments = $"\"{scriptPath}\"",
                    UseShellExecute = false,
                    RedirectStandardInput = true,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true
                };
                psi.EnvironmentVariables["PEER_IP"] = "127.0.0.1";

                _pythonProcess = new Process();
                _pythonProcess.StartInfo = psi;
                _pythonProcess.OutputDataReceived += PythonOutputReceived;
                _pythonProcess.ErrorDataReceived += PythonErrorReceived;

                _pythonProcess.Start();
                _pythonProcess.BeginOutputReadLine();
                _pythonProcess.BeginErrorReadLine();
            }
            catch (Exception ex)
            {
                MessageBox.Show("Failed to start Python bridge: " + ex.Message);
            }
        }

        private void PythonOutputReceived(object sender, DataReceivedEventArgs e)
        {
            if (string.IsNullOrWhiteSpace(e.Data))
                return;

            HandlePythonLine(e.Data);
        }

        private void PythonErrorReceived(object sender, DataReceivedEventArgs e)
        {
            if (string.IsNullOrWhiteSpace(e.Data))
                return;

            AppendIncoming("[PY-ERR] " + e.Data);
        }
        private void ApplyServerInit(string line)
        {
            string[] parts = line.Split('|');

            // SERVER-INIT|serverName|serverIp|tcpPort|ip|udpPort|serverTcp
            if (parts.Length < 7)
                return;

            if (isServerMode)
            {
                name_2_tb.Text = parts[1];
                serverIp_2_tb.Text = parts[2];
                tcpPort_2_tb.Text = parts[3];
                ip_2_tb.Text = parts[4];
                udpPort_2_tb.Text = parts[5];
                serverTcp_2_tb.Text = parts[6];

                name_2_tb.ReadOnly = true;
                serverIp_2_tb.ReadOnly = true;
                tcpPort_2_tb.ReadOnly = true;
                ip_2_tb.ReadOnly = true;
                udpPort_2_tb.ReadOnly = true;
                serverTcp_2_tb.ReadOnly = true;

                SendCommand($"LOADUSERS {serverIp_2_tb.Text} {tcpPort_2_tb.Text}");
            }
            else
            {
                SendCommand("INIT_CLIENT");
            }
        }
        private void clients_2_cb_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (_updatingCombo)
                return;

            if (clients_2_cb.SelectedItem == null)
                return;

            string key = clients_2_cb.SelectedItem.ToString();
            SendCommand($"SELECT {key}");
        }

        private void HandlePythonLine(string line)
        {
            if (InvokeRequired)
            {
                BeginInvoke(new Action(() => HandlePythonLine(line)));
                return;
            }

            if (line == "PYTHON CLIENT READY")
            {
              
                AppendIncoming(line);
                InitializeActiveSide();
                return;
            }
            else if (line.StartsWith("SERVER-INIT|"))
            {
                ApplyServerInit(line);
            }
            else if (line.StartsWith("CLIENT-INIT|"))
            {
                ApplyClientInit(line);
            }
            else if (line.StartsWith("CLIENT-ADDED|"))
            {
                string key = line.Split('|')[1];

                _updatingCombo = true;
                if (!clients_2_cb.Items.Contains(key))
                    clients_2_cb.Items.Add(key);
                clients_2_cb.SelectedItem = key;
                _updatingCombo = false;
            }
            else if (line.StartsWith("CLIENT-REMOVED|"))
            {
                string key = line.Split('|')[1];

                _updatingCombo = true;
                clients_2_cb.Items.Remove(key);

                if (clients_2_cb.Items.Count > 0)
                    clients_2_cb.SelectedIndex = 0;
                else
                    clients_2_cb.Text = "";

                _updatingCombo = false;
            }
            else if (line.StartsWith("CLIENT-SELECTED|"))
            {
                string key = line.Split('|')[1];

                _updatingCombo = true;
                if (clients_2_cb.Items.Contains(key))
                    clients_2_cb.SelectedItem = key;
                _updatingCombo = false;
            }
            else if (line.StartsWith("CLIENT-LIST|"))
            {
                LoadClientList(line);
            }
            else if (line.StartsWith("STATE|"))
            {
                ApplyState(line);
            }
            else if (line == "NO-CLIENTS")
            {
                ClearClientFields();

                _updatingCombo = true;
                clients_2_cb.Items.Clear();
                clients_2_cb.Text = "";
                _updatingCombo = false;
            }
            else
            {
                AppendIncoming(line);
            }
        }

        private void LoadClientList(string line)
        {
            string[] parts = line.Split('|');
            string csv = parts.Length > 1 ? parts[1] : "";

            _updatingCombo = true;
            clients_2_cb.Items.Clear();

            if (!string.IsNullOrWhiteSpace(csv))
            {
                foreach (string item in csv.Split(new[] { ',' }, StringSplitOptions.RemoveEmptyEntries))
                    clients_2_cb.Items.Add(item);

                if (clients_2_cb.Items.Count > 0)
                    clients_2_cb.SelectedIndex = 0;
            }

            _updatingCombo = false;
        }

        private void ApplyState(string line)
        {
            string[] parts = line.Split('|');

            // STATE|name|ip|tcp|udp|serverip|serverport|registered|subjects
            if (parts.Length < 9)
                return;

            name_2_tb.Text = parts[1];
            ip_2_tb.Text = parts[2];
            tcpPort_2_tb.Text = parts[3];
            udpPort_2_tb.Text = parts[4];
            serverIp_2_tb.Text = parts[5];
            serverTcp_2_tb.Text = parts[6];

            string subjectsCsv = parts[8];
            string[] subjects = subjectsCsv.Split(new[] { ',' }, StringSplitOptions.RemoveEmptyEntries);

        }

        private void ClearClientFields()
        {
            name_2_tb.Text = "";
            ip_2_tb.Text = "";
            tcpPort_2_tb.Text = "";
            udpPort_2_tb.Text = "";
            serverIp_2_tb.Text = "";
            serverTcp_2_tb.Text = "";
            
        }

        private void AppendIncoming(string text)
        {
            if (InvokeRequired)
            {
                BeginInvoke(new Action(() => AppendIncoming(text)));
                return;
            }

            if (isServerMode)
                feed_2_rtb.AppendText(text + Environment.NewLine);
            else
                feed_1_rtb.AppendText(text + Environment.NewLine);
        }
        private void SendCommand(string cmd)
        {
            try
            {
                if (_pythonProcess != null && !_pythonProcess.HasExited)
                {
                    _pythonProcess.StandardInput.WriteLine(cmd);
                    _pythonProcess.StandardInput.Flush();
                }
                else
                {
                    MessageBox.Show("Python bridge is not running.");
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Failed to send command: " + ex.Message);
            }
        }

 
    }
}