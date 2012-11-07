
hudsonURL = 'http://paris.urbansim.org:8080/hudson/job/MTC_Model';
reportURL = 'http://paris.urbansim.org/MTC_Model';
opusRestURL = 'http://paris.urbansim.org/opus/rest';

function sortBuilds(sortFunction) {
  var mylist = $('#builds');
  var listitems = mylist.children('div').get();
  listitems.sort(sortFunction);
  $.each(listitems, function(idx, itm) {
    mylist.append(itm);
  });
}

function sortByUrbansimBuildAscending() {
  sortBuilds(function(a, b) {
    var compA = $(a).data("build").urbansimNumber;
    var compB = $(b).data("build").urbansimNumber;
    return (compA > compB) ? -1 : (compA < compB) ? 1 : 0;
  });
}

function sortByBuildStatus() {
  var orderedStatus = {"RUNNING":0, "SUCCESS":1, "FAILURE":2, "ABORTED":3};
  sortBuilds(function(a, b) {
    var compA = orderedStatus[$(a).data("build").status];
    var compB = orderedStatus[$(b).data("build").status];
    return (compA < compB) ? -1 : (compA > compB) ? 1 : 0;
  });
}

function createXMLHttpRequest() {
  var xmlHttp = false;
  if(window.ActiveXObject) {
    xmlhttp = new ActiveXObject('Microsoft.XMLHTTP');
  } else if(window.XMLHttpRequest) {
    xmlhttp = new XMLHttpRequest();
  } else {
    alert('Your browser is not supported.');
  }
  return xmlhttp;
}

var xmlhttp = null;

// Ugh.  We're really gonna need a proper state machine.
var cancel = false;

function cancelAll() {
  cancel = true;
  if (xmlhttp) {
      xmlhttp.onreadystatechange = function() {};
	  xmlhttp.abort();
  }
}

function getBuildNumber(buildURL, callback) {
  // We must user our own XMLHttpRequest because we want to parse data as it
  // comes in.  The reason for this is that the raw console log is often HUGE,
  // so we want to abort after detecting the urbansim build number.
  xmlhttp = createXMLHttpRequest();
  xmlhttp.onreadystatechange = function() {
	if (xmlhttp.readyState == 3 && xmlhttp.responseText.length > 1024*1024) {
      // give up if the first 1MB of text don't have what we're looking for
      xmlhttp.onreadystatechange = function() {};
	  xmlhttp.abort();
      if (callback != null) {
        callback(-1);
      }
    } else if (xmlhttp.readyState == 3) {
      // if this run was a new run, we'll see the line where the cache
      // directory was created.
	  var magicString = 'Cache directory for run ';
	  var i = xmlhttp.responseText.indexOf(magicString);
      if (i < 0) {
        // if this run was a re-launch, we rely on the HUDSON_RESTART_RUN
        // environment var
        magicString = 'HUDSON_RESTART_RUN=';
	    i = xmlhttp.responseText.indexOf(magicString);
        if (i < 0)
          return;
      }
	  i = i + magicString.length;
	  urbansimNumber = xmlhttp.responseText.substring(i, i + 20).split('\n')[0].split(' ')[0];
      xmlhttp.onreadystatechange = function() {};
	  xmlhttp.abort();
	  console.log('Found urbansim run number ' + urbansimNumber);
      if (callback != null) {
        callback(urbansimNumber);
      }

    } else if (xmlhttp.readyState == 4) {
      // This is the case where the console log did not have any evidence of
      // the urbansim build number.  This probably happened because the job was
      // canceled before urbansim ran.
      if (callback != null) {
        callback(0);
      }
	}
  };
  xmlhttp.open('GET', buildURL + '/consoleText', true);
  xmlhttp.send(null);
}

// get urbansim run data.  Note that this data comes from opus_rest, not from
// hudson.  Accordingly, it has much more information on the run, including
// whatever is available in the configuration resources.  Note that we call the
// callback on success or failure because opus_rest is under development and
// may occasionally fail.  Anyway, callbacks should check for possible null
// response.
function getUrbansimRun(runURL, callback) {
  $.ajax({
    url: runURL,
    dataType: 'json',
    data: null,
    success: function (run) {
      callback(run);
    },
    error: function () {
      console.log("Failed to fetch opus run from " + runURL);
      callback(null);
    }
  });
}

function getBuild(buildURL, callback) {
  getBuildNumber(buildURL, function (urbansimNumber) {
    if (urbansimNumber == -1) {
      console.log("Failed to get urbansim build number");
      return;
    }
    if (urbansimNumber == 0) {
      callback(null);
      return;
    }
    url = buildURL + '/api/json';
    $.ajax({
      url: url,
      data: null,
      dataType: 'json',
      success: function(build) {
        build.urbansimNumber = urbansimNumber;
	    $.each(build.actions, function (key, val) {
		  if (typeof val.parameters == "undefined")
		    return;
		  $.each(val.parameters, function(key, val) {
		    build[val.name] = val.value;
		  });
	    });
        getUrbansimRun(opusRestURL + '/' + urbansimNumber + '/', function (run) {
          build.urbansimRun = run;
	      callback(build);
        });
      },
      error: function() {
        console.log("Hmm.  Failed to get " + this.url);
      }
    });
  });
}

function escapeHTML(t) {
  return $('<div/>').text(t).html();
}

var numBuilds = 0;
var MAX_BUILDS = 20;
var currentBuild;

function getNextBuild() {
  if (numBuilds < MAX_BUILDS && currentBuild > 0) {
    currentBuild--;
    getBuild(hudsonURL + '/' + currentBuild, addBuild);
  }
}

function addBuild(build) {
  if (cancel)
    return;
  if (!build) {
    getNextBuild();
    return;
  }
  build.status = build.result;
  if (build.building)
    build.status = 'RUNNING';

  e = $('#run' + build.urbansimNumber + " .hudsonNumber");
  if (e.length != 0 && e.text() > build.number) {
	console.log("It appears that " + build.number + " is an older build for run " + build.urbansimNumber);
    getNextBuild();
	return;
  }
  numBuilds++;
  title = '<a href="#">UrbanSim Run #' + build.urbansimNumber + ': ' +
	'<span class="hudsonNumber" style="display:none">' + build.number + '</span>' +
	'<span>' + build.HUDSON_SCENARIO + '</span>' + ' | ' + 
	'<span id="status"> ' + build.status + '</span>' + ' | ' +
        '<span>' + build.id + '</span> </a>';
  build.reportURL = reportURL + '/' + build.HUDSON_SCENARIO + '/run_' + build.urbansimNumber;
  if (typeof build.HUDSON_SCENARIO == "undefined" || build.HUDSON_COMMENT == "")
    build.HUDSON_COMMENT = "(no description available)";

  dataLocation = "&lt;unavailable&gt;";
  if (build.urbansimRun)
    dataLocation = build.urbansimRun.hudson_details.node + ':' + build.urbansimRun.cache_directory;

  body = 
    '<ul>' +
    '<li><b>Travel Model:</b> ' + build.HUDSON_TRAVEL_MODEL + '</li>' +
    '<li><b>Go to the </b> <a href="' + build.url + 'console">hudson page</a></li>' +
    '<li><b>Go to the </b> <a href="' + build.reportURL + '">report page</a></li>' +
    '<li><b>Comment:</b> ' + escapeHTML(build.HUDSON_COMMENT) + '<li>' +
    '<li><b>Post-Run Analysis:</b> ' + escapeHTML(build.description) + '<li>' +
    '<li><b>Data location:</b> ' + dataLocation;

  html = '<h3>' + title + '</h3><div>' + body + '</div>';
  if (e.length != 0) {
	$('#run' + build.urbansimNumber).html(html);
	$('#builds').accordion('destroy').accordion({header: "h3"});
  } else {
    html = '<div id=run' + build.urbansimNumber + '>' + html + '</div>';
	$('#builds').append(html).accordion('destroy').accordion({header: "h3"});
  }
  $('#run' + build.urbansimNumber).data("build", build);

  // fetch builds until we have MAX_BUILDS.
  getNextBuild();
}

function getBuilds() {
  cancel = false;
  getBuild(hudsonURL + '/lastBuild', function(build) {
    currentBuild = build.number;
    addBuild(build);
  });
}

function getNextPage() {
  cancelAll();
  $('#builds').empty();
  cancel = false;
  numBuilds = 0;
  getNextBuild();
}

$(function() {
  $("#builds").accordion({header: "h3"});
  getBuilds();
});
