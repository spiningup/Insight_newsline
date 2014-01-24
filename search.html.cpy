<!DOCTYPE html>
<html lang="en">
 <head>
   <meta charset="utf-8">
   <meta http-equiv="X-UA-Compatible" content="IE=edge">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <meta name="description" content="">
   <meta name="author" content="">

   <title>Newsline</title>

   <!-- Bootstrap core CSS -->
   <link href="static/css/bootstrap.css" rel="stylesheet">

   <!-- Custom styles for this template -->
   <link href="static/css/starter-template.css" rel="stylesheet">
   <link href="static/css/vertical-timeline.css" rel="stylesheet">

   <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
   <!--[if lt IE 9]>
     <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
     <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
   <![endif]-->

 </head>

 <body {% if query %} onload="queryURL('{{ query }}')" {% endif %}>


   <div class="container">
     <a href="/"><h1 class="splash-small">Newsline</h1></a>
     <h2 class="caption" style="font-size:1.5em">Your Portal to News with Context</h2>

     <div align="center">
       <div class="input-group">
	 <input style="width: 350px; height:43px; font-size:20px;" type="text" class="form-control" id="query" name="q">
	 <span class="input-group-btn">
	   </span>
	   <button style="height:43px; font-size:20px;margin-right:5px;" 
		   class="btn primary-button" onclick="visualize()"  id="timelinebut" type="button"
		   >Show Timeline</button>
	   <button style="height:43px; font-size:20px;" class="btn secondary-button" 
		   onclick="visualizesum()" id="summarybut" type="button"
		   >Top 10 Topics</button>
	 </span>
       </div><!-- /input-group -->

     </div>
   </div>
   



   <div align="center">
     <div id="hottopics" style="margin-top: 20px;">
     </div>
   </div>

   <div align="center">
     <div id="google-table" style=" width: 600px; height: 800px; margin-top: 20px;">
     </div>
   </div>


   <div class="timeline-jquery" style="width: 1100px; margin-top: 20px; margin-left: 20px; margin-right: 20px;"></div>


   <!-- Bootstrap core JavaScript
   ================================================== -->
   <!-- Placed at the end of the document so the pages load faster -->
   <script src="https://code.jquery.com/jquery-1.10.2.min.js"></script>
   <script type="text/javascript" src="static/js/bootstrap.min.js"></script>
   <script type="text/javascript" src="static/js/d3.v3.min.js"></script>
   <script type="text/javascript" src="static/js/tooltip.js"></script>

   <script type="text/javascript" src="static/js/libs/jquery-1.7.1.min.js"></script>
   <script type="text/javascript" src="static/js/libs/handlebars-1.0.rc.1.min.js"></script>
   <script type="text/javascript" src="static/js/libs/tabletop-zzolo.master-20130402.min.js"></script>
   <script type="text/javascript" src="static/js/libs/jquery.isotope.v1.5.21.min.js"></script>
   <script type="text/javascript" src="static/js/libs/jquery.ba-resize.v1.1.min.js"></script>
   <script type="text/javascript" src="static/js/libs/jquery.imagesloaded.v2.1.0.min.js"></script>
   <script type="text/javascript" src="static/js/jquery-veritcal-timeline.js"></script>
   
   <script type="text/javascript" src="static/js/google-timeline.js"></script>
   
   <script type="text/javascript" src="static/js/visualize2.js"></script>


 </body>
</html>
