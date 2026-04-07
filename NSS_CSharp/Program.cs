using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace NSS
{
    internal static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main(string[] args)
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            bool isServerMode = args.Any(a => a.Equals("server", StringComparison.OrdinalIgnoreCase));
            bool isServerA = args.Any(a => a.Equals("A", StringComparison.OrdinalIgnoreCase));

            Application.Run(new Form1(isServerMode, isServerA));
        }
    }
}
