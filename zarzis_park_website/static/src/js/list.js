odoo.define('mini_project.list', function (require) {
    "use strict";
    var ajax = require('web.ajax');
    var core = require('web.core');
    var Widget = require('web.Widget');

    let contact_button = document.querySelector(".oe_structure_solo")
    contact_button.style.display = "none"


    let header_li = document.querySelector("#top_menu li")
    header_li.parentElement.style.cssText = "align-items: center;"
    header_li.style.cssText = "margin-left: auto; font-weight: 700; font-size: larger;"

    document.querySelector("path").style.fill = "#d0d4d7"

    if(document.querySelector("main div.oe_structure").classList.contains('local_list_class')) {
        var form = document.querySelector("main .search_div");
        form.onsubmit = function(e) {
            e.preventDefault();
        }

        // how many cards for each status
        function calc_cards_status() {
            let num_cards_status = document.querySelectorAll(".search_div .filter div");
            let cards_num = document.querySelectorAll('.local_list_class .container_all_containers_list > .container');
            let num;
            cards_num.forEach(function(c,i) {
                num = 0;
                let calc_card = c.querySelectorAll("a.card");
                for(let i=0;i<calc_card.length;i++) {
                    if(getComputedStyle(calc_card[i]).display == "flex")
                        num++;
                }
                num_cards_status[i].firstElementChild.innerHTML = "("+num+")";
                if(num == 0) {
                    if(!c.firstElementChild.classList.contains("error")) {
                        let p = document.createElement("p");
                        p.className = "error"
                        p.innerHTML = "No local Found";
                        p.style.cssText = "position: absolute; left: 50%; top: 35%; transform: translate(-50%, -50%); font-size: xx-large; opacity: 0.8; text-align: center;";
                        c.prepend(p);
                    }
                    c.querySelector(".bullets").parentElement.style.display = "none";
                } else {
                    if(c.firstElementChild.classList.contains("error"))
                        c.firstElementChild.remove();
                    c.querySelector(".bullets").parentElement.style.display = "flex";
                }
            });
        }
        //replace displayed cards
        function replace_displayed_cards() {
            let allContainer = document.querySelectorAll('.local_list_class .container_all_containers_list > .container');
            allContainer.forEach(function(container) {
                let containerAll = container.querySelectorAll(".list");
                let i=0;
                let j=containerAll.length - 1;
                while(i<j) {
                    let front_cards = containerAll[i].children;
                    for(let k=0; k<front_cards.length; k++) {
                        if(getComputedStyle(front_cards[k]).display == "none") {
                            let back_cards = containerAll[j].children;
                            for(let d=0; d<back_cards.length; d++) {
                                if(getComputedStyle(back_cards[d]).display == "flex") {
                                    let tmp1 = front_cards[k].cloneNode(true);
                                    let tmp2 = back_cards[d].cloneNode(true);
                                    front_cards[k].replaceWith(tmp2);
                                    back_cards[d].replaceWith(tmp1);
                                    break;
                                }
                            }
                            break;
                        }
                    }
                    i++;
                    j--;
                }
            });

        }
        //style each list
        function style_list() {
            let allContainer = document.querySelectorAll('.local_list_class .container_all_containers_list > .container');
            allContainer.forEach(function(list_container,k) {
                let bullets =  list_container.querySelectorAll(".bullets");
                list_container.querySelectorAll(".list").forEach(function(list,i) {
                    if(i == 0) {
                        list.style.left = "20px";
                        list.classList.add("active");
                        bullets[i].classList.add("active");
                    } else {
                        list.style.left = "1500px";
                        list.classList.remove("active");
                        bullets[i].classList.remove("active");
                    }
                    replace_displayed_cards();
                    let num = 0;
                    for(let j=0;j<list.children.length;j++) {
                        if(getComputedStyle(list.children[j]).display == "flex")
                            num++;
                    }
                    if(num >=0 && num <=4)
                        list.style.gridTemplateRows = "repeat(1,280px)";
                    else if(num >=5 && num <=8)
                        list.style.gridTemplateRows = "repeat(2,280px)";
                    else
                        list.style.gridTemplateRows = "repeat(3,280px)";
                });
            });
        }
        // set pagination
        function set_pagination() {
            let active_list_container = [...document.querySelector(".local_list_class .container_all_containers_list > .active").querySelectorAll("ul .bullets")];
            let prev = document.querySelectorAll(".local_list_class .container_all_containers_list > .active .page-link")[0];
            let next = document.querySelectorAll(".local_list_class .container_all_containers_list > .active .page-link")[document.querySelectorAll(".local_list_class .container_all_containers_list > .active .page-link").length - 1];
            let num = 0;
            active_list_container[0].classList.contains("active") ? prev.classList.add("disabled") : prev.classList.remove("disabled");
            active_list_container[active_list_container.length - 1].classList.contains("active") ? next.classList.add("disabled") : next.classList.remove("disabled");
            active_list_container.forEach(function(li) {
                if(getComputedStyle(li).display == "list-item")
                    num++;
            });
            if(num == 0 || num == 1) {
                active_list_container[0].parentElement.lastElementChild.setAttribute("style", "display: none;");
                active_list_container[0].parentElement.firstElementChild.setAttribute("style", "display: none;");
                active_list_container[0].style.borderRadius = "50%";
            } else {
                active_list_container[0].parentElement.lastElementChild.setAttribute("style", "display: block;");
                active_list_container[0].parentElement.firstElementChild.setAttribute("style", "display: block;");
                active_list_container[0].style.borderRadius = "0";
            }
            prev.onclick = function() {
                for(let i=0; i<active_list_container.length; i++) {
                    if(active_list_container[i].classList.contains("active") && i != 0)
                        active_list_container[i-1].click();
                }
            }
            next.onclick = function() {
                for(let i=0; i<active_list_container.length; i++) {
                    if(active_list_container[i].classList.contains("active") && i != active_list_container.length - 1)
                        active_list_container[i+1].click();
                }
            }
        }
        // set height list container
        function set_height_container() {
            let allContainer = document.querySelectorAll('.local_list_class .container_all_containers_list > .container');
            let container_all_containers_list = document.querySelector('.local_list_class .container_all_containers_list > .active');
            allContainer.forEach(function(list_container) {
                list_container.style.height = parseInt(getComputedStyle(list_container.querySelector(".active")).height)+ 150 + "px";
            });
            container_all_containers_list.parentElement.style.height = parseInt(container_all_containers_list.style.height) + "px";
        }
        //set position bullets
        function position_bullets() {
            let allContainer = document.querySelectorAll('.local_list_class .container_all_containers_list > .container');
            allContainer.forEach(function(list_container) {
                list_container.lastElementChild.style.top = parseInt(getComputedStyle(list_container.querySelector(".active")).height)+ 75 + "px";
                list_container.lastElementChild.style.transition = "0.5s";
            });
        }
        //change bullets active and list positions with click bullets
        function activate_bullets_list() {
            let allContainer = document.querySelectorAll('.local_list_class .container_all_containers_list > .container');
            let bullets = [...document.querySelectorAll(".local_list_class .bullets")];

            allContainer.forEach(function(cont) {
                let bullets = cont.querySelectorAll(".bullets");

                bullets.forEach(function(e,i) {
                    e.onclick = function() {
                        for(let i=0; i<bullets.length; i++) {
                            bullets[i].classList.remove("active");
                        }
                        e.classList.add("active");

                        // cards
                        allContainer.forEach(function(cont) {
                            if(cont.children.length >= 3) {
                                let allList = cont.querySelectorAll(".list");
                                allList.forEach(function(list,j) {
                                    if(j>i) {
                                        list.style.left = "1500px";
                                    } else if(j<i){
                                        list.style.left = "-1500px";
                                        list.classList.remove("active");
                                    } else {
                                        list.style.left = "20px";
                                        list.classList.add("active");
                                        // set scrollY
                                        if(list.children.length >=1 && list.children.length <=4) {
                                            scrollTo({left: 0,top: 220,"behavior": "smooth"});
                                        }
                                        else if(list.children.length >=5 && list.children.length <=8) {
                                            scrollTo({left: 0,top: 520,"behavior": "smooth"});
                                        }
                                        else
                                        {
                                            scrollTo({left: 0,top: 780,"behavior": "smooth"});
                                        }
                                    }
                                })
                            }
                        });
                        set_height_container();
                        position_bullets();
                        set_pagination();
                    }
                });
            });
        }

        //////////////////// Begin Search Bar
        function verify_list() {
            let allContainer = document.querySelectorAll('.local_list_class .container_all_containers_list > .container');
            allContainer.forEach(function(list_container) {
                let allList = list_container.querySelectorAll(".list");
                let bullets = list_container.querySelectorAll(".bullets");

                allList.forEach(function(list,i) {
                    let num = 0;
                    for(let j=0;j<list.children.length;j++) {
                        if(getComputedStyle(list.children[j]).display == "flex")
                            num++;
                    }
                    if(num == 0) {
                        bullets[i].style.display = "none";
                    } else
                        bullets[i].style.display = "list-item";
                });

            });
        }

        var input_search = document.querySelector("main input#choices-text-preset-values");
        input_search.addEventListener('input',function() {
            let allCards = document.querySelectorAll('.local_list_class .container_all_containers_list > .container .card');
            allCards.forEach(function(card) {
                card.lastElementChild.innerText.split(" | ")[0].toLowerCase().startsWith(input_search.value.toLowerCase()) ? card.style.display = "flex" : card.style.display = "none";
            });
            calc_cards_status();
            style_list();
            set_height_container();
            verify_list();
            set_pagination();
            position_bullets();
        });
        //////////////////// End Search Bar

        //////////////////// Begin Filter Bar
        var filter = [...document.querySelector(".local_list_class .filter").children];
        var allContainer = document.querySelectorAll('.local_list_class .container_all_containers_list > .container');
        filter.forEach(function(e,index) {
            allContainer[0].classList.add("active");
            e.onclick = function() {
                for(let i=0; i<filter.length; i++) {
                    filter[i].classList.remove("active");
                    allContainer[i].classList.remove("active");
                }
                e.classList.add("active");
                allContainer[index].classList.add("active");
                set_pagination();
                set_height_container();
            }
        });
        //////////////////// End Filter Bar

        /////////////////// Start section partner
        let nb_partner = [...document.querySelector(".nos_partners .content_partner").children]
        $(document).ready(function(){
            if(nb_partner.length >= 4) {
                $(".content_partner").owlCarousel({
                    loop:true,
                    margin:40,
//                    autoplay:true,
                    autoplayTimeout:4000,
                    autoplayHoverPause:true,
                    responsive:{
                        0:{
                            items:1
                        },
                        '576':{
                            items:nb_partner.length
                        }
                    }
                });
            } else {
                $(".content_partner").owlCarousel({
                    loop:false,
                    margin:40,
                    autoplay:false,
                    responsive:{
                        0:{
                            items:1
                        },
                        '576':{
                            items:nb_partner.length
                        }
                    }
                });
            }
        });
        /////////////////// End section partner

        ////////////////////  Each reload
        calc_cards_status();
        style_list();
        set_pagination();
        set_height_container();
        position_bullets();
        activate_bullets_list();
//        section_partner_slick();

        console.log("####### End Console");

        /////////////////// Document Script

            let nums = document.querySelectorAll("div.info .sec_child");
            let section_nums = document.querySelector("div.info");
            let started = false

            window.onscroll = function() {
                let try1 = section_nums.offsetTop - 800
                if(window.scrollY >= try1) {
                    if(!started)
                        nums.forEach((num) => startCount(num));
                    started = true
                }
            }

            function startCount(el) {
                let goal = el.dataset.goal;
                if(goal > 0) {
                    let count = setInterval(() => {
                    el.textContent++;
                    if(el.textContent == goal)
                            clearInterval(count);
                    }, 2000 / goal)
                }
            }
    } else
        console.log("before List")

});
