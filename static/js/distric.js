var MCA = ["1st Year","2nd Year"];
var MTECH = ["1st Year","2nd Year"];
var BTECH = ["1st Year","2nd Year","3rd Year","4th Year"];


$("#inputState").change(function(){
  var Choosecourse = $(this).val();
  var optionsList;
  var htmlString = "";

  switch (Choosecourse) {
    case "MCA":
        optionsList = MCA;
        break;
    case "MTECH":
        optionsList = MTECH;
        break;
    case "BTECH":
        optionsList = BTECH;
        break;

}


  for(var i = 0; i < optionsList.length; i++){
    htmlString = htmlString+"<option value='"+ optionsList[i] +"'>"+ optionsList[i] +"</option>";
  }
  $("#inputDistrict").html(htmlString);

});