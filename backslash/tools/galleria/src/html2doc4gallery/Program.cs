using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml.Serialization;
using System.IO;

namespace html2doc4gallery
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Usage: html2doc4gallery.exe createconfig|basePath");
            Console.WriteLine("createconfig writes a sample xml config. basePath is where resumes reside. Outputs to basePath + '\\output'.");

            string basePath;
            if (args.Length > 0)
            {
                if (args[0] == "createconfig")
                {
                    CreateConfig();
                    return;
                }
                basePath = args[0];
            }
            else
                basePath = System.IO.Directory.GetCurrentDirectory();

            new Converter(basePath).Do();
        }

        private static void CreateConfig()
        {
            TemplateSettings settings = new TemplateSettings();
            Template template = new Template();
            template.Name = "www.jobhunt.in:Template(Bright)";
            template.StyleName = "Fancy";
            template.BottomMargin = 48;
            template.TopMargin = 48;
            template.LeftMargin = 48;
            template.RightMargin = 48;
            settings.Templates.Add(template);

            // Serialization
            XmlSerializer s = new XmlSerializer(typeof(TemplateSettings));
            TextWriter w = new StreamWriter(@"templatesettings.sample.xml");
            s.Serialize(w, settings);
            w.Close();
        }
    }
}
