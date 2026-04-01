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
        private Process _pythonProcess;
        private bool _updatingCombo = false;
        private bool _pythonReady = false;


        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            InitializeSubjects();
            server_1_tb.Text = "127.0.0.1";
            servertcp_1_tb.Text = "10000";
            StartPythonBridge();


        }

        private void InitializeSubjects()
        {
            subjects_2_clb.Items.Clear();

            subjects_2_clb.Items.Add("Sports");
            subjects_2_clb.Items.Add("Entertainment");
            subjects_2_clb.Items.Add("Health");
            subjects_2_clb.Items.Add("Science");
            subjects_2_clb.Items.Add("Technology");
            subjects_2_clb.Items.Add("Politics");
            subjects_2_clb.Items.Add("Business");
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

        private void HandlePythonLine(string line)
        {
            if (InvokeRequired)
            {
                BeginInvoke(new Action(() => HandlePythonLine(line)));
                return;
            }
            if (line == "PYTHON CLIENT READY")
            {
                _pythonReady = true;
                AppendIncoming(line);

                SendCommand($"LOADUSERS {server_1_tb.Text} {servertcp_1_tb.Text}");
                return;
            }

            if (line.StartsWith("CLIENT-ADDED|"))
            {
                string key = line.Split('|')[1];

                _updatingCombo = true;
                if (!clients_1_cb.Items.Contains(key))
                    clients_1_cb.Items.Add(key);
                clients_1_cb.SelectedItem = key;
                _updatingCombo = false;
            }
            else if (line.StartsWith("CLIENT-REMOVED|"))
            {
                string key = line.Split('|')[1];

                _updatingCombo = true;
                clients_1_cb.Items.Remove(key);

                if (clients_1_cb.Items.Count > 0)
                    clients_1_cb.SelectedIndex = 0;
                else
                    clients_1_cb.Text = "";

                _updatingCombo = false;
            }
            else if (line.StartsWith("CLIENT-SELECTED|"))
            {
                string key = line.Split('|')[1];

                _updatingCombo = true;
                if (clients_1_cb.Items.Contains(key))
                    clients_1_cb.SelectedItem = key;
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
                clients_1_cb.Items.Clear();
                clients_1_cb.Text = "";
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
            clients_1_cb.Items.Clear();

            if (!string.IsNullOrWhiteSpace(csv))
            {
                foreach (string item in csv.Split(new[] { ',' }, StringSplitOptions.RemoveEmptyEntries))
                    clients_1_cb.Items.Add(item);

                if (clients_1_cb.Items.Count > 0)
                    clients_1_cb.SelectedIndex = 0;
            }

            _updatingCombo = false;
        }

        private void ApplyState(string line)
        {
            string[] parts = line.Split('|');

            // STATE|name|ip|tcp|udp|serverip|serverport|registered|subjects
            if (parts.Length < 9)
                return;

            name_1_tb.Text = parts[1];
            ip_1_tb.Text = parts[2];
            tcp_1_tb.Text = parts[3];
            udp_1_tb.Text = parts[4];
            server_1_tb.Text = parts[5];
            servertcp_1_tb.Text = parts[6];

            string subjectsCsv = parts[8];

            var selectedSubjects = new HashSet<string>(
                subjectsCsv.Split(new[] { ',' }, StringSplitOptions.RemoveEmptyEntries)
            );

            for (int i = 0; i < subjects_2_clb.Items.Count; i++)
            {
                string subject = subjects_2_clb.Items[i].ToString();
                subjects_2_clb.SetItemChecked(i, selectedSubjects.Contains(subject));
            }
        }

        private void ClearClientFields()
        {
            name_1_tb.Text = "";
            ip_1_tb.Text = "";
            tcp_1_tb.Text = "";
            udp_1_tb.Text = "";
            server_1_tb.Text = "";
            servertcp_1_tb.Text = "";

            for (int i = 0; i < subjects_2_clb.Items.Count; i++)
                subjects_2_clb.SetItemChecked(i, false);
        }

        private void AppendIncoming(string text)
        {
            if (InvokeRequired)
            {
                BeginInvoke(new Action(() => AppendIncoming(text)));
                return;
            }

            incoming_3_ltb.AppendText(text + Environment.NewLine);
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

        private void register_1_bt_Click(object sender, EventArgs e)
        {
            string cmd =
                $"REGISTER {name_1_tb.Text} {ip_1_tb.Text} {tcp_1_tb.Text} {udp_1_tb.Text} {server_1_tb.Text} {servertcp_1_tb.Text}";
            SendCommand(cmd);
        }

        private void update_1_bt_Click(object sender, EventArgs e)
        {
            string cmd =
                $"UPDATE {ip_1_tb.Text} {tcp_1_tb.Text} {udp_1_tb.Text} {servertcp_1_tb.Text}";
            SendCommand(cmd);
        }

        private void deregister_1_bt_Click(object sender, EventArgs e)
        {
            SendCommand("DEREGISTER");
        }

        private void updatesubjects_2_bt_Click(object sender, EventArgs e)
        {
            var selected = subjects_2_clb.CheckedItems
                .Cast<object>()
                .Select(x => x.ToString())
                .ToList();

            if (selected.Count == 0)
            {
                MessageBox.Show("Select at least one subject.");
                return;
            }

            string cmd = "SUBJECTS " + string.Join(" ", selected);
            SendCommand(cmd);
        }

        private void clients_1_cb_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (_updatingCombo)
                return;

            if (clients_1_cb.SelectedItem == null)
                return;

            string key = clients_1_cb.SelectedItem.ToString();
            SendCommand($"SELECT {key}");
        }

        protected override void OnFormClosing(FormClosingEventArgs e)
        {
            try
            {
                if (_pythonProcess != null && !_pythonProcess.HasExited)
                {
                    _pythonProcess.StandardInput.WriteLine("EXIT");
                    _pythonProcess.StandardInput.Flush();

                    if (!_pythonProcess.WaitForExit(1000))
                        _pythonProcess.Kill();
                }
            }
            catch
            {
            }

            base.OnFormClosing(e);
        }
    }
}