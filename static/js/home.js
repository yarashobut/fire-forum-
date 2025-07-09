// we wait for the DOM (HTML) to be fully loaded before running the script
document.addEventListener("DOMContentLoaded", function () {

    // the form element where users create a new thread
    let form = document.querySelector("form");

    // event listener that triggers when form is submitted
    form.addEventListener("submit", function (event) {
        event.preventDefault(); //stops default form submission ( would refresh the page)

        // user input values from form fields
        let title = document.getElementById("title").value.trim();
        let content = document.getElementById("content").value.trim();
        let author = document.getElementById("author").value.trim();

        // if any field is empty, show an alert and stop execution
        if (!title || !content || !author) {
            alert("All fields are required!");
            return; 
        }

        //lets make a JSON object with thread details
        let body = JSON.stringify({ "title": title, "content": content, "author": author });

        // send POST request to the server to create a new thread
        fetch('/new_thread', {
            method: 'POST',  // sends data to server
            headers: {
                'Accept': 'application/json',  // telling server that we expect JSON in return
                'Content-Type': 'application/json'  // we're sending JSON
            },
            body: body 
        })
        .then(response => response.json())  // convert server response into JSON
        .then(data => {
            if (!data.success) {  // did request fail
                throw new Error(data.error || "Failed to create thread.");
            }

            console.log("Success:", data); // log success response in console

            // get newly created thread data
            let thread = data["thread"];
            let listgrp = document.getElementsByClassName("list-group")[0]; // pick thread container

            // make new thread element to display it dynamically on page
            let threadContainer = document.createElement("div");
            threadContainer.className = "thread-item"; // CSS for styling

            // create link to the new thread page
            let a = document.createElement("a");
            a.href = `/thread/${thread["id"]}`; // clicking this will take user to full thread page
            a.className = "list-group-item";

            // make title element for thread
            let h = document.createElement("h3");
            h.appendChild(document.createTextNode(thread["title"])); // set thread title

            // make paragraph w/ comment count and upvotes
            let p = document.createElement("p");
            p.innerHTML = `🗨️ <strong>0 Comments</strong> | 👍 <strong><span id="upvotes-${thread["id"]}">0</span> Upvotes</strong>`;

            // make a date element for when the thread was created
            let date = document.createElement("small");
            date.innerHTML = `📅 Created: ${new Date().toISOString().split("T")[0]}`; // get current date

            // now make the Upvote Button
            let upvoteButton = document.createElement("button");
            upvoteButton.className = "upvote-button"; // styling class
            upvoteButton.setAttribute("data-thread-id", thread["id"]); // store thread ID
            upvoteButton.innerHTML = "👍 Upvote";
            upvoteButton.addEventListener("click", function () { // event listener for upvote 
                upvoteThread(thread["id"]); //call upvote function when clicked
            });

            // append all elements to their containers
            a.appendChild(h); // add title inside link
            a.appendChild(p); //add comment/upvote count
            a.appendChild(date); //add date
            threadContainer.appendChild(a); //add link inside thread container
            threadContainer.appendChild(upvoteButton); // add upvote button

            listgrp.prepend(threadContainer); // add new thread at the top of the list

            // clear input fields after successful submission
            document.getElementById("title").value = "";
            document.getElementById("content").value = "";
            document.getElementById("author").value = "";
        })
        .catch(error => {
            console.error("Error:", error); // log errors to console
            alert("Error: " + error.message); // show an alert if something goes wrong
        });
    });

    // select all upvote buttons that already exist on the page
    let upvoteButtons = document.querySelectorAll(".upvote-button");

    //event listeners to upvote buttons to handle upvotes
    upvoteButtons.forEach(button => {
        button.addEventListener("click", function () {
            let threadId = this.getAttribute("data-thread-id"); // get thread ID from the button
            upvoteThread(threadId); 
        });
    });

    // handle upvoting a thread (`thread.js`)
    function upvoteThread(threadId) {
        fetch(`/upvote/${threadId}`, {  // send a PUT request to the upvote route!!!
            method: "PUT",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json()) // convert response to JSON
        .then(data => {
            if (data.success) {  // if upvote was successful
                let upvoteCountElement = document.getElementById(`upvotes-${threadId}`);
                upvoteCountElement.textContent = data.upvotes;  // update upvote count
            }
        })
        .catch(error => {
            console.error("Error upvoting thread:", error); //error if something goes wrong
        });
    }
});
