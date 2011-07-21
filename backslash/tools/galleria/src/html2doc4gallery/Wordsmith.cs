using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using Microsoft.Office.Interop.Word;
using System.Runtime.InteropServices;
using System.Reflection;

namespace html2doc4gallery
{
    class Wordsmith
    {
        object missing = Type.Missing;
        bool createNew = true;
        Application app = null;

        public void ApplyTemplate(string srcHtml, Template template, string outputDoc)
        {
            object readOnly = true;
            object saveChanges = false;
            object oSource = srcHtml;
            object oTrue = true;
            object oFalse = false;

            try
            {
                if (createNew)
                {
                    app = new Application();
                    createNew = false;
                }

                // Source document open here
                app.Documents.Open(ref oSource, ref missing,
                     ref readOnly, ref missing, ref missing,
                     ref missing, ref missing, ref missing,
                     ref missing, ref missing, ref missing,
                     ref missing, ref missing, ref missing, ref missing,
                     ref missing);

                app.ActiveDocument.ApplyQuickStyleSet(template.StyleName);

                SetProperty(app.ActiveDocument, true, "Comments", template.Name);

                PageSetup pageSetup = app.ActiveDocument.PageSetup;
                pageSetup.BottomMargin = template.BottomMargin;
                pageSetup.TopMargin = template.TopMargin;
                pageSetup.LeftMargin = template.LeftMargin;
                pageSetup.RightMargin = template.RightMargin;

                object format = WdSaveFormat.wdFormatDocument;
                object oOutputDoc = outputDoc;

                if (template.EmbedFonts)
                    app.ActiveDocument.SaveSubsetFonts = false;

                object oEmbedFonts = template.EmbedFonts ? true : false;
                app.ActiveDocument.ActiveWindow.ActivePane.View.Type = WdViewType.wdPrintView;
                app.ActiveDocument.SaveAs(ref oOutputDoc, ref format,
                        ref missing, ref missing, ref missing,
                        ref missing, ref missing, ref oEmbedFonts,
                        ref missing, ref missing, ref missing,
                        ref missing, ref missing, ref missing,
                        ref missing, ref missing);

                app.ActiveDocument.Close(ref oFalse, ref missing, ref missing);
            }
            catch
            {
                if (app != null)
                {
                    app.Quit(ref saveChanges, ref missing, ref missing);
                    Marshal.ReleaseComObject(app);
                    createNew = true;
                }
                throw;
            }
        }

        private void SetProperty(Document doc, bool isBuiltIn, string name, string value)
        {
            object oDocBuiltInProps;
            if (isBuiltIn)
                oDocBuiltInProps = doc.BuiltInDocumentProperties;
            else
                throw new Exception("Custom properties are not supported.");

            Type typeDocBuiltInProps = oDocBuiltInProps.GetType();

            typeDocBuiltInProps.InvokeMember("Item",
                                       BindingFlags.Default |
                                       BindingFlags.SetProperty,
                                       null, oDocBuiltInProps,
                                       new object[] { name, value });

        }
    }
}