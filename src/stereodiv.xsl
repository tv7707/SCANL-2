<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns="http://www.srcML.org/srcML/src" 
    xmlns:src="http://www.srcML.org/srcML/src"
    xmlns:html="http://www.w3.org/1999/xhtml"
    extension-element-prefixes=""
    exclude-result-prefixes="src"
    version="1.0">
<!-- 
	@file stereotypediv.xsl

	Creates a <div> around methods and their preceding comment 
 -->

<xsl:output method="xml" encoding="UTF-8" standalone="yes"/>

<!-- Match the comment that precedes the function --> 
<xsl:template match="src:comment[following-sibling::*[1][self::src:function or self::src:constructor]]">

  <!-- extract the stereotype from the comment -->
  <xsl:variable name="stereotype_s" select="substring-after(., '@stereotype')"/>

  <xsl:variable name="stereotype">
    <xsl:choose>
      <xsl:when test="contains($stereotype_s, '&#xA;')">
        <xsl:value-of select="substring-before($stereotype_s, '&#xA;')"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="substring-before($stereotype_s, '*/')"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:variable>

  <html:div class="stereotype {$stereotype}">

  <!-- copy current comment -->
  <xsl:copy-of select="."/>

  <!-- copy whitespace inbetween the comment and the function -->
  <xsl:copy-of select="following-sibling::text()[1]"/>

  <!-- copy existing function or constructor -->
  <xsl:copy-of select="following-sibling::*[1]"/>

  </html:div>

</xsl:template>

<!-- Do not copy functions with a preceding comment as that is handled in the comment -->
<xsl:template match="src:function[preceding-sibling::*[1][self::src:comment]] |
  src:constructor[preceding-sibling::*[1][self::src:comment]]"/>

<!-- Do not copy nodes (whitespace) between comment and function and that is handled in the comment -->
<xsl:template match="text()[following-sibling::src:*[1][self::src:function or self::src:constructor] and preceding-sibling::*[1][self::src:comment[1]]]"/>

<!-- default copy -->
<xsl:template match="@*|node()">
<xsl:copy>
  <xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

</xsl:stylesheet>