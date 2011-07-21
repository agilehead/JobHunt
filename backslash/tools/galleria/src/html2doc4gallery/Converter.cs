using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Xml.Serialization;
using html2doc4gallery.ResumeParser;

namespace html2doc4gallery
{
    class Converter
    {
        string basePath;

        public Converter(string basePath)
        {
            this.basePath = basePath;
        }

        private IEnumerable<string> GetHtmlFiles()
        {
            List<string> results = new List<string>();
            foreach (var ext in new[] { "*.htm", "*.html" })
            {
                results.AddRange(Directory.GetFiles(basePath, ext));
            }
            return results;
        }

        //The application assumes the file named "templatesettings.xml" in basePath.
        private TemplateSettings GetTemplateSettings()
        {
            XmlSerializer s = new XmlSerializer(typeof(TemplateSettings));
            TextReader r = new StreamReader(Path.Combine(basePath, "templatesettings.xml"));
            return (TemplateSettings)s.Deserialize(r);
        }

        public void Do()
        {
            string outputDir = Path.Combine(basePath, "output");
            string xslFile = Path.Combine(basePath, "preprocessor.xslt");

            IEnumerable<string> htmlFiles = GetHtmlFiles();
            TemplateSettings settings = GetTemplateSettings();

            Preprocessor processor = new Preprocessor();
            Wordsmith agentSmith = new Wordsmith();
            Preview preview = new Preview();

            int counter = 0;
            foreach (var htmlSrc in htmlFiles)
            {
                foreach (var template in settings.Templates)
                {
                    counter++;

                    Console.WriteLine("Starting file " + counter.ToString() + ": " + Path.GetFileNameWithoutExtension(htmlSrc));
                    
                    //Step1: HTML Pre-processor
                    //After pre-processing the new file will be in the output directory.
                    var preprocOutput = Path.Combine(outputDir, Path.GetFileName(htmlSrc));
                    Console.WriteLine("Pre-processing " + Path.GetFileNameWithoutExtension(htmlSrc));
                    processor.Convert(htmlSrc, xslFile, preprocOutput);
                    
                    //Step2: Convert HTML to Doc                    
                    var outputDoc = Path.Combine(outputDir, Path.GetFileNameWithoutExtension(htmlSrc)
                        + "-" + template.StyleName + ".doc");
                    Console.WriteLine(Path.GetFileNameWithoutExtension(htmlSrc) + " + " + template.StyleName
                        + " = " + Path.GetFileNameWithoutExtension(outputDoc));
                    agentSmith.ApplyTemplate(preprocOutput, template, outputDoc);

                    //Step3: Get the Preview
                    var previewImg = Path.Combine(outputDir, Path.GetFileNameWithoutExtension(outputDoc) + ".png");
                    Console.WriteLine("Generating preview for " + Path.GetFileName(outputDoc));
                    preview.SaveImage(outputDoc, previewImg);
                }
            }
        }
    }
}