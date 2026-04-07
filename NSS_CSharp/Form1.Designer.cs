using System;

namespace NSS
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.backgroundWorker1 = new System.ComponentModel.BackgroundWorker();
            this.main_tc = new System.Windows.Forms.TabControl();
            this.tabPage1 = new System.Windows.Forms.TabPage();
            this.title_lb = new System.Windows.Forms.Label();
            this.groupBox7 = new System.Windows.Forms.GroupBox();
            this.serverTcp_1_tb = new System.Windows.Forms.TextBox();
            this.label10 = new System.Windows.Forms.Label();
            this.serverIp_1_tb = new System.Windows.Forms.TextBox();
            this.label11 = new System.Windows.Forms.Label();
            this.udpPort_1_tb = new System.Windows.Forms.TextBox();
            this.label12 = new System.Windows.Forms.Label();
            this.tcpPort_1_tb = new System.Windows.Forms.TextBox();
            this.label13 = new System.Windows.Forms.Label();
            this.ip_1_tb = new System.Windows.Forms.TextBox();
            this.label14 = new System.Windows.Forms.Label();
            this.name_1_tb = new System.Windows.Forms.TextBox();
            this.label15 = new System.Windows.Forms.Label();
            this.groupBox5 = new System.Windows.Forms.GroupBox();
            this.publish_1_bt = new System.Windows.Forms.Button();
            this.text_1_tb = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.title_1_tb = new System.Windows.Forms.TextBox();
            this.label4 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.subject_1_cb = new System.Windows.Forms.ComboBox();
            this.groupBox4 = new System.Windows.Forms.GroupBox();
            this.feed_1_rtb = new System.Windows.Forms.RichTextBox();
            this.comment_1_bt = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.comment_1_tb = new System.Windows.Forms.TextBox();
            this.tabPage2 = new System.Windows.Forms.TabPage();
            this.clients_2_cb = new System.Windows.Forms.ComboBox();
            this.groupBox3 = new System.Windows.Forms.GroupBox();
            this.debug_2_rtb = new System.Windows.Forms.RichTextBox();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.update_2_bt = new System.Windows.Forms.Button();
            this.deRegister_2_bt = new System.Windows.Forms.Button();
            this.register_2_bt = new System.Windows.Forms.Button();
            this.serverTcp_2_tb = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.serverIp_2_tb = new System.Windows.Forms.TextBox();
            this.label6 = new System.Windows.Forms.Label();
            this.udpPort_2_tb = new System.Windows.Forms.TextBox();
            this.label7 = new System.Windows.Forms.Label();
            this.tcpPort_2_tb = new System.Windows.Forms.TextBox();
            this.label8 = new System.Windows.Forms.Label();
            this.ip_2_tb = new System.Windows.Forms.TextBox();
            this.label9 = new System.Windows.Forms.Label();
            this.name_2_tb = new System.Windows.Forms.TextBox();
            this.label16 = new System.Windows.Forms.Label();
            this.title2_lb = new System.Windows.Forms.Label();
            this.clientIndication_lb = new System.Windows.Forms.Label();
            this.clientIndicatation_lb = new System.Windows.Forms.Label();
            this.serverIndication_lb = new System.Windows.Forms.Label();
            this.main_tc.SuspendLayout();
            this.tabPage1.SuspendLayout();
            this.groupBox7.SuspendLayout();
            this.groupBox5.SuspendLayout();
            this.groupBox4.SuspendLayout();
            this.tabPage2.SuspendLayout();
            this.groupBox3.SuspendLayout();
            this.groupBox1.SuspendLayout();
            this.SuspendLayout();
            // 
            // main_tc
            // 
            this.main_tc.Controls.Add(this.tabPage1);
            this.main_tc.Controls.Add(this.tabPage2);
            this.main_tc.Location = new System.Drawing.Point(3, 2);
            this.main_tc.Name = "main_tc";
            this.main_tc.SelectedIndex = 0;
            this.main_tc.Size = new System.Drawing.Size(645, 673);
            this.main_tc.TabIndex = 4;
            // 
            // tabPage1
            // 
            this.tabPage1.Controls.Add(this.clientIndicatation_lb);
            this.tabPage1.Controls.Add(this.clientIndication_lb);
            this.tabPage1.Controls.Add(this.title_lb);
            this.tabPage1.Controls.Add(this.groupBox7);
            this.tabPage1.Controls.Add(this.groupBox5);
            this.tabPage1.Controls.Add(this.groupBox4);
            this.tabPage1.Location = new System.Drawing.Point(4, 22);
            this.tabPage1.Name = "tabPage1";
            this.tabPage1.Padding = new System.Windows.Forms.Padding(3);
            this.tabPage1.Size = new System.Drawing.Size(637, 647);
            this.tabPage1.TabIndex = 0;
            this.tabPage1.Text = "tabPage1";
            this.tabPage1.UseVisualStyleBackColor = true;
            // 
            // title_lb
            // 
            this.title_lb.AutoSize = true;
            this.title_lb.Font = new System.Drawing.Font("Microsoft Sans Serif", 20.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.title_lb.Location = new System.Drawing.Point(16, 15);
            this.title_lb.Name = "title_lb";
            this.title_lb.Size = new System.Drawing.Size(84, 31);
            this.title_lb.TabIndex = 6;
            this.title_lb.Text = "Client";
            // 
            // groupBox7
            // 
            this.groupBox7.Controls.Add(this.serverTcp_1_tb);
            this.groupBox7.Controls.Add(this.label10);
            this.groupBox7.Controls.Add(this.serverIp_1_tb);
            this.groupBox7.Controls.Add(this.label11);
            this.groupBox7.Controls.Add(this.udpPort_1_tb);
            this.groupBox7.Controls.Add(this.label12);
            this.groupBox7.Controls.Add(this.tcpPort_1_tb);
            this.groupBox7.Controls.Add(this.label13);
            this.groupBox7.Controls.Add(this.ip_1_tb);
            this.groupBox7.Controls.Add(this.label14);
            this.groupBox7.Controls.Add(this.name_1_tb);
            this.groupBox7.Controls.Add(this.label15);
            this.groupBox7.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.groupBox7.Location = new System.Drawing.Point(5, 67);
            this.groupBox7.Name = "groupBox7";
            this.groupBox7.Size = new System.Drawing.Size(625, 134);
            this.groupBox7.TabIndex = 5;
            this.groupBox7.TabStop = false;
            this.groupBox7.Text = "User Info / Connection";
            // 
            // serverTcp_1_tb
            // 
            this.serverTcp_1_tb.Location = new System.Drawing.Point(265, 88);
            this.serverTcp_1_tb.Name = "serverTcp_1_tb";
            this.serverTcp_1_tb.ReadOnly = true;
            this.serverTcp_1_tb.Size = new System.Drawing.Size(94, 22);
            this.serverTcp_1_tb.TabIndex = 11;
            // 
            // label10
            // 
            this.label10.AutoSize = true;
            this.label10.Location = new System.Drawing.Point(179, 91);
            this.label10.Name = "label10";
            this.label10.Size = new System.Drawing.Size(80, 16);
            this.label10.TabIndex = 10;
            this.label10.Text = "Server TCP:";
            // 
            // serverIp_1_tb
            // 
            this.serverIp_1_tb.Location = new System.Drawing.Point(76, 85);
            this.serverIp_1_tb.Name = "serverIp_1_tb";
            this.serverIp_1_tb.ReadOnly = true;
            this.serverIp_1_tb.Size = new System.Drawing.Size(94, 22);
            this.serverIp_1_tb.TabIndex = 9;
            // 
            // label11
            // 
            this.label11.AutoSize = true;
            this.label11.Location = new System.Drawing.Point(6, 88);
            this.label11.Name = "label11";
            this.label11.Size = new System.Drawing.Size(65, 16);
            this.label11.TabIndex = 8;
            this.label11.Text = "Server IP:";
            // 
            // udpPort_1_tb
            // 
            this.udpPort_1_tb.Location = new System.Drawing.Point(265, 55);
            this.udpPort_1_tb.Name = "udpPort_1_tb";
            this.udpPort_1_tb.ReadOnly = true;
            this.udpPort_1_tb.Size = new System.Drawing.Size(94, 22);
            this.udpPort_1_tb.TabIndex = 7;
            // 
            // label12
            // 
            this.label12.AutoSize = true;
            this.label12.Location = new System.Drawing.Point(179, 58);
            this.label12.Name = "label12";
            this.label12.Size = new System.Drawing.Size(66, 16);
            this.label12.TabIndex = 6;
            this.label12.Text = "UDP Port:";
            // 
            // tcpPort_1_tb
            // 
            this.tcpPort_1_tb.Location = new System.Drawing.Point(76, 55);
            this.tcpPort_1_tb.Name = "tcpPort_1_tb";
            this.tcpPort_1_tb.ReadOnly = true;
            this.tcpPort_1_tb.Size = new System.Drawing.Size(94, 22);
            this.tcpPort_1_tb.TabIndex = 5;
            // 
            // label13
            // 
            this.label13.AutoSize = true;
            this.label13.Location = new System.Drawing.Point(6, 58);
            this.label13.Name = "label13";
            this.label13.Size = new System.Drawing.Size(64, 16);
            this.label13.TabIndex = 4;
            this.label13.Text = "TCP Port:";
            // 
            // ip_1_tb
            // 
            this.ip_1_tb.Location = new System.Drawing.Point(265, 25);
            this.ip_1_tb.Name = "ip_1_tb";
            this.ip_1_tb.ReadOnly = true;
            this.ip_1_tb.Size = new System.Drawing.Size(94, 22);
            this.ip_1_tb.TabIndex = 3;
            // 
            // label14
            // 
            this.label14.AutoSize = true;
            this.label14.Location = new System.Drawing.Point(179, 31);
            this.label14.Name = "label14";
            this.label14.Size = new System.Drawing.Size(22, 16);
            this.label14.TabIndex = 2;
            this.label14.Text = "IP:";
            // 
            // name_1_tb
            // 
            this.name_1_tb.Location = new System.Drawing.Point(76, 27);
            this.name_1_tb.Name = "name_1_tb";
            this.name_1_tb.ReadOnly = true;
            this.name_1_tb.Size = new System.Drawing.Size(94, 22);
            this.name_1_tb.TabIndex = 1;
            // 
            // label15
            // 
            this.label15.AutoSize = true;
            this.label15.Location = new System.Drawing.Point(8, 33);
            this.label15.Name = "label15";
            this.label15.Size = new System.Drawing.Size(47, 16);
            this.label15.TabIndex = 0;
            this.label15.Text = "Name:";
            // 
            // groupBox5
            // 
            this.groupBox5.Controls.Add(this.publish_1_bt);
            this.groupBox5.Controls.Add(this.text_1_tb);
            this.groupBox5.Controls.Add(this.label3);
            this.groupBox5.Controls.Add(this.title_1_tb);
            this.groupBox5.Controls.Add(this.label4);
            this.groupBox5.Controls.Add(this.label5);
            this.groupBox5.Controls.Add(this.subject_1_cb);
            this.groupBox5.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.groupBox5.Location = new System.Drawing.Point(3, 225);
            this.groupBox5.Name = "groupBox5";
            this.groupBox5.Size = new System.Drawing.Size(625, 134);
            this.groupBox5.TabIndex = 3;
            this.groupBox5.TabStop = false;
            this.groupBox5.Text = "Publish News";
            // 
            // publish_1_bt
            // 
            this.publish_1_bt.Location = new System.Drawing.Point(395, 26);
            this.publish_1_bt.Name = "publish_1_bt";
            this.publish_1_bt.Size = new System.Drawing.Size(92, 30);
            this.publish_1_bt.TabIndex = 14;
            this.publish_1_bt.Text = "Publish";
            this.publish_1_bt.UseVisualStyleBackColor = true;
            // 
            // text_1_tb
            // 
            this.text_1_tb.Location = new System.Drawing.Point(76, 89);
            this.text_1_tb.Multiline = true;
            this.text_1_tb.Name = "text_1_tb";
            this.text_1_tb.Size = new System.Drawing.Size(526, 22);
            this.text_1_tb.TabIndex = 8;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(17, 89);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(36, 16);
            this.label3.TabIndex = 7;
            this.label3.Text = "Text:";
            // 
            // title_1_tb
            // 
            this.title_1_tb.Location = new System.Drawing.Point(76, 53);
            this.title_1_tb.Name = "title_1_tb";
            this.title_1_tb.Size = new System.Drawing.Size(121, 22);
            this.title_1_tb.TabIndex = 6;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(15, 56);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(36, 16);
            this.label4.TabIndex = 2;
            this.label4.Text = "Title:";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(15, 26);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(55, 16);
            this.label5.TabIndex = 1;
            this.label5.Text = "Subject:";
            // 
            // subject_1_cb
            // 
            this.subject_1_cb.FormattingEnabled = true;
            this.subject_1_cb.Location = new System.Drawing.Point(76, 23);
            this.subject_1_cb.Name = "subject_1_cb";
            this.subject_1_cb.Size = new System.Drawing.Size(121, 24);
            this.subject_1_cb.TabIndex = 0;
            // 
            // groupBox4
            // 
            this.groupBox4.Controls.Add(this.feed_1_rtb);
            this.groupBox4.Controls.Add(this.comment_1_bt);
            this.groupBox4.Controls.Add(this.label2);
            this.groupBox4.Controls.Add(this.comment_1_tb);
            this.groupBox4.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.groupBox4.Location = new System.Drawing.Point(3, 384);
            this.groupBox4.Name = "groupBox4";
            this.groupBox4.Size = new System.Drawing.Size(625, 255);
            this.groupBox4.TabIndex = 2;
            this.groupBox4.TabStop = false;
            this.groupBox4.Text = "Incoming Feed / Messages";
            // 
            // feed_1_rtb
            // 
            this.feed_1_rtb.Location = new System.Drawing.Point(3, 18);
            this.feed_1_rtb.Name = "feed_1_rtb";
            this.feed_1_rtb.Size = new System.Drawing.Size(616, 162);
            this.feed_1_rtb.TabIndex = 16;
            this.feed_1_rtb.Text = "";
            // 
            // comment_1_bt
            // 
            this.comment_1_bt.Location = new System.Drawing.Point(526, 186);
            this.comment_1_bt.Name = "comment_1_bt";
            this.comment_1_bt.Size = new System.Drawing.Size(93, 26);
            this.comment_1_bt.TabIndex = 15;
            this.comment_1_bt.Text = "Comment";
            this.comment_1_bt.UseVisualStyleBackColor = true;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(6, 191);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(67, 16);
            this.label2.TabIndex = 8;
            this.label2.Text = "Comment:";
            // 
            // comment_1_tb
            // 
            this.comment_1_tb.Location = new System.Drawing.Point(79, 188);
            this.comment_1_tb.Multiline = true;
            this.comment_1_tb.Name = "comment_1_tb";
            this.comment_1_tb.Size = new System.Drawing.Size(437, 24);
            this.comment_1_tb.TabIndex = 1;
            // 
            // tabPage2
            // 
            this.tabPage2.Controls.Add(this.serverIndication_lb);
            this.tabPage2.Controls.Add(this.clients_2_cb);
            this.tabPage2.Controls.Add(this.groupBox3);
            this.tabPage2.Controls.Add(this.groupBox1);
            this.tabPage2.Controls.Add(this.title2_lb);
            this.tabPage2.Location = new System.Drawing.Point(4, 22);
            this.tabPage2.Name = "tabPage2";
            this.tabPage2.Padding = new System.Windows.Forms.Padding(3);
            this.tabPage2.Size = new System.Drawing.Size(637, 647);
            this.tabPage2.TabIndex = 1;
            this.tabPage2.Text = "tabPage2";
            this.tabPage2.UseVisualStyleBackColor = true;
            // 
            // clients_2_cb
            // 
            this.clients_2_cb.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.clients_2_cb.FormattingEnabled = true;
            this.clients_2_cb.Location = new System.Drawing.Point(131, 23);
            this.clients_2_cb.Name = "clients_2_cb";
            this.clients_2_cb.Size = new System.Drawing.Size(188, 21);
            this.clients_2_cb.TabIndex = 11;
            this.clients_2_cb.SelectedIndexChanged += new System.EventHandler(this.clients_2_cb_SelectedIndexChanged);
            // 
            // groupBox3
            // 
            this.groupBox3.Controls.Add(this.debug_2_rtb);
            this.groupBox3.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.groupBox3.Location = new System.Drawing.Point(3, 375);
            this.groupBox3.Name = "groupBox3";
            this.groupBox3.Size = new System.Drawing.Size(625, 183);
            this.groupBox3.TabIndex = 10;
            this.groupBox3.TabStop = false;
            this.groupBox3.Text = "Debug / Server Communication";
            // 
            // debug_2_rtb
            // 
            this.debug_2_rtb.Location = new System.Drawing.Point(3, 18);
            this.debug_2_rtb.Name = "debug_2_rtb";
            this.debug_2_rtb.Size = new System.Drawing.Size(616, 159);
            this.debug_2_rtb.TabIndex = 16;
            this.debug_2_rtb.Text = "";
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.update_2_bt);
            this.groupBox1.Controls.Add(this.deRegister_2_bt);
            this.groupBox1.Controls.Add(this.register_2_bt);
            this.groupBox1.Controls.Add(this.serverTcp_2_tb);
            this.groupBox1.Controls.Add(this.label1);
            this.groupBox1.Controls.Add(this.serverIp_2_tb);
            this.groupBox1.Controls.Add(this.label6);
            this.groupBox1.Controls.Add(this.udpPort_2_tb);
            this.groupBox1.Controls.Add(this.label7);
            this.groupBox1.Controls.Add(this.tcpPort_2_tb);
            this.groupBox1.Controls.Add(this.label8);
            this.groupBox1.Controls.Add(this.ip_2_tb);
            this.groupBox1.Controls.Add(this.label9);
            this.groupBox1.Controls.Add(this.name_2_tb);
            this.groupBox1.Controls.Add(this.label16);
            this.groupBox1.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.groupBox1.Location = new System.Drawing.Point(3, 64);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(625, 134);
            this.groupBox1.TabIndex = 8;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "User Info / Connection";
            // 
            // update_2_bt
            // 
            this.update_2_bt.Location = new System.Drawing.Point(516, 74);
            this.update_2_bt.Name = "update_2_bt";
            this.update_2_bt.Size = new System.Drawing.Size(86, 30);
            this.update_2_bt.TabIndex = 14;
            this.update_2_bt.Text = "Update";
            this.update_2_bt.UseVisualStyleBackColor = true;
            // 
            // deRegister_2_bt
            // 
            this.deRegister_2_bt.Location = new System.Drawing.Point(395, 74);
            this.deRegister_2_bt.Name = "deRegister_2_bt";
            this.deRegister_2_bt.Size = new System.Drawing.Size(92, 30);
            this.deRegister_2_bt.TabIndex = 13;
            this.deRegister_2_bt.Text = "De-Register";
            this.deRegister_2_bt.UseVisualStyleBackColor = true;
            // 
            // register_2_bt
            // 
            this.register_2_bt.Location = new System.Drawing.Point(452, 25);
            this.register_2_bt.Name = "register_2_bt";
            this.register_2_bt.Size = new System.Drawing.Size(86, 30);
            this.register_2_bt.TabIndex = 12;
            this.register_2_bt.Text = "Register";
            this.register_2_bt.UseVisualStyleBackColor = true;
            // 
            // serverTcp_2_tb
            // 
            this.serverTcp_2_tb.Location = new System.Drawing.Point(265, 88);
            this.serverTcp_2_tb.Name = "serverTcp_2_tb";
            this.serverTcp_2_tb.ReadOnly = true;
            this.serverTcp_2_tb.Size = new System.Drawing.Size(94, 22);
            this.serverTcp_2_tb.TabIndex = 11;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(179, 91);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(80, 16);
            this.label1.TabIndex = 10;
            this.label1.Text = "Server TCP:";
            // 
            // serverIp_2_tb
            // 
            this.serverIp_2_tb.Location = new System.Drawing.Point(76, 85);
            this.serverIp_2_tb.Name = "serverIp_2_tb";
            this.serverIp_2_tb.ReadOnly = true;
            this.serverIp_2_tb.Size = new System.Drawing.Size(94, 22);
            this.serverIp_2_tb.TabIndex = 9;
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(6, 88);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(65, 16);
            this.label6.TabIndex = 8;
            this.label6.Text = "Server IP:";
            // 
            // udpPort_2_tb
            // 
            this.udpPort_2_tb.Location = new System.Drawing.Point(265, 55);
            this.udpPort_2_tb.Name = "udpPort_2_tb";
            this.udpPort_2_tb.ReadOnly = true;
            this.udpPort_2_tb.Size = new System.Drawing.Size(94, 22);
            this.udpPort_2_tb.TabIndex = 7;
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(179, 58);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(66, 16);
            this.label7.TabIndex = 6;
            this.label7.Text = "UDP Port:";
            // 
            // tcpPort_2_tb
            // 
            this.tcpPort_2_tb.Location = new System.Drawing.Point(76, 55);
            this.tcpPort_2_tb.Name = "tcpPort_2_tb";
            this.tcpPort_2_tb.ReadOnly = true;
            this.tcpPort_2_tb.Size = new System.Drawing.Size(94, 22);
            this.tcpPort_2_tb.TabIndex = 5;
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Location = new System.Drawing.Point(6, 58);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(64, 16);
            this.label8.TabIndex = 4;
            this.label8.Text = "TCP Port:";
            // 
            // ip_2_tb
            // 
            this.ip_2_tb.Enabled = false;
            this.ip_2_tb.Location = new System.Drawing.Point(265, 25);
            this.ip_2_tb.Name = "ip_2_tb";
            this.ip_2_tb.ReadOnly = true;
            this.ip_2_tb.Size = new System.Drawing.Size(94, 22);
            this.ip_2_tb.TabIndex = 3;
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.Location = new System.Drawing.Point(179, 25);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(22, 16);
            this.label9.TabIndex = 2;
            this.label9.Text = "IP:";
            // 
            // name_2_tb
            // 
            this.name_2_tb.Location = new System.Drawing.Point(76, 22);
            this.name_2_tb.Name = "name_2_tb";
            this.name_2_tb.ReadOnly = true;
            this.name_2_tb.Size = new System.Drawing.Size(94, 22);
            this.name_2_tb.TabIndex = 1;
            // 
            // label16
            // 
            this.label16.AutoSize = true;
            this.label16.Location = new System.Drawing.Point(6, 25);
            this.label16.Name = "label16";
            this.label16.Size = new System.Drawing.Size(47, 16);
            this.label16.TabIndex = 0;
            this.label16.Text = "Name:";
            // 
            // title2_lb
            // 
            this.title2_lb.AutoSize = true;
            this.title2_lb.Font = new System.Drawing.Font("Microsoft Sans Serif", 20.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.title2_lb.Location = new System.Drawing.Point(16, 16);
            this.title2_lb.Name = "title2_lb";
            this.title2_lb.Size = new System.Drawing.Size(94, 31);
            this.title2_lb.TabIndex = 7;
            this.title2_lb.Text = "Server";
            // 
            // clientIndication_lb
            // 
            this.clientIndication_lb.AutoSize = true;
            this.clientIndication_lb.Font = new System.Drawing.Font("Microsoft Sans Serif", 14.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.clientIndication_lb.Location = new System.Drawing.Point(449, 15);
            this.clientIndication_lb.Name = "clientIndication_lb";
            this.clientIndication_lb.Size = new System.Drawing.Size(61, 24);
            this.clientIndication_lb.TabIndex = 7;
            this.clientIndication_lb.Text = "Active";
            // 
            // clientIndicatation_lb
            // 
            this.clientIndicatation_lb.AutoSize = true;
            this.clientIndicatation_lb.Location = new System.Drawing.Point(424, 8);
            this.clientIndicatation_lb.Name = "clientIndicatation_lb";
            this.clientIndicatation_lb.Size = new System.Drawing.Size(0, 13);
            this.clientIndicatation_lb.TabIndex = 8;
            // 
            // serverIndication_lb
            // 
            this.serverIndication_lb.AutoSize = true;
            this.serverIndication_lb.Font = new System.Drawing.Font("Microsoft Sans Serif", 14.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.serverIndication_lb.Location = new System.Drawing.Point(516, 16);
            this.serverIndication_lb.Name = "serverIndication_lb";
            this.serverIndication_lb.Size = new System.Drawing.Size(61, 24);
            this.serverIndication_lb.TabIndex = 12;
            this.serverIndication_lb.Text = "Active";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(649, 675);
            this.Controls.Add(this.main_tc);
            this.Name = "Form1";
            this.Text = "NSS";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.main_tc.ResumeLayout(false);
            this.tabPage1.ResumeLayout(false);
            this.tabPage1.PerformLayout();
            this.groupBox7.ResumeLayout(false);
            this.groupBox7.PerformLayout();
            this.groupBox5.ResumeLayout(false);
            this.groupBox5.PerformLayout();
            this.groupBox4.ResumeLayout(false);
            this.groupBox4.PerformLayout();
            this.tabPage2.ResumeLayout(false);
            this.tabPage2.PerformLayout();
            this.groupBox3.ResumeLayout(false);
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.ResumeLayout(false);

        }

        private void label1_Click_1(object sender, EventArgs e)
        {
           
        }

        private void groupBox1_Enter(object sender, EventArgs e)
        {
            
        }

        private void name_1_tb_TextChanged(object sender, EventArgs e)
        {
           
        }

        private void ip_1_lb_Click(object sender, EventArgs e)
        {
            
        }

        private void checkedListBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            
        }

        #endregion
        private System.ComponentModel.BackgroundWorker backgroundWorker1;
        private System.Windows.Forms.TabControl main_tc;
        private System.Windows.Forms.TabPage tabPage1;
        private System.Windows.Forms.GroupBox groupBox7;
        private System.Windows.Forms.TextBox serverTcp_1_tb;
        private System.Windows.Forms.Label label10;
        private System.Windows.Forms.TextBox serverIp_1_tb;
        private System.Windows.Forms.Label label11;
        private System.Windows.Forms.TextBox udpPort_1_tb;
        private System.Windows.Forms.Label label12;
        private System.Windows.Forms.TextBox tcpPort_1_tb;
        private System.Windows.Forms.Label label13;
        private System.Windows.Forms.TextBox ip_1_tb;
        private System.Windows.Forms.Label label14;
        private System.Windows.Forms.TextBox name_1_tb;
        private System.Windows.Forms.Label label15;
        private System.Windows.Forms.GroupBox groupBox5;
        private System.Windows.Forms.Button publish_1_bt;
        private System.Windows.Forms.TextBox text_1_tb;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox title_1_tb;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.ComboBox subject_1_cb;
        private System.Windows.Forms.GroupBox groupBox4;
        private System.Windows.Forms.RichTextBox feed_1_rtb;
        private System.Windows.Forms.Button comment_1_bt;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox comment_1_tb;
        private System.Windows.Forms.TabPage tabPage2;
        private System.Windows.Forms.Label title_lb;
        private System.Windows.Forms.Label title2_lb;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.Button update_2_bt;
        private System.Windows.Forms.Button deRegister_2_bt;
        private System.Windows.Forms.Button register_2_bt;
        private System.Windows.Forms.TextBox serverTcp_2_tb;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox serverIp_2_tb;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.TextBox udpPort_2_tb;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.TextBox tcpPort_2_tb;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.TextBox ip_2_tb;
        private System.Windows.Forms.Label label9;
        private System.Windows.Forms.TextBox name_2_tb;
        private System.Windows.Forms.Label label16;
        private System.Windows.Forms.GroupBox groupBox3;
        private System.Windows.Forms.RichTextBox debug_2_rtb;
        private System.Windows.Forms.ComboBox clients_2_cb;
        private System.Windows.Forms.Label clientIndicatation_lb;
        private System.Windows.Forms.Label clientIndication_lb;
        private System.Windows.Forms.Label serverIndication_lb;
    }
}

