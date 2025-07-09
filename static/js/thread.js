document.addEventListener("DOMContentLoaded", function () {
    let threadId = document.getElementById("upvote-button").getAttribute("data-thread-id");
    let upvoteButton = document.getElementById("upvote-button");
    let downvoteButton = document.getElementById("downvote-button");
    let upvoteCount = document.getElementById("upvote-count");

    // upvotes
    if (upvoteButton) {
        upvoteButton.addEventListener("click", function () {
            voteThread(threadId, "upvote");
        });
    }

    // downvotes
    if (downvoteButton) {
        downvoteButton.addEventListener("click", function () {
            voteThread(threadId, "downvote");
        });
    }

    // Voting (Upvote & Downvote)
    function voteThread(threadId, voteType) {
        fetch(`/vote/${threadId}`, {
            method: "PUT",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ "vote": voteType })  // send vote type in request
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                upvoteCount.textContent = data.upvotes;  // update Upvote Count
            }
        })
        .catch(error => {
            console.error("Error voting thread:", error);
            alert("Error: Unable to vote.");
        });
    }

    // comment submission
    let commentForm = document.getElementById("comment-form");
    if (commentForm) {
        commentForm.addEventListener("submit", function (event) {
            event.preventDefault();  //prevent page reload

            let author = document.getElementById("comment-author").value.trim();
            let content = document.getElementById("comment-content").value.trim();

            if (!author || !content) {
                alert("Error: Please enter your name and comment.");
                return;
            }

            let body = JSON.stringify({ "author": author, "content": content });

            fetch(`/comment/${threadId}`, {
                method: "POST",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                body: body
            })
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    throw new Error(data.error || "Failed to post comment.");
                }

                console.log("Comment added:", data);

                // dynamically add new comment to comment list
                let commentList = document.querySelector(".list-group");
                let newComment = document.createElement("li");
                newComment.className = "list-group-item";
                newComment.innerHTML = `<strong>${data.comment.author}</strong>: ${data.comment.content} <small>📅 Just Now</small>`;
                
                commentList.prepend(newComment);  // add new comment to top

                // clear input 
                document.getElementById("comment-author").value = "";
                document.getElementById("comment-content").value = "";
            })
            .catch(error => {
                console.error("Error:", error);
                alert("Error: " + error.message);
            });
        });
    }
});
