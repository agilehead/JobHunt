using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using Microsoft.Office.Interop.Word;
using System.Runtime.InteropServices;

namespace html2doc4gallery
{
    class Preview
    {
        Application App = null;
        bool createNew = true;

        public void SaveImage(string docFile, string outputImg)
        {
            object Unknown = Type.Missing;
            object ReadOnly = true;
            object SaveChanges = false;

            if (createNew)
            {
                App = new Application();
                createNew = false;
            }

            try
            {
                object Source = docFile;
                // Open document from file
                App.Documents.Open(ref Source, ref Unknown,
                                 ref ReadOnly, ref Unknown, ref Unknown,
                                 ref Unknown, ref Unknown, ref Unknown,
                                 ref Unknown, ref Unknown, ref Unknown,
                                 ref Unknown, ref Unknown, ref Unknown, ref Unknown,
                                 ref Unknown);
                // Print all pages of the document
                App.ActivePrinter = "Zan Image Printer(color)";
                object oTrue = true;
                object oFalse = false;
                object range = WdPrintOutRange.wdPrintCurrentPage;
                object items = WdPrintOutItem.wdPrintDocumentContent;
                object pageType = WdPrintOutPages.wdPrintAllPages;
                object pages = "1";
                object target = 1;
                object copies = "1";
                App.ActiveDocument.PrintOut(ref oTrue, ref oFalse, ref range, ref Unknown, ref Unknown, ref Unknown, ref items, ref copies,
                    ref pages, ref pageType, ref oFalse, ref Unknown, ref Unknown, ref Unknown, ref Unknown, ref Unknown,
                    ref Unknown, ref Unknown);

                App.ActiveDocument.Close(ref oFalse, ref Unknown, ref Unknown);
            }
            catch
            {
                // Close Microsoft Word
                App.Quit(ref SaveChanges, ref Unknown, ref Unknown);
                Marshal.ReleaseComObject(App);
                createNew = true;
            }
        }
    }
}