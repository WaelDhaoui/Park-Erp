odoo.define('zarzis_park_website.check', function (require) {
    "use strict";
    var ajax = require('web.ajax');
    var core = require('web.core');
    var Widget = require('web.Widget');

    if(document.querySelector("main div.oe_structure").classList.contains('check_template')) {

        if(document.querySelector("tbody").children.length == 0) {
        console.log("hello")
            let no_shareholders_statement = document.createElement('td')
            no_shareholders_statement.textContent = "No shareholders"
            no_shareholders_statement.setAttribute("colspan", "4")
            no_shareholders_statement.setAttribute("style", "text-align: center; font-size: large; font-weight: 600;")
            let no_shareholders_content = document.createElement('tr')
            no_shareholders_content.classList.add("verify")
            no_shareholders_content.append(no_shareholders_statement);
            document.querySelector("tbody").append(no_shareholders_content)
        }

        let btn_add = document.querySelector("#add")
        let tr_backup = document.querySelectorAll("tr")[1];

        function delete_line() {
            let close_tags = document.querySelectorAll("tr > td:last-child")
            close_tags.forEach(function(close) {
                close.addEventListener("click", function(ele) {
                    close.parentElement.remove();
                    if(document.querySelector("tbody").children.length == 0) {
                        let no_shareholders_statement = document.createElement('td')
                        no_shareholders_statement.textContent = "No shareholders"
                        no_shareholders_statement.setAttribute("colspan", "4")
                        no_shareholders_statement.setAttribute("style", "text-align: center; font-size: large; font-weight: 600;")
                        let no_shareholders_content = document.createElement('tr')
                        no_shareholders_content.classList.add("verify")
                        no_shareholders_content.append(no_shareholders_statement);
                        document.querySelector("tbody").append(no_shareholders_content)
                    }
                })
            })
        }

    }

});
