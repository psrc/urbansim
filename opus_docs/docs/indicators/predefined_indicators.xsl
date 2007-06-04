<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
				xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
				
<xsl:template match="/">
	
<html>

<head>
<meta http-equiv="Content-Language" content="en-us" />
<meta http-equiv="Content-Type" content="text/html; charset=windows-1252" />
<link href="../style/book.css" rel="stylesheet" type="text/css" />
<title>List of Predefined Indicators</title>
</head>

<body>

<h1>List of Predefined Indicators</h1>


<xsl:for-each select="indicator_list/group">

    <h2><xsl:value-of select="@name" /></h2>
    <ul>

    <ul>
    <xsl:for-each select="indicator">
        <li>
			<a>
				<xsl:attribute name="href">
					<xsl:value-of select="@filename" />
				</xsl:attribute>
				<xsl:value-of select="@fullname" />
			</a>
		</li>
    </xsl:for-each>
    </ul>

    <xsl:for-each select="subgroup">
    
        <h3><xsl:value-of select="@name" /></h3>
        <ul>
        <xsl:for-each select="indicator">
            <li>
				<a>
					<xsl:attribute name="href">
						<xsl:value-of select="@filename" />
					</xsl:attribute>
					<xsl:value-of select="@fullname" />
				</a>
			</li>
        </xsl:for-each>
        </ul>
    
    </xsl:for-each>
    </ul>

</xsl:for-each>

</body>
</html>
</xsl:template>
</xsl:stylesheet>
