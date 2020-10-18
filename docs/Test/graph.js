// goal1 graphs
google.charts.load("current", {
  packages: ["corechart", "table"],
});
google.charts.setOnLoadCallback(drawChart);

// Set a callback to run when the Google Visualization API is loaded.
var data1;

// Create the data table.
function drawChart() {
  // goal1 graph 1
  data1 = new google.visualization.arrayToDataTable([
    [
      "Region",
      "Proportion of women in managerial positions (%), by region, 2019",
      {
        role: "annotation",
      },
    ],
    ["Latin America and the Caribbean", 39, "39"],
    ["Australia and New Zealand", 38.06, "38.06"],
    ["Europe and Northern America", 37.75, "37.75"],
    ["Eastern and South-Eastern Asia", 32.1, "32.1"],
    ["Sub-Saharan Africa", 30.06, "30.06"],
    ["Oceania (exc. Australia and New Zealand)", 27.38, "27.38"],
    ["Central and Southern Asia", 13.23, "13.23"],
    ["Northern Africa and Western Asia", 11.75, "11.75"],
    ["", , ""],
    ["World", 27.89, "27.89"],
  ]);

  var options1 = {
    height: 280,
    annotations: {
      textStyle: {
        fontSize: 10,
      },
    },
    chartArea: {
      width: "60%",
      height: "100%",
      left: 200,
      top: 10,
      bottom: 40,
      right: 60,
    },
    colors: ["#F36E24"],
    bar: {
      groupWidth: "90%",
    },
    legend: "none",
    annotations: {
      alwaysOutside: false,
      textStyle: {
        fontSize: 9,
        color: "#FFFFFF",
      },
    },
    fontSize: 11,
    bars: "horizontal", // Required for Material Bar Charts.
    hAxis: {
      ticks: [0, 10, 20, 30, 40, 50],
    },
  };

  var chart1 = new google.visualization.BarChart(
    document.getElementById("na1_g1")
  );
  chart1.draw(data1, options1);

  // End graph 1
}
//http://stackoverflow.com/questions/17853248/google-visualization-datatable-to-csv-download

function downloadCSV(filename, data) {
  jsonDataTable = data.toJSON();
  var jsonObj = eval("(" + jsonDataTable + ")");
  output = JSONObjtoCSV(jsonObj, ",");
}

function JSONObjtoCSV(jsonObj, filename) {
  filename = filename || "test.csv";
  var body = "";
  var j = 0;
  var columnObj = [];
  var columnLabel = [];
  var columnType = [];
  var columnRole = [];
  var outputLabel = [];
  var outputList = [];
  for (var i = 0; i < jsonObj.cols.length; i++) {
    columnObj = jsonObj.cols[i];
    columnLabel[i] = columnObj.label;
    columnType[i] = columnObj.type;
    columnRole[i] = columnObj.role;
    if (columnRole[i] == null) {
      outputLabel[j] = '"' + columnObj.label + '"';
      outputList[j] = i;
      j++;
    }
  }
  body += outputLabel.join(",") + String.fromCharCode(13);

  for (var thisRow = 0; thisRow < jsonObj.rows.length; thisRow++) {
    outputData = [];
    for (var k = 0; k < outputList.length; k++) {
      var thisColumn = outputList[k];
      var thisType = columnType[thisColumn];
      thisValue = jsonObj.rows[thisRow].c[thisColumn].v;
      switch (thisType) {
        case "string":
          outputData[k] = '"' + thisValue + '"';
          break;
        case "datetime":
          thisDateTime = eval("new " + thisValue);
          outputData[k] =
            '"' +
            thisDateTime.getDate() +
            "-" +
            (thisDateTime.getMonth() + 1) +
            "-" +
            thisDateTime.getFullYear() +
            " " +
            thisDateTime.getHours() +
            ":" +
            thisDateTime.getMinutes() +
            ":" +
            thisDateTime.getSeconds() +
            '"';
          delete window.thisDateTime;
          break;
        default:
          outputData[k] = thisValue;
      }
    }
    body += outputData.join(",");
    body += String.fromCharCode(13);
  }

  uri = "data:text/csv;filename=download.csv," + encodeURIComponent(body);
  //newWindow=downloadWithName(uri, 'download.csv');

  if (msieversion()) {
    var IEwindow = window.open();
    IEwindow.document.write(body);
    IEwindow.document.close();
    IEwindow.document.execCommand("SaveAs", true, "download.csv");
    IEwindow.close();
  } else {
    //var uri = 'data:application/csv;charset=utf-8,' + escape(body); //  "data:text/csv;filename=download.csv," + encodeURIComponent(body); //'data:application/csv;charset=utf-8,' + escape(body);
    //newWindow=downloadWithName(uri, 'download.csv');
    var link = document.createElement("a");
    link.download = "download.csv"; //name;
    link.href = uri;
    document.body.appendChild(link);

    link.click();
    document.body.removeChild(link);
  }

  return body;
}

function msieversion() {
  var ua = window.navigator.userAgent;
  var msie = ua.indexOf("MSIE ");
  if (msie != -1 || !!navigator.userAgent.match(/Trident.*rv\:11\./)) {
    // If Internet Explorer, return version number
    return true;
  } else {
    // If another browser,
    return false;
  }
  return false;
}

$(window).resize(function () {
  drawChart();
});

$(document).ready(function () {
  $("#table_div1").hide();
  $("#table_div2").hide();
  $("#table_div3").hide();
  $("#table_div4").hide();
  //$("#goal8_table_g5").hide();

  $(".table1").click(function () {
    var $this = $(this);
    $this.toggleClass("table1");

    if ($this.hasClass("table1")) {
      $this.text("Show Data");
      $("#table_div1").toggle("hide");
    } else {
      $this.text("Hide Data");
      $("#table_div1").toggle("show");
    }
  });
  $(".table2").click(function () {
    var $this = $(this);
    $this.toggleClass("table2");

    if ($this.hasClass("table2")) {
      $this.text("Show Data");
      $("#table_div2").toggle("hide");
    } else {
      $this.text("Hide Data");
      $("#table_div2").toggle("show");
    }
  });
  $(".table3").click(function () {
    var $this = $(this);
    $this.toggleClass("table3");

    if ($this.hasClass("table3")) {
      $this.text("Show Data");
      $("#table_div3").toggle("hide");
    } else {
      $this.text("Hide Data");
      $("#table_div3").toggle("show");
    }
  });
  $(".table4").click(function () {
    var $this = $(this);
    $this.toggleClass("table4");

    if ($this.hasClass("table4")) {
      $this.text("Show Data");
      $("#table_div4").toggle("hide");
    } else {
      $this.text("Hide Data");
      $("#table_div4").toggle("show");
    }
  });
});
