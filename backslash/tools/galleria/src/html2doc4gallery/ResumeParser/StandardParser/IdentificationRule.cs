using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace html2doc4gallery.ResumeParser.StandardParser
{
    abstract class IdentificationRule
    {
        public abstract bool Run(Section section);
    }
}
