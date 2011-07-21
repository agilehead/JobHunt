using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace html2doc4gallery
{
    public class TemplateSettings
    {        
        List<Template> properties = new List<Template>();
        public List<Template> Templates
        {
            get
            {
                return properties;
            }
            set
            {
                properties = value;
            }
        }
    }

    public class Template
    {
        public string Name { get; set; }
        public string StyleName { get; set; }
        public float TopMargin { get; set; }
        public float BottomMargin { get; set; }
        public float LeftMargin { get; set; }
        public float RightMargin { get; set; }
        public bool EmbedFonts { get; set; }
    }
}

