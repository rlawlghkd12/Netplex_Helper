using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Microsoft.Office.Interop.Excel;

namespace Netflix_Helper
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();

            prepare_comboBox();
        }

        private string filePath = "";

        public void prepare_comboBox()
        {
            // item 추가하기
            comboBox1.Items.Add("SF");
            comboBox1.Items.Add("드라마");
            comboBox1.Items.Add("스릴러");
        }

        // 제목
        private void label1_Click(object sender, EventArgs e)
        {

        }


        private void Form1_Load(object sender, EventArgs e)
        {

        }

        // 일반 검색
        private void textBox1_TextChanged(object sender, EventArgs e)
        {
            // textBox1.Text
        }

        // 장르 검색
        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        // 검색 버튼
        private void button1_Click(object sender, EventArgs e)
        {

        }

        // 엑셀 파일 위치 검색
        private void button2_Click(object sender, EventArgs e)
        {
            OpenFileDialog OFD = new OpenFileDialog();

            if (OFD.ShowDialog() == DialogResult.OK) {
                richTextBox2.Clear();
                richTextBox2.Text = OFD.FileName;
                filePath = OFD.FileName;
            }
        }

        private void DeleteObject(object obj)
        {
            try
            {
                System.Runtime.InteropServices.Marshal.ReleaseComObject(obj);
                obj = null;
            }
            catch (Exception ex)
            {
                obj = null;
                MessageBox.Show("메모리 할당을 해제하는 중 문제가 발생하였습니다." + ex.ToString(), "경고!");
            }
            finally
            {
                GC.Collect();
            }
        }

        private void richTextBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void richTextBox2_TextChanged(object sender, EventArgs e)
        {

        }

        private void button3_Click(object sender, EventArgs e)
        {
            if (filePath != "") {
                Microsoft.Office.Interop.Excel.Application application = new Microsoft.Office.Interop.Excel.Application();
                Workbook workbook = application.Workbooks.Open(Filename: @filePath);
                Worksheet worksheet1 = workbook.Worksheets.get_Item("Sheet1");
                application.Visible = false;
                Range range = worksheet1.UsedRange;
                String data = "";
                
                for (int i = 1; i <= range.Rows.Count; ++i) {
                    for (int j = 1; j <= range.Columns.Count; ++j) {
                        data += ((range.Cells[i, j] as Range).Value2.ToString() + " ");
                    } 
                    data += "\n";
                }

                richTextBox1.Text = data;

                DeleteObject(worksheet1);
                DeleteObject(workbook);
                application.Quit();
                DeleteObject(application);
            }
        }
    }
}
