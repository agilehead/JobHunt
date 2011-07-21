using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml;
using System.Xml.Linq;
using System.IO;
using System.Xml.Xsl;

namespace html2doc4gallery
{
    class Preprocessor
    {
        public void Convert(string inputFileName, string xsl, string outputFileName)
        {
            XslCompiledTransform xslt = new XslCompiledTransform(false);
            xslt.Load(xsl);
            xslt.Transform(inputFileName, outputFileName);

            //File.Copy(inputFileName, outputFileName, true);
        }
    }
}
