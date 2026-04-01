using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml.Linq;



namespace NSS
{
  
    public partial class Form1 : Form
    {
        Process pyProcess;
        StreamWriter pyInput;
        StreamReader pyOutput;
        public Form1()
        {
            InitializeComponent();
        }

        private void groupBox1_Enter(object sender, EventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void ip_1_lb_Click(object sender, EventArgs e)
        {

        }

        private void checkedListBox1_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void label1_Click_1(object sender, EventArgs e)
        {

        }

        private void Form1_Load(object sender, EventArgs e)
        {
            StartPython();
        }
        private void StartPython()
        {
            try
            {
                string pythonExe = @""; // change it to pyhton.exe find python exe using which pyhton
                string pythonScript = @"..\..\client_app.py";
                string pythonWorkDir = @"..\";

                pyProcess = new Process();
                pyProcess.StartInfo.FileName = pythonExe;
                pyProcess.StartInfo.Arguments = $"\"{pythonScript}\"";
                pyProcess.StartInfo.WorkingDirectory = pythonWorkDir;
                pyProcess.StartInfo.UseShellExecute = false;
                pyProcess.StartInfo.RedirectStandardInput = true;
                pyProcess.StartInfo.RedirectStandardOutput = true;
                pyProcess.StartInfo.RedirectStandardError = true;
                pyProcess.StartInfo.CreateNoWindow = true;

                pyProcess.Start();

                pyInput = pyProcess.StandardInput;
                pyOutput = pyProcess.StandardOutput;

                string ready = pyOutput.ReadLine();
                MessageBox.Show(ready ?? "No response from Python process.");

                if (pyProcess.HasExited)
                {
                    string err = pyProcess.StandardError.ReadToEnd();
                    MessageBox.Show("Python exited early:\n" + err);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Failed to start Python:\n" + ex.Message);
            }
        }

   

       private async void register_1_bt_Click(object sender, EventArgs e)
        {
            DrainPythonOutput();

            string cmd = $"REGISTER {name_1_tb.Text} {ip_1_tb.Text} {tcp_1_tb.Text} {udp_1_tb.Text} {server_1_tb.Text} {servertcp_1_tb.Text}";

            pyInput.WriteLine(cmd);

            string response = await Task.Run(() => pyOutput.ReadLine());

            MessageBox.Show(response);
        }

        private void name_1_tb_TextChanged(object sender, EventArgs e)
        {

        }

        private void DrainPythonOutput()
        {
            while (pyProcess != null && !pyProcess.HasExited && pyOutput.Peek() > -1)
            {
                pyOutput.ReadLine();
            }
        }

    }
}
