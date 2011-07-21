using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml;
using System.Xml.Linq;

namespace html2doc4gallery.ResumeParser
{
    class Resume : Section
    {        
        public void Load(string htmlFile)
        {
            XmlDocument doc = new XmlDocument();
            doc.Load(htmlFile);
            Name = doc.DocumentElement.Name;
            HtmlNode = doc.DocumentElement;
            ParseTree(doc.DocumentElement, this);
        }

        private void ParseTree(XmlNode node, Section currentSection)
        {
            foreach (XmlNode child in node.ChildNodes)
            {
                Section section = new Section();
                section.Name = child.Name.ToLower();
                section.HtmlNode = child;

                if (!HtmlHelper.IsHeader(child))
                {
                    section.Parent = currentSection;
                    currentSection.ChildSections.Add(section);
                    ParseTree(child, section);
                }
                else
                {
                    Section parent = FindParent(section, currentSection);
                    section.Parent = parent;
                    parent.ChildSections.Add(section);
                    currentSection = section;
                }
            }
        }

        private Section FindParent(Section header, Section currentSection)
        {
            Func<Section,int> getLevel = sec => Convert.ToInt32(sec.Name.Substring(1));
            
            //Start from top, and see move on until the header refused to fit.
            //To start from top, reverse the sectionChain
            List<Section> sections = new List<Section>();
            sections.Add(currentSection);
            Section section = currentSection;
            while((section = section.Parent) != null)
                sections.Add(section);
            sections.Reverse();

            Section compatible = null;
            foreach (Section s in sections)
            {
                if (HtmlHelper.IsHeader(s.HtmlNode) && (getLevel(s) >= getLevel(header)))
                    break; //If we encounter a header that is smaller than our target header, return the last compatible section.

                if (new []{"body", "div"}.Contains(s.Name) ||
                    (HtmlHelper.IsHeader(s.HtmlNode) && (getLevel(s) < getLevel(header))))
                {
                    compatible = s;
                }
            }
            return compatible;
        }
    }
}
