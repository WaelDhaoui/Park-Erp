odoo.define('zarzis_park_website.rental', function (require) {
    "use strict";
    var ajax = require('web.ajax');
    var core = require('web.core');
    var Widget = require('web.Widget');

    if(document.querySelector("main div.oe_structure").classList.contains('rental_template')) {
        // Get the "add" button element
        let btn_add = document.querySelector("#add");

        // Get the backup table row element
        let tr_backup = document.querySelectorAll("tr")[1];

        // Function to delete a table row
        function delete_line() {
            // Get all the close tags (last td element) in each row
            let close_tags = document.querySelectorAll("tr > td:last-child");

            // Iterate over each close tag
            close_tags.forEach(function(close) {
                // Add click event listener to the close tag
                close.addEventListener("click", function(ele) {
                    // Remove the parent row when the close tag is clicked
                    close.parentElement.remove();

                    // Check if there are no more rows in the table body
                    if (document.querySelector("tbody").children.length == 0) {
                        // Create a new table cell for displaying "No shareholders" statement
                        let no_shareholders_statement = document.createElement('td');
                        no_shareholders_statement.textContent = "No shareholders";
                        no_shareholders_statement.setAttribute("colspan", "4");
                        no_shareholders_statement.setAttribute("style", "text-align: center; font-size: large; font-weight: 600;");

                        // Create a new table row to contain the statement
                        let no_shareholders_content = document.createElement('tr');
                        no_shareholders_content.classList.add("verify");
                        no_shareholders_content.append(no_shareholders_statement);

                        // Append the new row to the table body
                        document.querySelector("tbody").append(no_shareholders_content);
                    }
                });
            });
        }

        // Event listener for the "add" button click event
        btn_add.onclick = function() {
            let first_line;

            // Check if the first row is not a "No shareholders" row
            if (!document.querySelector("tbody").children[0].classList.contains("verify")) {
                first_line = document.querySelectorAll("tr")[1];
            } else {
                // Remove the "No shareholders" row and use the backup row
                document.querySelector("tbody").children[0].remove();
                first_line = tr_backup;
            }

            // Clone the first row and clear input values
            let copy_line = first_line.cloneNode(true);
            let inputs = copy_line.querySelectorAll('input.form-control');
            inputs.forEach(function(input) {
                input.value = "";
            });

            // Append the cloned row to the table body
            document.querySelector("tbody").append(copy_line);

            // Apply delete_line() to the new row
            delete_line();
        }

        // Call delete_line() initially to handle existing rows
        delete_line();


//        capital financing
        var input_capital = document.querySelector("main input#capital_company");
        var current_partners = document.querySelector("main input#current_partners");
        var total_financing = document.querySelector("main input#total_financing");
        var input_finance = document.querySelector("main input#capital_finance");

        input_capital.addEventListener('input',function() {
            if(total_financing.value == '')
                total_financing.value = 0
            if(current_partners.value == '')
                current_partners.value = 0
            input_finance.setAttribute("value", input_capital.value)
        });

//        total investment
        var total_investment = document.querySelector("main input#total_investment");
        var construction_equipments = document.querySelector("main input#construction_equipments");
        var imported_equipments = document.querySelector("main input#imported_equipments");
        var local_equipments = document.querySelector("main input#local_equipments");
        var means_transport = document.querySelector("main input#means_transport");
        var other_costs = document.querySelector("main input#other_costs");
        var working_capital = document.querySelector("main input#working_capital");

        if(total_investment.value == '')
            total_investment.value = 0
        if(means_transport.value == '')
            means_transport.value = 0
        if(other_costs.value == '')
            other_costs.value = 0
        if(local_equipments.value == '')
            local_equipments.value = 0
        if(working_capital.value == '')
            working_capital.value = 0
        if(imported_equipments.value == '')
            imported_equipments.value = 0
        if(construction_equipments.value == '')
            construction_equipments.value = 0
        if(total_investment.value == '')
            total_investment.value = 0

        document.querySelector("main form#rental").addEventListener('submit', function(event) {

            total_financing.setAttribute("value", parseInt(input_capital.value) + parseInt(current_partners.value));
            total_financing.value = parseInt(input_capital.value) + parseInt(current_partners.value)

            total_investment.setAttribute("value", parseInt(construction_equipments.value) + parseInt(imported_equipments.value) + parseInt(local_equipments.value) + parseInt(means_transport.value) + parseInt(other_costs.value) + parseInt(working_capital.value));
            total_investment.value = parseInt(construction_equipments.value) + parseInt(imported_equipments.value) + parseInt(local_equipments.value) + parseInt(means_transport.value) + parseInt(other_costs.value) + parseInt(working_capital.value)


            console.log(parseInt(total_investment.value))
            console.log(parseInt(total_financing.value))

            if(parseInt(total_financing.value) != parseInt(total_investment.value)) {
                //window.alert("Total investment must be equal to total financing")
                event.preventDefault();
                Swal.fire({
                  title: 'Total investment must be equal to total financing!',
                  icon: 'error',
                  confirmButtonText: 'Ok'
                })
            }
        });

    }

});
