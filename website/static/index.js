// Function to handle liking/unliking a post
function like(postId) {
    const likeCount = document.getElementById(`likes-count-${postId}`);
    const likeButton = document.getElementById(`like-button-${postId}`);
 // Send a POST request to the server to like/unlike the post
    fetch(`/like-post/${postId}`, { method: "POST" })
      .then((res) => res.json())
      .then((data) => {
        likeCount.innerHTML = data["likes"];

        // Update the like button's class based on whether the user liked or unliked the post
        if (data["liked"] === true) {
          likeButton.className = "fas fa-thumbs-up";
        } else {
          likeButton.className = "far fa-thumbs-up";
        }
      })
      .catch((e) => alert("Could not like post."));
  }