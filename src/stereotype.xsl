<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns="http://www.srcML.org/srcML/src" 
    xmlns:src="http://www.srcML.org/srcML/src"
    xmlns:str="http://exslt.org/strings"
    extension-element-prefixes=""
    exclude-result-prefixes="src str"
    version="1.0">
<!-- 
@file stereotype.xsl

@copyright Copyright (C) 2018 srcML, LLC. (www.srcML.org)

The stereocode is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

The stereocode Toolkit is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with the stereocode Toolkit; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 -->

<!--
  Define what is to be inserted for each method in a comment. For method stereotypes, this
  is just the name of the stereotype. For method summarization, this is the summary
-->
<xsl:import href="stereotype_base.xsl"/>

<!--
  method stereotype names 
  Note: Leave a single blank space after name
-->
<xsl:template name="method_get">get </xsl:template>
<xsl:template name="method_nonconstget">nonconstget </xsl:template>
<xsl:template name="method_predicate">predicate </xsl:template>
<xsl:template name="method_property">property </xsl:template>
<xsl:template name="method_voidaccessor">void-accessor </xsl:template>
<xsl:template name="method_set">set </xsl:template>
<xsl:template name="method_command">command </xsl:template>
<xsl:template name="method_non-void-command">non-void-command </xsl:template>
<xsl:template name="method_collaborational-predicate">controller </xsl:template>
<xsl:template name="method_collaborational-property">controller </xsl:template>
<xsl:template name="method_collaborational-voidaccessor">controller </xsl:template>
<xsl:template name="method_collaborational-command">controller </xsl:template>
<xsl:template name="method_collaborator">collaborator </xsl:template>
<xsl:template name="method_factory">factory </xsl:template>
<xsl:template name="method_stateless">stateless </xsl:template>
<xsl:template name="method_incidental">incidental </xsl:template>
<xsl:template name="method_empty">empty </xsl:template>

<xsl:template name="method_constructor">constructor </xsl:template>
<xsl:template name="method_copy-constructor">copy-constructor </xsl:template>

<!--
  Section responsible for actually applying all of the stereotypes and annotating
  the source code with a comment.
-->

<xsl:template match="src:comment[@type='block'][following-sibling::*[1][self::src:function or self::src:constructor]]">

  <!-- copy start and contents of existing comment -->
  <xsl:element name="comment" namespace="http://www.srcML.org/srcML/src">
    <xsl:copy-of select="@*"/>

  <!-- copy start and contents of existing comment -->
  <xsl:value-of select="substring-before(., '*/')"/>

  <!-- classifies stereotypes using criteria from stereotype_base.xsl -->
  <xsl:variable name="stereotype">
    <xsl:variable name="raw_stereotype"><xsl:apply-templates select="following-sibling::*[1]" mode="stereotype"/></xsl:variable>
    <xsl:choose>
      <xsl:when test="$raw_stereotype != ''"><xsl:value-of select="$raw_stereotype"/></xsl:when>
      <xsl:otherwise>unclassified </xsl:otherwise>
    </xsl:choose>
  </xsl:variable>

  <!-- insert generated stereotype comment -->
  <xsl:text>&#xa;</xsl:text>
  <xsl:variable name="lastws" select="src:last_ws(.)"/>
  <xsl:if test="string-length($lastws) = 0">
    <xsl:text>    </xsl:text>
  </xsl:if>
  <xsl:value-of select="$lastws"/>

<xsl:text>@stereotype </xsl:text><xsl:value-of select="$stereotype"/>

  <!-- end the comment -->
  <xsl:if test="string-length($lastws) &gt; 0">
    <xsl:text>&#xa;</xsl:text><xsl:value-of select="src:last_ws(.)"/>
  </xsl:if>
  <xsl:value-of select="'*/'"/></xsl:element>

</xsl:template>

<xsl:template match="src:function[not(preceding-sibling::*[1][self::src:comment[@type='block']])] | src:constructor[not(preceding-sibling::*[1][self::src:comment[@type='block']])]
  ">

  <!-- classifies stereotypes using criteria from stereotype_base.xsl -->
  <xsl:variable name="stereotype">
    <xsl:variable name="raw_stereotype"><xsl:apply-templates select="." mode="stereotype"/></xsl:variable>
    <xsl:choose>
      <xsl:when test="$raw_stereotype != ''"><xsl:value-of select="$raw_stereotype"/></xsl:when>
      <xsl:otherwise>unclassified </xsl:otherwise>
    </xsl:choose>
  </xsl:variable>

  <!-- insert new stereotype comment -->
   <sterotype><xsl:value-of select="$stereotype"/></sterotype><xsl:text>&#xa;</xsl:text>

  <!-- insert a copy of the indentation for the function, since we stole it for the inserted comment, must repeat it -->
  <xsl:value-of select="str:split(preceding-sibling::text()[1], '&#xa;')[last()]"/>

  <!-- copy existing method/constructor -->
  <xsl:copy-of select="."/>

</xsl:template>

</xsl:stylesheet>
