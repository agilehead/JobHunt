using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml;
using System.Xml.Linq;

namespace html2doc4gallery.ResumeParser
{
    static class HtmlHelper
    {
        public static bool IsHeader(XmlNode node)
        {
            return new[] { "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8" }.Contains(node.Name.ToLower());
        }

        public static bool IsHeader(Section section)
        {
            return new[] { "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8" }.Contains(section.Name);
        }

        public static List<Section> GetHeaderSections(Section section)
        {
            return GetHeaderSectionsRec(section, new List<Section>());
        }

        private static List<Section> GetHeaderSectionsRec(Section section, List<Section> headersList)
        {
            foreach (Section child in section.ChildSections)
            {
                if (IsHeader(section))
                    headersList.Add(child);
                GetHeaderSectionsRec(child, headersList);
            }
            return headersList;
        }

        public static List<string> GetClassNames(XmlNode node)
        {
            XmlAttribute attrClass = node.Attributes["class"];
            if (attrClass != null && attrClass.Value != null)
                return new List<string>(attrClass.Value.Split(' '));
            else
                return null;
        }
    }
}