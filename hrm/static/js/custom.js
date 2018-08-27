/**
 * Created by huongnm on 31/10/2017.
 */

$( document ).ready(function() {
    //
    // $('input').tagsinput({
    //     confirmKeys: [32],
    //
    // });
    // $('#ava-filechooser').change( function(event) {
    //     var tmppath = URL.createObjectURL(event.target.files[0]);
    //     $("#temppath").html("Temporary Path --> <strong>["+tmppath+"]</strong>");
    //     // alert(document.getElementById('ava-filechooser').value)
    //
    // });

    $('.skillbar-title').css('background', getRandomColor());

    $('#chart-container').orgchart({
        'data' : $('#datasource'),
        'pan': true,
         // 'direction': 't2b',
        'zoom': true
    });

});

$(document).keypress(function () {
    if (event.which == 13) {
        event.preventDefault();
        // console.log($('#receiver').val());
        console.log($('#receiver').tagsinput('items'));
    }
});

function getRandomColor(){
 var color =  "#" + (Math.random() * 0xFFFFFF << 0).toString(16);
 return color;
}

function sentPass(){
    document.getElementById("mess").innerHTML ='We just sent a message to the email you provided with a link to reset your password. Please check your inbox and follow the instructions in the email.'
    document.getElementById("forgot-pass-header").innerHTML = "Sent!"
    document.getElementById('formarea').style.display = 'none'
}
function showChangePassForm() {
   $("#id-changepass").toggle();
   document.getElementById('id-editinfo').style.display= "none";
}
function showEditInfoForm() {
   $("#id-editinfo").toggle();
}

action = document.getElementById("update-relationship").action;
function showUpdateRelaForm() {
    id = event.currentTarget.id.split("-")[1]
    name = event.currentTarget.childNodes[3].textContent
    rela = event.currentTarget.childNodes[5].textContent

    document.getElementById("id_name").value = name
    document.getElementById("id_rela_name").value = rela

    form = document.getElementById("update-relationship")
    form.action = action + id

    document.getElementById('id-editrela').style.display = "block";
    document.getElementById('id-addrela').style.display = "none"
}

function showAddRelaForm() {
   $("#id-addrela").toggle();
   if(document.getElementById("add-rela").textContent=="+"){
       document.getElementById("add-rela").textContent="-";

   }
   else {

       document.getElementById("add-rela").textContent="+";
   }

}

function showSkillExp(x){
    // span_year_id = 'exp-'+  (event.target).id.split("-")[1]
    duration_id = 'exp-'+  x.id.split("-")[1]
    start_id = 'start-' + x.id.split("-")[1]
    end_id = 'end-' + x.id.split("-")[1]
    var start = document.getElementById(start_id).innerHTML
    var end = document.getElementById(end_id).innerHTML
    start_date = new Date(start)
    end_date = new Date(end)
    diffdays = Math.round((end_date-start_date)/(1000*60*60*24))
    diffmonth = Math.round(diffdays/30)
    diffyear = Math.round(diffdays/365)
    // document.getElementById(duration_id).style.display = "block"

    if(diffdays < 31) {
        document.getElementById(duration_id).innerHTML = diffdays + " day(s)"
    }else if(diffmonth <10){
        document.getElementById(duration_id).innerHTML = diffmonth + " month(s)"
    }else{
        document.getElementById(duration_id).innerHTML =  diffyear + " year(s)"
    }
    // $( "#"+duration_id ).slideDown(800);
    $('#'+duration_id).show();

}

function skillmouseout(x){
    duration_id = 'exp-'+  x.id.split("-")[1]
    $('#'+duration_id).hide()
}

function showChangeSkillForm() {
    document.getElementById('id-editskill').style.display = "block";
    document.getElementById('id-addskill').style.display= "none";
    var ele = event.target;
    console.log(ele.innerHTML);
    document.getElementById('skill-name').innerHTML = ele.innerHTML
    var form = document.getElementById("update-skill-form")
    id = ele.id.split("-")[1]
    form.action += "?id="+id
    start_id = 'start-' + ele.id.split("-")[1]
    end_id = 'end-' + ele.id.split("-")[1]
    var start = document.getElementById(start_id).innerHTML
    var end = document.getElementById(end_id).innerHTML
    start_date = new Date(start)
    end_date = new Date(end)
    var select_month_st = document.getElementById('id_date_start_month')
    var select_day_st = document.getElementById('id_date_start_day')
    var select_year_st = document.getElementById('id_date_start_year')
    select_month_st.options[start_date.getMonth()].selected = "true"
    select_day_st.options[start_date.getDate()-1].selected = "true"
    select_year_st.options[start_date.getFullYear()-1900].selected = "true"
    var select_month_end = document.getElementById('id_date_end_month')
    var select_day_end = document.getElementById('id_date_end_day')
    var select_year_end = document.getElementById('id_date_end_year')
    select_month_end.options[end_date.getMonth()].selected = "true"
    select_year_end.options[end_date.getFullYear()-1900].selected = "true"
    select_day_end.options[end_date.getDate()-1].selected = "true"
}
function showAddSkillForm() {
    $("#id-addskill").toggle();
    if(document.querySelector('#add-skill').textContent=="+"){
        document.querySelector('#add-skill').textContent="-";
    }
    else {
        document.querySelector('#add-skill').textContent="+";
    }
}

function showChangeEduForm() {
    document.getElementById('id-editedu').style.display = "block";
    document.getElementById('id-addedu').style.display= "none";
    var ele = event.target;
    console.log(ele.id)
    document.getElementById('edu-name').innerHTML = ele.innerHTML
    var form = document.getElementById("update-edu-form")
    id = ele.id.split("-")[1]
    form.action += "?id="+id
    degree_id = 'edudegree-'+ ele.id.split("-")[1]
    console.log(degree_id)
    start_id = 'edustart-' + ele.id.split("-")[1]
    end_id = 'eduend-' + ele.id.split("-")[1]
    var degree = document.getElementById(degree_id).innerHTML
    var start = document.getElementById(start_id).innerHTML
    var end = document.getElementById(end_id).innerHTML
    start_date = new Date(start)
    end_date = new Date(end)
    console.log(degree)
    var degree_index = ['Kindergarden','Primary School','Secondary School','High School', 'Bachelor','Master','PhD']
    var select_degree = document.getElementById('id_degree')

    select_degree.options[degree_index.indexOf(degree)].selected = "true"
    var select_m_st = document.getElementById('id_start_month')
    var select_d_st = document.getElementById('id_start_day')
    var select_y_st = document.getElementById('id_start_year')
    select_m_st.options[start_date.getMonth()].selected = "true"
    select_d_st.options[start_date.getDate()-1].selected = "true"
    select_y_st.options[start_date.getFullYear()-1900].selected = "true"
    var select_m_end = document.getElementById('id_end_month')
    var select_d_end = document.getElementById('id_end_day')
    var select_y_end = document.getElementById('id_end_year')
    select_m_end.options[end_date.getMonth()].selected = "true"
    select_y_end.options[end_date.getFullYear()-1900].selected = "true"
    select_d_end.options[end_date.getDate()-1].selected = "true"
}
function showAddEduForm() {
   document.getElementById('id-addedu').style.display = "block";
   document.getElementById('id-editedu').style.display= "none"
}

function showAttachment(){
    var name = document.getElementById('fileInput');
    document.getElementById('help-block').innerHTML = name.files.item(0).name;
}

function uploadDocument() {
    input = document.getElementById('fileInput')
    csrf_input = document.querySelector('[name="csrfmiddlewaretoken"]');
    input.click()
    $("#fileInput").change(function(){

        var formData = new FormData();
        formData.append("document", input.files[0]);
        var request = new XMLHttpRequest();
         request.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                obj = JSON.parse(this.responseText);
                var wrapper = document.createElement('span');
                wrapper.innerHTML= obj["element"];

                document.querySelector("div.timeline-body").appendChild(wrapper)
    }
  };
        request.open("POST", "http://localhost:8025/add-document/", true);
        console.log(csrf_input.name)
        request.setRequestHeader("X-CSRFToken", csrf_input.value)
        request.send(formData);
        $("#fileInput").off('change');

    });

}