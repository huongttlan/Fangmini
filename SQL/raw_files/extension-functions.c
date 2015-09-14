<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head>
<title>SQLite Home Page</title>
<style type="text/css">
body {
    margin: auto;
    font-family: Verdana, sans-serif;
    padding: 8px 1%;
}

a { color: #044a64 }
a:visited { color: #734559 }

.logo { position:absolute; margin:3px; }
.tagline {
  float:right;
  text-align:right;
  font-style:italic;
  width:300px;
  margin:12px;
  margin-top:58px;
}

.toolbar {
  text-align: center;
  line-height: 1.6em;
  margin: 0;
  padding: 0px 8px;
}
.toolbar a { color: white; text-decoration: none; padding: 6px 12px; }
.toolbar a:visited { color: white; }
.toolbar a:hover { color: #044a64; background: white; }

.content    { margin: 5%; }
.content dt { font-weight:bold; }
.content dd { margin-bottom: 25px; margin-left:20%; }
.content ul { padding:0px; padding-left: 15px; margin:0px; }

/* rounded corners */
.se  { background: url(images/se.gif) 100% 100% no-repeat #044a64}
.sw  { background: url(images/sw.gif) 0% 100% no-repeat }
.ne  { background: url(images/ne.gif) 100% 0% no-repeat }
.nw  { background: url(images/nw.gif) 0% 0% no-repeat }

/* Things for "fancyformat" documents start here. */
.fancy img+p {font-style:italic}
.fancy .codeblock i { color: darkblue; }
.fancy h1,.fancy h2,.fancy h3,.fancy h4 {font-weight:normal;color:#044a64}
.fancy h2 { margin-left: 10px }
.fancy h3 { margin-left: 20px }
.fancy h4 { margin-left: 30px }
.fancy th {white-space:nowrap;text-align:left;border-bottom:solid 1px #444}
.fancy th, .fancy td {padding: 0.2em 1ex; vertical-align:top}
.fancy #toc a        { color: darkblue ; text-decoration: none }
.fancy .todo         { color: #AA3333 ; font-style : italic }
.fancy .todo:before  { content: 'TODO:' }
.fancy p.todo        { border: solid #AA3333 1px; padding: 1ex }
.fancy img { display:block; }
.fancy :link:hover, .fancy :visited:hover { background: wheat }
.fancy p,.fancy ul,.fancy ol { margin: 1em 5ex }
.fancy li p { margin: 1em 0 }
/* End of "fancyformat" specific rules. */

</style>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
  
</head>
<body>
<div><!-- container div to satisfy validator -->

<a href="index.html">
<img class="logo" src="images/sqlite370_banner.gif" alt="SQLite Logo"
 border="0"></a>
<div><!-- IE hack to prevent disappearing logo--></div>
<div class="tagline">Small. Fast. Reliable.<br>Choose any three.</div>

<table width=100% style="clear:both"><tr><td>
  <div class="se"><div class="sw"><div class="ne"><div class="nw">
  <table width=100% style="padding:0;margin:0;cell-spacing:0"><tr>
  <td width=100%>
  <div class="toolbar">
    <a href="about.html">About</a>
    <a href="sitemap.html">Sitemap</a>
    <a href="docs.html">Documentation</a>

    <a href="download.html">Download</a>
    <a href="copyright.html">License</a>
    <a href="news.html">News</a>
    <a href="support.html">Support</a>
  </div>
<script>
  gMsg = "Search SQLite Docs..."
  function entersearch() {
    var q = document.getElementById("q");
    if( q.value == gMsg ) { q.value = "" }
    q.style.color = "black"
    q.style.fontStyle = "normal"
  }
  function leavesearch() {
    var q = document.getElementById("q");
    if( q.value == "" ) { 
      q.value = gMsg
      q.style.color = "#044a64"
      q.style.fontStyle = "italic"
    }
  }
</script>
<td>

    <div style="padding:0 1em 0px 0;white-space:nowrap">
    <form name=f method="GET" action="http://www.sqlite.org/search">
      <input id=q name=q type=text
       onfocus="entersearch()" onblur="leavesearch()" style="width:24ex;padding:1px 1ex; border:solid white 1px; font-size:0.9em ; font-style:italic;color:#044a64;" value="Search SQLite Docs...">
      <input type=submit value="Go" style="border:solid white 1px;background-color:#044a64;color:white;font-size:0.9em;padding:0 1ex">
    </form>
    </div>
  </table>
</div></div></div></div>
</td></tr></table>
<div class=startsearch></div>

<h1 align="center">Contributed Files</h1>


<p>The files below are contributed by users and are not part
of the standard SQLite package.  The content of these files has
not been verified.  Use at your own risk.
</p>

<p>If you would like to contribute files and need a userid and password,
send an email to <a href="mailto:drh@hwaci.com">drh@hwaci.com</a>
requesting one.</p>

<p>Redisplay results ordered by
<a href="/contrib/download/extension-functions.c?orderby=name">Filename</a>,
<a href="/contrib/download/extension-functions.c?orderby=size">Size</a>, or
<a href="/contrib/download/extension-functions.c?orderby=date">Date</a>.</p>

<hr><p>
<p><a href="/contrib/download/extension-functions.c/download/mksqlite.zip?get=2">mksqlite.zip</a> (14.54&nbsp;KB)
contributed by Mike Cariotoglou on 2004-10-10 08:03:30</p>
<blockquote>Delphi sqlite3 bindings, plus an OO layer for SQLITE</blockquote>
<p><a href="/contrib/download/extension-functions.c/download/sqlite_fk.tgz?get=3">sqlite_fk.tgz</a> (204.18&nbsp;KB)
contributed by Cody Pisto on 2004-10-14 23:05:34</p>
<blockquote>Utility to generate triggers to enforce foreign key constraints with sqlite, operates on database schema and understands most CREATE TABLE syntax. Win32 and linux x86 binaries included, public domain source code.</blockquote>
<p><a href="/contrib/download/extension-functions.c/download/DataGrid_DataSet_DataTable.rar?get=6">DataGrid_DataSet_DataTable.rar</a> (844.84&nbsp;KB)
contributed by Mike Willhite on 2004-12-10 23:24:34</p>
<blockquote>Example Code for working with DataSources, DataTables, DataGrids and SQLite3 in VB.NET with CoreLab SQLite.NET driver. </blockquote>
<p><a href="/contrib/download/extension-functions.c/download/idxchk?get=7">idxchk</a> (9761&nbsp;bytes)
contributed by tpoindex on 2005-02-16 21:07:33</p>
<blockquote>idxchk reports index usage for queries.  Can be used to help diagnose performance related problems.  See Wiki page for documenation and usage.  Version 1.0</blockquote>
<p><a href="/contrib/download/extension-functions.c/download/sqlite_wrapper_0.0.3.tar.gz?get=9">sqlite_wrapper_0.0.3.tar.gz</a> (7279&nbsp;bytes)
contributed by Ben.Clewett on 2005-06-02 13:34:59</p>
<blockquote>LiteWrap. Wrapper for SQLite. Simple API to return a query as table in memory. No lock left on database. Random access on returned data. Data may be kept indefinitelly. Contains several functions for displying/streaming result table.  Now with a simple shell.</blockquote>
<p><a href="/contrib/download/extension-functions.c/download/simple_sqlite_wrap.tar.gz?get=10">simple_sqlite_wrap.tar.gz</a> (23.14&nbsp;KB)
contributed by Joseph Wamicha on 2006-07-07 17:27:51</p>
<blockquote>simple_sqlite_wrap. The code extends sqlite so you are now able to execute sql statements off a file (see the how we use routes.sql in the example), return a recordset that is formatted into well defined rows and columns and execute a simple sql statement.</blockquote>
<p><a href="/contrib/download/extension-functions.c/download/sqlite.ico?get=11">sqlite.ico</a> (29.22&nbsp;KB)
contributed by Brannon King on 2006-07-18 17:14:49</p>
<blockquote>This is a Windows (non XP) icon file built from the logo using the "Real World Icon Editor" for compilation into the shell. Just add it as a resource to exe compiles.</blockquote>
<p><a href="/contrib/download/extension-functions.c/download/exeWtimer.zip?get=12">exeWtimer.zip</a> (203.86&nbsp;KB)
contributed by Brannon King on 2006-07-18 18:23:39</p>
<blockquote>This file contains a Windows exe of the sqlite3.exe utility. It is changed in that it has options (on by default) to output the time the query required. You can also shut off the output printing so that the timer does not include the time to render the text to the console. The shell.c (v1.144) is included as well. The shell.c should work on Linux as well, though it has not been tested.</blockquote>
<p><a href="/contrib/download/extension-functions.c/download/sqlite%2Btcc.tar.gz?get=13">sqlite+tcc.tar.gz</a> (4752&nbsp;bytes)
contributed by Christian Werner on 2006-08-22 17:46:25</p>
<blockquote>Experimental combination of SQLite 3.3.x and TinyCC 0.9.23
 using the new SQLite loadable extension mechanism.
 An extension module creates an SQLite scalar function
 'tcc_compile' which takes one argument which is a string
 made up of C source code to be on-the-fly compiled using
 TinyCC (www.tinycc.org). The SQLite API is visible during
 compilation when 'sqlite3.h' is included.
 So far, only partially tested on Linux i386.</blockquote>
<p><a href="/contrib/download/extension-functions.c/download/sqlite-networked.zip?get=18">sqlite-networked.zip</a> (636.60&nbsp;KB)
contributed by Dave Dyer on 2007-04-21 17:06:19</p>
<blockquote>This is a working demonstration of sqlite3 wrapped as
a client-server pair, based on an earlier implementation
for sqlite2 http://www.it77.de/sqlite/sqlite.htm.
This demo was developed and tested only under win32.
</blockquote>
<p><a href="/contrib/download/extension-functions.c/download/sqlite-java-shell-3.4.0.zip?get=19">sqlite-java-shell-3.4.0.zip</a> (845.13&nbsp;KB)
contributed by Joe Wilson on 2007-06-19 04:35:32</p>
<blockquote>100% pure java version of the sqlite3 command-line shell built with NestedVM. No shared libraries or DLLs required. This is not a JDBC driver.</blockquote>
<p><a href="/contrib/download/extension-functions.c/download/WINNERS_embedded_database+LAST+BETA+RELEASE.cpp?get=21">WINNERS_embedded_database LAST BETA RELEASE.cpp</a> (916.88&nbsp;KB)
contributed by Ettore Chiacchio on 2007-08-26 06:44:31</p>
<blockquote>I am working to a software project (WINNERS' Project) embedding a server web a database (starting from SQLite) and a content generator. So I am rewriting all sqlite in C++. I cleaned SQLite C code to obtain a more compact source code and a faster and shorter binary code before rewriting it in C++. This file, result of my efforts, is a "work in progress" to C++ so it is not intended to work (I have to debug final job) but and you can use any portion to substitute slower SQLite functions I improved.</blockquote>
<p><a href="/contrib/download/extension-functions.c/download/prettyreports.zip?get=23">prettyreports.zip</a> (3.43&nbsp;MB)
contributed by Grega Loboda on 2007-10-22 13:39:33</p>
<blockquote>Create reports on SQLite database. Pretty reports are freeware.</blockquote>
<p><a href="/contrib/download/extension-functions.c/download/idxchk.py?get=24">idxchk.py</a> (10.76&nbsp;KB)
contributed by Tom Lynn on 2008-03-07 23:46:27</p>
<blockquote>A Python port of idxchk. Requires pysqlite2, sqlite3 (comes with Python 2.5+) or apsw.</blockquote>
<p><a href="/contrib/download/extension-functions.c/download/extension-functions.c?get=25">extension-functions.c</a> (50.96&nbsp;KB)
contributed by Liam Healy on 2010-02-06 15:45:07</p>
<blockquote>Provide mathematical and string extension functions for SQL queries using the loadable extensions mechanism. Math: acos, asin, atan, atn2, atan2, acosh, asinh, atanh, difference, degrees, radians, cos, sin, tan, cot, cosh, sinh, tanh, coth, exp, log, log10, power, sign, sqrt, square, ceil, floor, pi. String: replicate, charindex, leftstr, rightstr, ltrim, rtrim, trim, replace, reverse, proper, padl, padr, padc, strfilter. Aggregate: stdev, variance, mode, median, lower_quartile, upper_quartile.
</blockquote>
</table></p><hr>
<form method="POST" action="/contrib/download/extension-functions.c">
Login to upload new files.
Userid: <input type="text" size="20" name="uid">
Password: <input type="password" size="20" name="pw">
<input type="submit" value="Login">
</form>
</body>
</html>
