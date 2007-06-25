<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
				xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
				
	<xsl:template match="/">
	
<html>
	<meta http-equiv="Content-Type" content="text/html; charset=windows-1252" />
	<link href="../style/book.css" rel="stylesheet" type="text/css" />
	<head>
		<title>
			<xsl:value-of select="//@display-name"/>
		</title>
	</head>
	<body>
	
		<h2>
			<xsl:value-of select="//@display-name"/>
		</h2>
		
	<xsl:for-each select="indicator-declaration">
	<xsl:for-each select="indicator-documentation">

		<xsl:choose>
			<xsl:when test="count(definition) > 0">
     			<xsl:for-each select="definition">
	       			<p><xsl:value-of select="." /></p>
  			    </xsl:for-each>
   			 </xsl:when>
    		<xsl:otherwise>
     			<p><font color="red">[definition missing]</font></p>
    		</xsl:otherwise>
  		</xsl:choose>	
  		
		<h3 id="interpreting-results">Interpreting Results 
		    <a href="reading_indicator_documentation.html#interpreting_results"><img border="0" src="help.gif" alt="Help"/></a></h3>
		<xsl:choose>
			<xsl:when test="count(interpreting-results) > 0">
     			<xsl:for-each select="interpreting-results">
	       			<p><xsl:copy-of select="." /></p>
  			    </xsl:for-each>
   			 </xsl:when>
    		<xsl:otherwise>
     			<p>Interpreting indicator results depends on the context of use.  We don't yet have
     			   any advice about interpreting this indicator.  If you have a question or suggestion, 
     			   please let us know!</p>
    		</xsl:otherwise>
  		</xsl:choose>

		<h3>Units of Measurement and Precision 
		    <a href="reading_indicator_documentation.html#units_and_precision"><img border="0" src="help.gif" alt="Help"/></a></h3>
		<xsl:for-each select="display-format">
		    <p>
			<xsl:for-each select="units">
				Units: <xsl:value-of select="."/> <br/>
			</xsl:for-each>		
			<xsl:for-each select="unitless">
				Units: unitless <br/>
			</xsl:for-each>	
			<xsl:for-each select="number">
				Default precision for display: as a number using <xsl:value-of select="@digits"/> digits after the decimal
			</xsl:for-each>
			<xsl:for-each select="percentage">
				Default precision for display: as a percentage with <xsl:value-of select="@digits"/> digits after the decimal
			</xsl:for-each>
			<xsl:for-each select="scientific">
				Default precision for display: scientific notation with <xsl:value-of select="@digits"/> digits of precision
			</xsl:for-each>
			</p>
	    </xsl:for-each>

		<h3>Related Indicators  
		    <a href="reading_indicator_documentation.html#related"><img border="0" src="help.gif" alt="Help"/></a></h3>
		<xsl:choose>
			<xsl:when test="count(related-indicators) > 0">
     			<xsl:for-each select="related-indicators">
	       			<p><xsl:copy-of select="." /></p>
  			    </xsl:for-each>
   			 </xsl:when>
    		<xsl:otherwise>
     			<p>None listed.</p>
    		</xsl:otherwise>
  		</xsl:choose>

		<h3>Specification 
		    <a href="reading_indicator_documentation.html#specification"><img border="0" src="help.gif" alt="Help"/></a></h3>
		<xsl:choose>
			<xsl:when test="count(specification) > 0">
     			<xsl:for-each select="specification">
	       			<p><xsl:copy-of select="." /></p>
  			    </xsl:for-each>
   			 </xsl:when>
    		<xsl:otherwise>
     			<p><font color="red">[specification missing]</font></p>
    		</xsl:otherwise>
  		</xsl:choose>
  		
		<h3 id="limitations">Limitations 
		    <a href="reading_indicator_documentation.html#limitations"><img border="0" src="help.gif" alt="Help"/></a></h3>
		<xsl:choose>
			<xsl:when test="count(limitations) > 0">
     			<xsl:for-each select="limitations">
	       			<p><xsl:copy-of select="." /></p>
  			    </xsl:for-each>
   			 </xsl:when>
    		<xsl:otherwise>
     			<p>None listed.</p>
    		</xsl:otherwise>
  		</xsl:choose>

		<h3 id="how-modeled">How Modeled 
		    <a href="reading_indicator_documentation.html#how_modeled"><img border="0" src="help.gif" alt="Help"/></a></h3>
		<xsl:choose>
			<xsl:when test="count(how-modeled) > 0">
     			<xsl:for-each select="how-modeled">
	       			<p><xsl:copy-of select="." /></p>
  			    </xsl:for-each>
   			 </xsl:when>
    		<xsl:otherwise>
     			<p>Not specified.  (In this case, normally one can assume that the value of this indicator is modeled by UrbanSim itself,
     			as opposed to being exogenous, that is, coming from an external source
     			such as a control total.)</p>
    		</xsl:otherwise>
  		</xsl:choose>

		<h3>Indicator Source, Evolution, and Examples of Use 
		    <a href="reading_indicator_documentation.html#source"><img border="0" src="help.gif" alt="Help"/></a></h3>
		<xsl:choose>
			<xsl:when test="count(source-evolution-examples) > 0">
     			<xsl:for-each select="source-evolution-examples">
	       			<p><xsl:copy-of select="." /></p>
  			    </xsl:for-each>
   			 </xsl:when>
    		<xsl:otherwise>
     			<p>Not specified.</p>
    		</xsl:otherwise>
  		</xsl:choose>

	</xsl:for-each>

    <h3>Source Code and Tests 
		    <a href="reading_indicator_documentation.html#source-code"><img border="0" src="help.gif" alt="Help"/></a></h3>
		    
    <p>This section provides links to the source code for the Opus variables that implement this indicator,
    with accompanying unit tests.  (Primary attributes don't have any associated code, however.)</p>
		<ul>
        <xsl:for-each select="source">
	        <li><xsl:copy-of select="." /></li>
  		</xsl:for-each>
  		</ul>
	
	</xsl:for-each>
	</body>
</html>
</xsl:template>
</xsl:stylesheet>
