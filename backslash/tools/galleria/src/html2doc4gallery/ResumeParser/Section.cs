using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml;
using System.Xml.Linq;

namespace html2doc4gallery.ResumeParser
{
    class Section
    {
        public string Name { get; set; }

        public XmlNode HtmlNode { get; set; }

        List<XmlNode> htmlChildNodes = new List<XmlNode>();
        public List<XmlNode> HtmlChildNodes
        {
            get
            {
                return htmlChildNodes;
            }
        }

        Dictionary<string, string> annotations = new Dictionary<string, string>();
        public Dictionary<string, string> Annotations
        {
            get
            {
                return annotations;
            }
        }

        List<Section> childSections = new List<Section>();
        public List<Section> ChildSections
        {
            get
            {
                return childSections;
            }
        }

        public Section Parent { get; set; }

        public void ParseContents()
        {
            foreach (Section section in ChildSections)
                section.ParseContents();
        }

        public ContentTypes ContentType
        {
            get;
            set;
        }
    }
}