using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace html2doc4gallery.ResumeParser.StandardParser
{
    /* Name should be in Header with class = "fullname"     * 
     */
    class FullNameRule : IdentificationRule
    {
        public override bool Run(Section resume)
        {
            bool success = false;

            List<Section> headers = HtmlHelper.GetHeaderSections(resume);
            foreach (Section header in headers)
            {
                if (HtmlHelper.GetClassNames(header.HtmlNode).Contains("fullname"))
                {
                    success = true;
                    header.ContentType = ContentTypes.FullName;
                }
            }

            return success;
        }
    }
}
