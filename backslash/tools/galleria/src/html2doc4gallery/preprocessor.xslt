<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:msxsl="urn:schemas-microsoft-com:xslt" exclude-result-prefixes="msxsl">
  <xsl:output method="html" indent="yes" />
  
  <!-- This does nothing right now -->
  
  <!--<xsl:template match="ul">
    <xsl:for-each select="li">
      <p class="MsoListParagraph">
        <xsl:value-of select="."/>
      </p>
    </xsl:for-each>
  </xsl:template>-->
  <!--<xsl:template match="p">
    <p class="MsoNormal">
      <xsl:apply-templates select="*|node()" />
    </p>
  </xsl:template>
  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()" />
    </xsl:copy>
  </xsl:template>-->
</xsl:stylesheet>
