using System;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Windows.Forms;

namespace NSS
{
    public partial class Form1 : Form
    {
        private Timer _refreshTimer;
        private bool isServerMode = false;   // true = server side active, false = client side active
        private bool isServerA = true;      // true = Server A, false = Server B

        private void InitializeSubjects()
        {
            subjects_1_clb.Items.Clear();
            subject_1_cb.Items.Clear();

            string[] subjects =
            {
                "Sports",
                 "Entertainment",
                 "Health",
                 "Science",
                 "Technology",
                 "Politics",
                 "Business"
    };

            foreach (string subject in subjects)
            {
                subjects_1_clb.Items.Add(subject);
                subject_1_cb.Items.Add(subject);
            }
        }

        private bool ShouldShowClientLine(string line)
        {
            if (string.IsNullOrWhiteSpace(line))
                return false;

            if (line == "PYTHON CLIENT READY")
                return true;

            if (line.StartsWith("MESSAGE|"))
                return true;

            if (line.StartsWith("COMMENT|"))
                return true;

            if (line.StartsWith("ERROR|"))
                return false;

            return false;
        }
        private void LockClientConnectionFields()
        {
            name_1_tb.ReadOnly = true;
            tcpPort_1_tb.ReadOnly = true;
            udpPort_1_tb.ReadOnly = true;
            serverIp_1_tb.ReadOnly = true;
            serverTcp_1_tb.ReadOnly = true;

            name_1_tb.Enabled = false;
            tcpPort_1_tb.Enabled = false;
            udpPort_1_tb.Enabled = false;
            serverIp_1_tb.Enabled = false;
            serverTcp_1_tb.Enabled = false;
        }
        private void UnlockClientConnectionFields()
        {
            name_1_tb.ReadOnly = false;
            tcpPort_1_tb.ReadOnly = false;
            udpPort_1_tb.ReadOnly = false;
            serverIp_1_tb.ReadOnly = false;
            serverTcp_1_tb.ReadOnly = false;

            name_1_tb.Enabled = true;
            tcpPort_1_tb.Enabled = true;
            udpPort_1_tb.Enabled = true;
            serverIp_1_tb.Enabled = true;
            serverTcp_1_tb.Enabled = true;

            ip_1_tb.ReadOnly = true;
            ip_1_tb.Enabled = true;
        }

        private string GetLocalIPv4()
        {
            try
            {
                using (Socket socket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, 0))
                {
                    socket.Connect("8.8.8.8", 80);
                    IPEndPoint endPoint = socket.LocalEndPoint as IPEndPoint;
                    return endPoint?.Address.ToString() ?? "127.0.0.1";
                }
            }
            catch
            {
                return "127.0.0.1";
            }
        }
        private void InitializeRefreshTimer()
        {
            _refreshTimer = new Timer();
            _refreshTimer.Interval = 2000; // 2 seconds
            _refreshTimer.Tick += RefreshTimer_Tick;
        }

        private void RefreshTimer_Tick(object sender, EventArgs e)
        {
            if (_pythonProcess == null || _pythonProcess.HasExited)
                return;

            if (isServerMode)
            {
                SendCommand($"LOADUSERS {serverIp_2_tb.Text} {tcpPort_2_tb.Text}");

                if (clients_2_cb.SelectedItem != null)
                {
                    string key = clients_2_cb.SelectedItem.ToString();
                    SendCommand($"SELECT {key}");
                }
            }
        }

        private Process _pythonProcess;
        private bool _updatingCombo = false;


        private void StyleActionButton(Button btn, Color backColor)
        {
            btn.FlatStyle = FlatStyle.Flat;
            btn.FlatAppearance.BorderSize = 0;
            btn.FlatAppearance.MouseOverBackColor = ControlPaint.Light(backColor);
            btn.FlatAppearance.MouseDownBackColor = ControlPaint.Dark(backColor);
            btn.BackColor = backColor;
            btn.ForeColor = Color.White;
            btn.Font = new Font("Segoe UI", 10F, FontStyle.Bold);
            btn.Cursor = Cursors.Hand;
            btn.Height = 36;
        }

        private void StyleControls(Control parent)
        {
            Color formBg = Color.FromArgb(245, 247, 250);
            Color cardBg = Color.White;
            Color inputBg = Color.FromArgb(250, 250, 252);
            Color textColor = Color.FromArgb(45, 45, 45);
            Color logBg = Color.FromArgb(248, 249, 251);

            foreach (Control ctrl in parent.Controls)
            {
                if (ctrl is GroupBox gb)
                {
                    gb.ForeColor = Color.FromArgb(55, 55, 55);
                    gb.Font = new Font("Segoe UI", 10F, FontStyle.Bold);
                    gb.BackColor = cardBg;
                    gb.Padding = new Padding(10);
                }
                else if (ctrl is Button btn)
                {
                    btn.FlatStyle = FlatStyle.Flat;
                    btn.FlatAppearance.BorderSize = 0;
                    btn.BackColor = Color.FromArgb(52, 120, 246);
                    btn.ForeColor = Color.White;
                    btn.Font = new Font("Segoe UI", 10F, FontStyle.Bold);
                    btn.Cursor = Cursors.Hand;
                    btn.Height = 36;
                }
                else if (ctrl is TextBox tb)
                {
                    tb.BorderStyle = BorderStyle.FixedSingle;
                    tb.BackColor = inputBg;
                    tb.ForeColor = textColor;
                    tb.Font = new Font("Segoe UI", 10F, FontStyle.Regular);
                }
                else if (ctrl is ComboBox cb)
                {
                    cb.FlatStyle = FlatStyle.Flat;
                    cb.BackColor = inputBg;
                    cb.ForeColor = textColor;
                    cb.Font = new Font("Segoe UI", 10F, FontStyle.Regular);
                }
                else if (ctrl is Label lbl)
                {
                    lbl.ForeColor = Color.FromArgb(60, 60, 60);
                    lbl.Font = new Font("Segoe UI", 10F, FontStyle.Regular);
                    lbl.BackColor = Color.Transparent;
                }
                else if (ctrl is RichTextBox rtb)
                {
                    rtb.BorderStyle = BorderStyle.FixedSingle;
                    rtb.BackColor = logBg;
                    rtb.ForeColor = Color.FromArgb(30, 30, 30);
                    rtb.Font = new Font("Consolas", 10F, FontStyle.Regular);
                }
                else if (ctrl is TabPage tp)
                {
                    tp.BackColor = formBg;
                }

                if (ctrl.HasChildren)
                    StyleControls(ctrl);
            }
        }

        private void StyleTitleLabel(Label lbl)
        {
            if (lbl == null) return;

            lbl.Font = new Font("Segoe UI", 22F, FontStyle.Bold);
            lbl.ForeColor = Color.FromArgb(25, 25, 25);
            lbl.BackColor = Color.Transparent;
        }

        private void ApplyModernTheme()
        {
            Color formBg = Color.FromArgb(245, 247, 250);
            Color textColor = Color.FromArgb(40, 40, 40);
            Color logBg = Color.FromArgb(248, 249, 251);

            // Form
            this.BackColor = formBg;
            this.Font = new Font("Segoe UI", 10F, FontStyle.Regular);
            this.ForeColor = textColor;
            this.StartPosition = FormStartPosition.CenterScreen;

            // Tabs
            tabPage1.Text = "Client";
            tabPage2.Text = "Server";

            tabPage1.BackColor = formBg;
            tabPage2.BackColor = formBg;

            main_tc.Appearance = TabAppearance.Normal;
            main_tc.SizeMode = TabSizeMode.Fixed;
            main_tc.ItemSize = new Size(120, 32);

            // Apply general control styling
            StyleControls(this);

            // Titles
            StyleTitleLabel(title_lb);
            StyleTitleLabel(title2_lb);

            // Buttons
           
            StyleActionButton(register_2_bt, Color.FromArgb(40, 167, 69));

         
            StyleActionButton(update_2_bt, Color.FromArgb(0, 123, 255));

           
            StyleActionButton(deRegister_2_bt, Color.FromArgb(220, 53, 69));

            StyleActionButton(publish_1_bt, Color.FromArgb(111, 66, 193));

            StyleActionButton(comment_1_bt, Color.FromArgb(245, 183, 0));
            comment_1_bt.ForeColor = Color.Black;

            // Feed boxes
            feed_1_rtb.ReadOnly = true;
            feed_1_rtb.BackColor = logBg;
            feed_1_rtb.ForeColor = Color.FromArgb(30, 30, 30);
            feed_1_rtb.Font = new Font("Consolas", 10F, FontStyle.Regular);
            feed_1_rtb.BorderStyle = BorderStyle.FixedSingle;

            debug_2_rtb.ReadOnly = true;
            debug_2_rtb.BackColor = logBg;
            debug_2_rtb.ForeColor = Color.FromArgb(30, 30, 30);
            debug_2_rtb.Font = new Font("Consolas", 10F, FontStyle.Regular);
            debug_2_rtb.BorderStyle = BorderStyle.FixedSingle;
        }

        public Form1(bool isServerMode, bool isServerA)
        {
            InitializeComponent();
            this.isServerMode = isServerMode;
            this.isServerA = isServerA;
            ApplyModernTheme();
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
            ip_1_tb.Text = GetLocalIPv4();

            ip_1_tb.ReadOnly = true;

            UnlockClientConnectionFields();



        }


        private void InitializeActiveSide()
        { 
            if (isServerMode)
            {
                    InitializeServerSide();
                    main_tc.TabPages.Remove(tabPage1);
                    serverIndication_lb.Text = "ACTIVE";
                    serverIndication_lb.ForeColor = Color.Green;
                    serverIndication_lb.Font = new Font("Segoe UI", 14F, FontStyle.Regular);
                   
                    

            }
               
                
            else
            {
                    InitializeClientSide();
                    main_tc.TabPages.Remove(tabPage2);
                    
                    clientIndication_lb.Text = "ACTIVE";
                    clientIndication_lb.ForeColor = Color.Green;
                    clientIndicatation_lb.Font = new Font("Segoe UI", 14F, FontStyle.Regular);
                    
            }
               

            if (_refreshTimer != null && !_refreshTimer.Enabled)
                _refreshTimer.Start();
        }
       
        private void Form1_Load(object sender, EventArgs e)
        {
            InitializeSubjects();
            InitializeRefreshTimer();
            StartPythonBridge();


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

            if (isServerMode)
                AppendIncoming("[PY-ERR] " + e.Data);
        }
        private void ApplyServerInit(string line)
        {
            string[] parts = line.Split('|');

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
            else if (line == "REGISTERED")
            {
                AppendIncoming(line);
                LockClientConnectionFields();
            }
            else if (line == "SUBJECTS-UPDATED")
            {
                AppendIncoming(line);
            }
            else if (line.StartsWith("REGISTER-DENIED|"))
            {
                AppendIncoming(line);
            }
            else if (line == "UPDATE-CONFIRMED")
            {
                AppendIncoming(line);
            }
            else if (line.StartsWith("UPDATE-DENIED|"))
            {
                AppendIncoming(line);
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
            {
                debug_2_rtb.AppendText(text + Environment.NewLine);
            }
            else
            {
                if (ShouldShowClientLine(text))
                    feed_1_rtb.AppendText(text + Environment.NewLine);
            }
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
        protected override void OnFormClosing(FormClosingEventArgs e)
        {
            try
            {
                if (_refreshTimer != null)
                    _refreshTimer.Stop();

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
        private void register_1_bt_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(name_1_tb.Text) ||
                string.IsNullOrWhiteSpace(ip_1_tb.Text) ||
                string.IsNullOrWhiteSpace(tcpPort_1_tb.Text) ||
                string.IsNullOrWhiteSpace(udpPort_1_tb.Text) ||
                string.IsNullOrWhiteSpace(serverIp_1_tb.Text) ||
                string.IsNullOrWhiteSpace(serverTcp_1_tb.Text))
            {
                MessageBox.Show("Fill all client connection fields first.");
                return;
            }

            string cmd =
                $"REGISTER {name_1_tb.Text} {ip_1_tb.Text} {tcpPort_1_tb.Text} {udpPort_1_tb.Text} {serverIp_1_tb.Text} {serverTcp_1_tb.Text}";
            SendCommand(cmd);
            register_1_bt.Visible = false;
            
        }
        private void updateSubjects_1_bt_Click(object sender, EventArgs e)
        {
            var selectedSubjects = subjects_1_clb.CheckedItems
                .Cast<object>()
                .Select(x => x.ToString())
                .ToList();

            if (selectedSubjects.Count == 0)
            {
                MessageBox.Show("Select at least one subject.");
                return;
            }

            string cmd = "SUBJECTS " + string.Join(" ", selectedSubjects);
            SendCommand(cmd);
        }

        private void publish_1_bt_Click(object sender, EventArgs e)
        {
            if (subject_1_cb.SelectedItem == null)
            {
                MessageBox.Show("Select a subject.");
                return;
            }

            if (string.IsNullOrWhiteSpace(title_1_tb.Text) ||
                string.IsNullOrWhiteSpace(text_1_tb.Text))
            {
                MessageBox.Show("Enter both title and text.");
                return;
            }

            string subject = subject_1_cb.SelectedItem.ToString();
            string title = title_1_tb.Text.Trim().Replace(" ", "_");
            string text = text_1_tb.Text.Trim().Replace(" ", "_");

            string cmd = $"PUBLISH {subject} {title} {text}";
            SendCommand(cmd);
            title_1_tb.Text = "";
            text_1_tb.Text = "";

        }

        private void comment_1_bt_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(comment_1_tb.Text))
            {
                MessageBox.Show("Enter a comment first.");
                return;
            }

            string text = comment_1_tb.Text.Trim().Replace(" ", "_");
            string cmd = $"COMMENT_LATEST {text}";
            SendCommand(cmd);
            comment_1_tb.Text = "";
        }


    }

}