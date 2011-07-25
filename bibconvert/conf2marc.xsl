<?xml version="1.0" encoding="ISO-8859-1"?>
<!-- $Id$ -->
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="xml" encoding="UTF-8"/>
<xsl:template match="/">
    <collection xmlns="http://www.loc.gov/MARC21/slim">
        <xsl:for-each select="//goal_record">
            <record>
                <xsl:if test="./mconf">
                    <datafield tag="970" ind1=" " ind2=" ">
                        <subfield code="a">CONF-<xsl:value-of select="./mconf"/></subfield>
                    </datafield>
                </xsl:if>


	        <xsl:call-template name="one-eleven">
	        </xsl:call-template>

	        <xsl:call-template name="basic-element">
	          <xsl:with-param name="select" select="./other-title" />
	          <xsl:with-param name="code">a</xsl:with-param>
	          <xsl:with-param name="tag">711</xsl:with-param>
	        </xsl:call-template>

	        <xsl:call-template name="basic-element">
	          <xsl:with-param name="select" select="./email" />
	          <xsl:with-param name="code">m</xsl:with-param>
	          <xsl:with-param name="tag">270</xsl:with-param>
	        </xsl:call-template>

                <xsl:call-template name="basic-element">
	          <xsl:with-param name="select" select="./note" />
	          <xsl:with-param name="code">a</xsl:with-param>
	          <xsl:with-param name="tag">500</xsl:with-param>
	        </xsl:call-template>

	        <xsl:call-template name="basic-element">
	          <xsl:with-param name="select" select="./newurl" />
	          <xsl:with-param name="code">u</xsl:with-param>
	          <xsl:with-param name="tag">856</xsl:with-param>
	          <xsl:with-param name="ind1">4</xsl:with-param>
	          <xsl:with-param name="sub2">y</xsl:with-param>
	          <xsl:with-param name="sub2val">Proceedings</xsl:with-param>	                   </xsl:call-template>

	        <xsl:call-template name="basic-element">
	          <xsl:with-param name="select" select="./trans" />
	          <xsl:with-param name="code">u</xsl:with-param>
	          <xsl:with-param name="tag">856</xsl:with-param>
	          <xsl:with-param name="ind1">4</xsl:with-param>
	          <xsl:with-param name="sub2">y</xsl:with-param>
	          <xsl:with-param name="sub2val">Talks</xsl:with-param>
	        </xsl:call-template>

	        <xsl:call-template name="basic-element">
	          <xsl:with-param name="select" select="./url" />
	          <xsl:with-param name="code">u</xsl:with-param>
	          <xsl:with-param name="tag">856</xsl:with-param>
	          <xsl:with-param name="ind1">4</xsl:with-param>
	          <xsl:with-param name="sub2">y</xsl:with-param>
	          <xsl:with-param name="sub2val">Conference Announcement</xsl:with-param>
	        </xsl:call-template>




	        <xsl:call-template name="basic-element">
	          <xsl:with-param name="select" select="./series" />
	          <xsl:with-param name="code">a</xsl:with-param>
	          <xsl:with-param name="tag">411</xsl:with-param>
	        </xsl:call-template>
	        <xsl:call-template name="basic-element">
	          <xsl:with-param name="select" select="./xpl" />
	          <xsl:with-param name="code">b</xsl:with-param>
	          <xsl:with-param name="tag">270</xsl:with-param>
	        </xsl:call-template>


                <xsl:call-template name="basic-element">
	          <xsl:with-param name="select" select="./keyword" />
	          <xsl:with-param name="code">a</xsl:with-param>
	          <xsl:with-param name="tag">653</xsl:with-param>
	          <xsl:with-param name="ind1">1</xsl:with-param>
	        </xsl:call-template>



                <!--add collection id-->
                <datafield tag="980" ind1=" " ind2=" ">
                  <subfield code="a">CONFERENCES</subfield>
                </datafield>
            </record>
<xsl:text>
</xsl:text>

        </xsl:for-each>
    </collection>

</xsl:template>


 <xsl:template name="basic-element">
    <xsl:param name = "select"/>
    <xsl:param name = "tag"/>
    <xsl:param name = "ind1"><xsl:text> </xsl:text></xsl:param>
    <xsl:param name = "ind2"><xsl:text> </xsl:text></xsl:param>
    <xsl:param name = "subfield"/>
    <xsl:param name = "code"/>
    <xsl:param name = "source" />
    <xsl:param name = "sub2"/>
    <xsl:param name = "sub2_val" />
    <xsl:param name = "sub_only" />
    <xsl:for-each select="$select">
      <!--do not print tags for empty values-->
      <xsl:if test="string(.)">
	  <datafield>
	    <xsl:attribute name = "tag">
	      <xsl:value-of select="$tag"/>
	    </xsl:attribute>
	    <xsl:attribute name = "ind1">
	      <xsl:value-of select="$ind1"/>
	    </xsl:attribute>
	    <xsl:attribute name = "ind2">
	      <xsl:value-of select="$ind2"/>
	    </xsl:attribute>

	  <xsl:call-template name="subfield">
	    <xsl:with-param name="select">
	    <xsl:value-of select="normalize-space(.)"/> </xsl:with-param>
	    <xsl:with-param name="code"><xsl:value-of select="$code"/></xsl:with-param>
	  </xsl:call-template>

	  <xsl:if test="string($source)">
	    <subfield code="9">
	      <xsl:value-of select="$source"/>
	    </subfield>
	  </xsl:if>
	  <xsl:if test="string($sub2_val)">


	  <xsl:call-template name="subfield">
	    <xsl:with-param name="select"><xsl:value-of select="$sub2_val" /> </xsl:with-param>
	    <xsl:with-param name="code"><xsl:value-of select="$sub2"/></xsl:with-param>
	  </xsl:call-template>


	  </xsl:if>
	  </datafield>
      </xsl:if>
      <xsl:text>&#10;</xsl:text>
    </xsl:for-each>
  </xsl:template>


 <xsl:template name="subfield">
    <xsl:param name = "code"/>
    <xsl:param name = "select"/>
    <subfield>
      <xsl:attribute name = "code">
	<xsl:value-of select="$code"/>
      </xsl:attribute>
      <xsl:value-of select="normalize-space($select)"/>
    </subfield>
 </xsl:template>

 <xsl:template name="one-eleven">
	<datafield>
	  <xsl:attribute name = "tag">
	    <xsl:value-of select="111"/>
	  </xsl:attribute>
	  <xsl:attribute name = "ind1">
            <xsl:text> </xsl:text>
	  </xsl:attribute>
	  <xsl:attribute name = "ind2">
            <xsl:text> </xsl:text>
	  </xsl:attribute>
	  <xsl:call-template name="subfield">
	    <xsl:with-param name="select" select="./title" />
	    <xsl:with-param name="code">a</xsl:with-param>
	  </xsl:call-template>
	  <xsl:call-template name="subfield">
	    <xsl:with-param name="select" select="./dates" />
	    <xsl:with-param name="code">d</xsl:with-param>
	  </xsl:call-template>
	  <xsl:call-template name="subfield">
	    <xsl:with-param name="select" select="./date-qual" />
	    <xsl:with-param name="code">x</xsl:with-param>
	  </xsl:call-template>
	  <xsl:call-template name="subfield">
	    <xsl:with-param name="select" select="./place" />
	    <xsl:with-param name="code">c</xsl:with-param>
	  </xsl:call-template>
	  <xsl:call-template name="subfield">
	    <xsl:with-param name="select" select="translate(./c-number,'/-.','')" />
	    <xsl:with-param name="code">g</xsl:with-param>
	  </xsl:call-template>
        </datafield>
 </xsl:template>

</xsl:stylesheet>
