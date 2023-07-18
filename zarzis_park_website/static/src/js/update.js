odoo.define('zarzis_park_website.update', function (require) {
    "use strict";
    var ajax = require('web.ajax');
    var core = require('web.core');
    var Widget = require('web.Widget');

    if(document.querySelector("main div.oe_structure").classList.contains('update_request_template')) {
        // Check if there are no shareholders
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


    }

});
