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
            this.connection_info_gp = new System.Windows.Forms.GroupBox();
            this.update_1_bt = new System.Windows.Forms.Button();
            this.deregister_1_bt = new System.Windows.Forms.Button();
            this.register_1_bt = new System.Windows.Forms.Button();
            this.servertcp_1_tb = new System.Windows.Forms.TextBox();
            this.servertcp_1_lb = new System.Windows.Forms.Label();
            this.server_1_tb = new System.Windows.Forms.TextBox();
            this.server_1_lb = new System.Windows.Forms.Label();
            this.udp_1_tb = new System.Windows.Forms.TextBox();
            this.udp_1_lb = new System.Windows.Forms.Label();
            this.tcp_1_tb = new System.Windows.Forms.TextBox();
            this.tcp_1_lb = new System.Windows.Forms.Label();
            this.ip_1_tb = new System.Windows.Forms.TextBox();
            this.ip_1_lb = new System.Windows.Forms.Label();
            this.name_1_tb = new System.Windows.Forms.TextBox();
            this.name_1_lb = new System.Windows.Forms.Label();
            this.backgroundWorker1 = new System.ComponentModel.BackgroundWorker();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.updatesubjects_2_btn = new System.Windows.Forms.Button();
            this.checkedListBox1 = new System.Windows.Forms.CheckedListBox();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.publish_2_bt = new System.Windows.Forms.Button();
            this.textBox1 = new System.Windows.Forms.TextBox();
            this.text_2_tb = new System.Windows.Forms.Label();
            this.title_2_tb = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.subject_2_lb = new System.Windows.Forms.Label();
            this.subject_2_cb = new System.Windows.Forms.ComboBox();
            this.groupBox3 = new System.Windows.Forms.GroupBox();
            this.comment_3_bt = new System.Windows.Forms.Button();
            this.comment_3_lb = new System.Windows.Forms.Label();
            this.textBox2 = new System.Windows.Forms.TextBox();
            this.incoming_3_ltb = new System.Windows.Forms.ListBox();
            this.title_lb = new System.Windows.Forms.Label();
            this.connection_info_gp.SuspendLayout();
            this.groupBox1.SuspendLayout();
            this.groupBox2.SuspendLayout();
            this.groupBox3.SuspendLayout();
            this.SuspendLayout();
            // 
            // connection_info_gp
            // 
            this.connection_info_gp.Controls.Add(this.update_1_bt);
            this.connection_info_gp.Controls.Add(this.deregister_1_bt);
            this.connection_info_gp.Controls.Add(this.register_1_bt);
            this.connection_info_gp.Controls.Add(this.servertcp_1_tb);
            this.connection_info_gp.Controls.Add(this.servertcp_1_lb);
            this.connection_info_gp.Controls.Add(this.server_1_tb);
            this.connection_info_gp.Controls.Add(this.server_1_lb);
            this.connection_info_gp.Controls.Add(this.udp_1_tb);
            this.connection_info_gp.Controls.Add(this.udp_1_lb);
            this.connection_info_gp.Controls.Add(this.tcp_1_tb);
            this.connection_info_gp.Controls.Add(this.tcp_1_lb);
            this.connection_info_gp.Controls.Add(this.ip_1_tb);
            this.connection_info_gp.Controls.Add(this.ip_1_lb);
            this.connection_info_gp.Controls.Add(this.name_1_tb);
            this.connection_info_gp.Controls.Add(this.name_1_lb);
            this.connection_info_gp.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.connection_info_gp.Location = new System.Drawing.Point(12, 60);
            this.connection_info_gp.Name = "connection_info_gp";
            this.connection_info_gp.Size = new System.Drawing.Size(625, 134);
            this.connection_info_gp.TabIndex = 0;
            this.connection_info_gp.TabStop = false;
            this.connection_info_gp.Text = "User Info / Connection";
            this.connection_info_gp.Enter += new System.EventHandler(this.groupBox1_Enter);
            // 
            // update_1_bt
            // 
            this.update_1_bt.Location = new System.Drawing.Point(516, 74);
            this.update_1_bt.Name = "update_1_bt";
            this.update_1_bt.Size = new System.Drawing.Size(86, 30);
            this.update_1_bt.TabIndex = 14;
            this.update_1_bt.Text = "Update";
            this.update_1_bt.UseVisualStyleBackColor = true;
            // 
            // deregister_1_bt
            // 
            this.deregister_1_bt.Location = new System.Drawing.Point(395, 74);
            this.deregister_1_bt.Name = "deregister_1_bt";
            this.deregister_1_bt.Size = new System.Drawing.Size(92, 30);
            this.deregister_1_bt.TabIndex = 13;
            this.deregister_1_bt.Text = "De-Register";
            this.deregister_1_bt.UseVisualStyleBackColor = true;
            // 
            // register_1_bt
            // 
            this.register_1_bt.Location = new System.Drawing.Point(452, 25);
            this.register_1_bt.Name = "register_1_bt";
            this.register_1_bt.Size = new System.Drawing.Size(86, 30);
            this.register_1_bt.TabIndex = 12;
            this.register_1_bt.Text = "Register";
            this.register_1_bt.UseVisualStyleBackColor = true;
            this.register_1_bt.Click += new System.EventHandler(this.register_1_bt_Click);
            // 
            // servertcp_1_tb
            // 
            this.servertcp_1_tb.Location = new System.Drawing.Point(265, 88);
            this.servertcp_1_tb.Name = "servertcp_1_tb";
            this.servertcp_1_tb.Size = new System.Drawing.Size(94, 22);
            this.servertcp_1_tb.TabIndex = 11;
            // 
            // servertcp_1_lb
            // 
            this.servertcp_1_lb.AutoSize = true;
            this.servertcp_1_lb.Location = new System.Drawing.Point(179, 91);
            this.servertcp_1_lb.Name = "servertcp_1_lb";
            this.servertcp_1_lb.Size = new System.Drawing.Size(80, 16);
            this.servertcp_1_lb.TabIndex = 10;
            this.servertcp_1_lb.Text = "Server TCP:";
            // 
            // server_1_tb
            // 
            this.server_1_tb.Location = new System.Drawing.Point(76, 85);
            this.server_1_tb.Name = "server_1_tb";
            this.server_1_tb.Size = new System.Drawing.Size(94, 22);
            this.server_1_tb.TabIndex = 9;
            // 
            // server_1_lb
            // 
            this.server_1_lb.AutoSize = true;
            this.server_1_lb.Location = new System.Drawing.Point(6, 88);
            this.server_1_lb.Name = "server_1_lb";
            this.server_1_lb.Size = new System.Drawing.Size(65, 16);
            this.server_1_lb.TabIndex = 8;
            this.server_1_lb.Text = "Server IP:";
            // 
            // udp_1_tb
            // 
            this.udp_1_tb.Location = new System.Drawing.Point(265, 52);
            this.udp_1_tb.Name = "udp_1_tb";
            this.udp_1_tb.Size = new System.Drawing.Size(94, 22);
            this.udp_1_tb.TabIndex = 7;
            // 
            // udp_1_lb
            // 
            this.udp_1_lb.AutoSize = true;
            this.udp_1_lb.Location = new System.Drawing.Point(179, 58);
            this.udp_1_lb.Name = "udp_1_lb";
            this.udp_1_lb.Size = new System.Drawing.Size(66, 16);
            this.udp_1_lb.TabIndex = 6;
            this.udp_1_lb.Text = "UDP Port:";
            // 
            // tcp_1_tb
            // 
            this.tcp_1_tb.Location = new System.Drawing.Point(76, 55);
            this.tcp_1_tb.Name = "tcp_1_tb";
            this.tcp_1_tb.Size = new System.Drawing.Size(94, 22);
            this.tcp_1_tb.TabIndex = 5;
            // 
            // tcp_1_lb
            // 
            this.tcp_1_lb.AutoSize = true;
            this.tcp_1_lb.Location = new System.Drawing.Point(6, 58);
            this.tcp_1_lb.Name = "tcp_1_lb";
            this.tcp_1_lb.Size = new System.Drawing.Size(64, 16);
            this.tcp_1_lb.TabIndex = 4;
            this.tcp_1_lb.Text = "TCP Port:";
            // 
            // ip_1_tb
            // 
            this.ip_1_tb.Location = new System.Drawing.Point(265, 24);
            this.ip_1_tb.Name = "ip_1_tb";
            this.ip_1_tb.Size = new System.Drawing.Size(94, 22);
            this.ip_1_tb.TabIndex = 3;
            // 
            // ip_1_lb
            // 
            this.ip_1_lb.AutoSize = true;
            this.ip_1_lb.Location = new System.Drawing.Point(179, 25);
            this.ip_1_lb.Name = "ip_1_lb";
            this.ip_1_lb.Size = new System.Drawing.Size(22, 16);
            this.ip_1_lb.TabIndex = 2;
            this.ip_1_lb.Text = "IP:";
            this.ip_1_lb.Click += new System.EventHandler(this.ip_1_lb_Click);
            // 
            // name_1_tb
            // 
            this.name_1_tb.Location = new System.Drawing.Point(76, 22);
            this.name_1_tb.Name = "name_1_tb";
            this.name_1_tb.Size = new System.Drawing.Size(94, 22);
            this.name_1_tb.TabIndex = 1;
            this.name_1_tb.TextChanged += new System.EventHandler(this.name_1_tb_TextChanged);
            // 
            // name_1_lb
            // 
            this.name_1_lb.AutoSize = true;
            this.name_1_lb.Location = new System.Drawing.Point(6, 25);
            this.name_1_lb.Name = "name_1_lb";
            this.name_1_lb.Size = new System.Drawing.Size(47, 16);
            this.name_1_lb.TabIndex = 0;
            this.name_1_lb.Text = "Name:";
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.updatesubjects_2_btn);
            this.groupBox1.Controls.Add(this.checkedListBox1);
            this.groupBox1.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.groupBox1.Location = new System.Drawing.Point(12, 200);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(625, 134);
            this.groupBox1.TabIndex = 1;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Subjects";
            // 
            // updatesubjects_2_btn
            // 
            this.updatesubjects_2_btn.Location = new System.Drawing.Point(214, 44);
            this.updatesubjects_2_btn.Name = "updatesubjects_2_btn";
            this.updatesubjects_2_btn.Size = new System.Drawing.Size(116, 30);
            this.updatesubjects_2_btn.TabIndex = 14;
            this.updatesubjects_2_btn.Text = "Update Subjects";
            this.updatesubjects_2_btn.UseVisualStyleBackColor = true;
            // 
            // checkedListBox1
            // 
            this.checkedListBox1.FormattingEnabled = true;
            this.checkedListBox1.Items.AddRange(new object[] {
            "Sports",
            "Entertainment",
            "Health",
            "Health",
            "Science",
            "Politics",
            "Business",
            "                                                     "});
            this.checkedListBox1.Location = new System.Drawing.Point(9, 21);
            this.checkedListBox1.Name = "checkedListBox1";
            this.checkedListBox1.Size = new System.Drawing.Size(180, 89);
            this.checkedListBox1.TabIndex = 0;
            this.checkedListBox1.SelectedIndexChanged += new System.EventHandler(this.checkedListBox1_SelectedIndexChanged);
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.publish_2_bt);
            this.groupBox2.Controls.Add(this.textBox1);
            this.groupBox2.Controls.Add(this.text_2_tb);
            this.groupBox2.Controls.Add(this.title_2_tb);
            this.groupBox2.Controls.Add(this.label1);
            this.groupBox2.Controls.Add(this.subject_2_lb);
            this.groupBox2.Controls.Add(this.subject_2_cb);
            this.groupBox2.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.groupBox2.Location = new System.Drawing.Point(12, 340);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(625, 134);
            this.groupBox2.TabIndex = 1;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "Publish News";
            // 
            // publish_2_bt
            // 
            this.publish_2_bt.Location = new System.Drawing.Point(395, 26);
            this.publish_2_bt.Name = "publish_2_bt";
            this.publish_2_bt.Size = new System.Drawing.Size(92, 30);
            this.publish_2_bt.TabIndex = 14;
            this.publish_2_bt.Text = "Publish";
            this.publish_2_bt.UseVisualStyleBackColor = true;
            // 
            // textBox1
            // 
            this.textBox1.Location = new System.Drawing.Point(76, 89);
            this.textBox1.Multiline = true;
            this.textBox1.Name = "textBox1";
            this.textBox1.Size = new System.Drawing.Size(526, 22);
            this.textBox1.TabIndex = 8;
            // 
            // text_2_tb
            // 
            this.text_2_tb.AutoSize = true;
            this.text_2_tb.Location = new System.Drawing.Point(17, 89);
            this.text_2_tb.Name = "text_2_tb";
            this.text_2_tb.Size = new System.Drawing.Size(36, 16);
            this.text_2_tb.TabIndex = 7;
            this.text_2_tb.Text = "Text:";
            // 
            // title_2_tb
            // 
            this.title_2_tb.Location = new System.Drawing.Point(76, 53);
            this.title_2_tb.Name = "title_2_tb";
            this.title_2_tb.Size = new System.Drawing.Size(121, 22);
            this.title_2_tb.TabIndex = 6;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(15, 56);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(36, 16);
            this.label1.TabIndex = 2;
            this.label1.Text = "Title:";
            this.label1.Click += new System.EventHandler(this.label1_Click_1);
            // 
            // subject_2_lb
            // 
            this.subject_2_lb.AutoSize = true;
            this.subject_2_lb.Location = new System.Drawing.Point(15, 26);
            this.subject_2_lb.Name = "subject_2_lb";
            this.subject_2_lb.Size = new System.Drawing.Size(55, 16);
            this.subject_2_lb.TabIndex = 1;
            this.subject_2_lb.Text = "Subject:";
            // 
            // subject_2_cb
            // 
            this.subject_2_cb.FormattingEnabled = true;
            this.subject_2_cb.Location = new System.Drawing.Point(76, 23);
            this.subject_2_cb.Name = "subject_2_cb";
            this.subject_2_cb.Size = new System.Drawing.Size(121, 24);
            this.subject_2_cb.TabIndex = 0;
            // 
            // groupBox3
            // 
            this.groupBox3.Controls.Add(this.comment_3_bt);
            this.groupBox3.Controls.Add(this.comment_3_lb);
            this.groupBox3.Controls.Add(this.textBox2);
            this.groupBox3.Controls.Add(this.incoming_3_ltb);
            this.groupBox3.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.groupBox3.Location = new System.Drawing.Point(12, 480);
            this.groupBox3.Name = "groupBox3";
            this.groupBox3.Size = new System.Drawing.Size(625, 183);
            this.groupBox3.TabIndex = 1;
            this.groupBox3.TabStop = false;
            this.groupBox3.Text = "Incoming Feed / Messages";
            // 
            // comment_3_bt
            // 
            this.comment_3_bt.Location = new System.Drawing.Point(526, 126);
            this.comment_3_bt.Name = "comment_3_bt";
            this.comment_3_bt.Size = new System.Drawing.Size(93, 26);
            this.comment_3_bt.TabIndex = 15;
            this.comment_3_bt.Text = "Comment";
            this.comment_3_bt.UseVisualStyleBackColor = true;
            // 
            // comment_3_lb
            // 
            this.comment_3_lb.AutoSize = true;
            this.comment_3_lb.Location = new System.Drawing.Point(10, 131);
            this.comment_3_lb.Name = "comment_3_lb";
            this.comment_3_lb.Size = new System.Drawing.Size(67, 16);
            this.comment_3_lb.TabIndex = 8;
            this.comment_3_lb.Text = "Comment:";
            // 
            // textBox2
            // 
            this.textBox2.Location = new System.Drawing.Point(83, 128);
            this.textBox2.Multiline = true;
            this.textBox2.Name = "textBox2";
            this.textBox2.Size = new System.Drawing.Size(437, 24);
            this.textBox2.TabIndex = 1;
            // 
            // incoming_3_ltb
            // 
            this.incoming_3_ltb.FormattingEnabled = true;
            this.incoming_3_ltb.ItemHeight = 16;
            this.incoming_3_ltb.Location = new System.Drawing.Point(9, 26);
            this.incoming_3_ltb.Name = "incoming_3_ltb";
            this.incoming_3_ltb.Size = new System.Drawing.Size(592, 84);
            this.incoming_3_ltb.TabIndex = 0;
            // 
            // title_lb
            // 
            this.title_lb.AutoSize = true;
            this.title_lb.Font = new System.Drawing.Font("Microsoft Sans Serif", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.title_lb.Location = new System.Drawing.Point(7, 21);
            this.title_lb.Name = "title_lb";
            this.title_lb.Size = new System.Drawing.Size(116, 25);
            this.title_lb.TabIndex = 2;
            this.title_lb.Text = "NSS Client";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(649, 675);
            this.Controls.Add(this.title_lb);
            this.Controls.Add(this.groupBox3);
            this.Controls.Add(this.groupBox2);
            this.Controls.Add(this.groupBox1);
            this.Controls.Add(this.connection_info_gp);
            this.Name = "Form1";
            this.Text = "NSS";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.connection_info_gp.ResumeLayout(false);
            this.connection_info_gp.PerformLayout();
            this.groupBox1.ResumeLayout(false);
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            this.groupBox3.ResumeLayout(false);
            this.groupBox3.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.GroupBox connection_info_gp;
        private System.ComponentModel.BackgroundWorker backgroundWorker1;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.GroupBox groupBox3;
        private System.Windows.Forms.TextBox ip_1_tb;
        private System.Windows.Forms.Label ip_1_lb;
        private System.Windows.Forms.TextBox name_1_tb;
        private System.Windows.Forms.Label name_1_lb;
        private System.Windows.Forms.Label title_lb;
        private System.Windows.Forms.TextBox udp_1_tb;
        private System.Windows.Forms.Label udp_1_lb;
        private System.Windows.Forms.TextBox tcp_1_tb;
        private System.Windows.Forms.Label tcp_1_lb;
        private System.Windows.Forms.TextBox servertcp_1_tb;
        private System.Windows.Forms.Label servertcp_1_lb;
        private System.Windows.Forms.TextBox server_1_tb;
        private System.Windows.Forms.Label server_1_lb;
        private System.Windows.Forms.CheckedListBox checkedListBox1;
        private System.Windows.Forms.Button update_1_bt;
        private System.Windows.Forms.Button deregister_1_bt;
        private System.Windows.Forms.Button register_1_bt;
        private System.Windows.Forms.Button updatesubjects_2_btn;
        private System.Windows.Forms.TextBox title_2_tb;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label subject_2_lb;
        private System.Windows.Forms.ComboBox subject_2_cb;
        private System.Windows.Forms.Label text_2_tb;
        private System.Windows.Forms.Button publish_2_bt;
        private System.Windows.Forms.TextBox textBox1;
        private System.Windows.Forms.TextBox textBox2;
        private System.Windows.Forms.ListBox incoming_3_ltb;
        private System.Windows.Forms.Button comment_3_bt;
        private System.Windows.Forms.Label comment_3_lb;
    }
}

