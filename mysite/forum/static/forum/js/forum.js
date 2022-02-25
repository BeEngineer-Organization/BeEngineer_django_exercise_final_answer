const infoAreas = document.querySelectorAll(".comment-info-box");

 infoAreas.forEach(function(element) {
     element.addEventListener("click", function(e) {
         var id = element.id;
         var commentAreaId = "comment-all-box-" + id;
         var commentArea = document.getElementById(commentAreaId);
         if (commentArea.style.display == "block") {
             commentArea.style.display = "none";
         } else {
             commentArea.style.display = "block";
         }
     });
 });