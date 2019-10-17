$(function(){
    $.ajax({
        url:"/api/ajax_all_sp",
        type:"POST",
        dataType:"json",
        success:function(data){
            var sp_data = data['SP_List']
            for(var i=0;i<sp_data.length;i++){
                var opt = $("<option value=" + sp_data[i] + ">" + sp_data[i] + "</option>")
                $("#sp").append(opt);
            }
        },
        error:function(XMLHttpRequest, textStatus, errorThrown){
            alert("error");
            //console.log("query sp list error");
        }
    });

    $('#table_div').jtable({
        title: 'Data Center',
        paging: true,
        sorting: true,
        pageSize: 20,
        defaultSorting: 'jira_id ASC',
        actions: {
            listAction: '/api/ajax_triage_list',
            //deleteAction: '/api/ajax_triage_dalete',
            //updateAction: '/api/ajax_triage_update',
            createAction: '/api/ajax_triage_create'
        },
        fields: {
            jira_id: {
                title:'JRID',
                key: true,
                create: false,
                edit: false,
                list: true
            },
            jira_status: {
                title: 'JRStatus',
                width: '9%'
            },
            sp_name: {
                title: 'SP',
                width: '9%',
                //options: { 'M': 'Male', 'F': 'Female' }
            },
            predict_prob: {
                title: 'PredProb',
                width: '9%',
                //options: '/Demo/GetCityOptions'
            },
            predict_cr: {
                title: 'PredCR',
                width: '9%',
                //type: 'date',
                //displayFormat: 'yy-mm-dd'
            },
            predict_area: {
                title: 'PredArea',
                width: '9%',
                //type: 'date',
                //displayFormat: 'yy-mm-dd'
            },
            predict_status: {
                title: 'PredStatus',
                width: '9%',
                //type: 'date',
                //displayFormat: 'yy-mm-dd'
            },
            predict_low: {
                title: 'PredLow',
                width: '9%',
                //type: 'date',
                //displayFormat: 'yy-mm-dd'
            },
            predict_cr_hit: {
                title: 'PredCrHit',
                width: '9%',
                //type: 'date',
                //displayFormat: 'yy-mm-dd'
            },
            predict_area_hit: {
                title: 'PredAreaHit',
                width: '9%',
                //type: 'date',
                //displayFormat: 'yy-mm-dd'
            },
            actual_cr: {
                title: 'ActualCR',
                width: '9%',
                //type: 'checkbox',
                //values: { 'false': 'Passive', 'true': 'Active' },
                //defaultValue: 'true'
            },
            actual_area: {
                title: 'ActualArea',
                width: '9%',
                //type: 'date',
                //displayFormat: 'yy-mm-dd'
            },
            actual_status: {
                title: 'ActualStatus',
                width: '9%',
                //type: 'date',
                //displayFormat: 'yy-mm-dd'
            },
            update_time: {
                title: 'UpdateTime',
                width: '9%',
                //type: 'date',
                //displayFormat: 'yy-mm-dd'
            },
            Demo_RecordDate: {
                title: 'Record date',
                width: '9%',
                type: 'date',
                displayFormat: 'dd.mm.yy',
                create: false,
                edit: false,
                list:false,
                sorting: false //This column is not sortable!
            },
            Demo: {
                title: 'demo',
                list: false,
                //type: 'radiobutton',
                //options: { '1': 'Primary school', '2': 'High school', '3': 'University' }
            },
            Demo_Password: {
                title: 'User Password',
                type: 'password',
                list: false
            },
            Demo_EmailAddress: {
                title: 'Email address',
                list: false
            }
        },

        rowInserted:function(event, data){
            console.log("insert....");
        },

        loadingRecords:function(event, data){
            //console.log(event.target);
            console.log("loading....");
        },

        recordsLoaded:function(event, data){
            //console.log("This is event capture");
            $.each($("#table_div").find("td"),function(){
                $(this).attr("title",$(this).text())
            });

            var tb_width = $("table").css("width");
            $(".jtable-title").css("width",tb_width);
            $(".jtable-bottom-panel").css("width",tb_width);
        }
    });

    //Re-load records when user click 'load records' button.
    $('#LoadRecordsButton').click(function (e) {
        e.preventDefault();
        $('#table_div').jtable('load', {
            sp: $('#sp').val(),
            //cityId: $('#cityId').val()
        },function(){
            $.each($("#table_div").find("td"),function(){
                $(this).attr("title",$(this).text())
            });
        });
    });

    //Load all records when page is first shown
    $('#table_div').jtable('load',{},function(){
        $.each($("#table_div").find("td"),function(){
            $(this).attr("title",$(this).text())
        });

        var tb_width = $("table").css("width");
        $(".jtable-title").css("width",tb_width);
        $(".jtable-bottom-panel").css("width",tb_width);
    });

    //$('#LoadRecordsButton').click();

});