var timeout;
        
async function getStatus() {

  let get;
  
  try {
    const res = await fetch("/status");
    get = await res.json();
  } catch (e) {
    console.error("Error: ", e);
  }
  
  document.getElementById("book-status").innerHTML = `loading books: ${get.book_status / 1.5 + "&percnt;"}`;
  document.getElementById("mood-status").innerHTML = `loading moods: ${get.mood_status / 1.5 + "&percnt;"}`;
  
  if (get.book_status == 150){
    document.getElementById("book-status").innerHTML = "Books loaded";
    clearTimeout(timeout);
    return false;
  }

  if (get.mood_status == 150){
    document.getElementById("book-status").innerHTML = "Books loaded";
    clearTimeout(timeout);
    return false;
  }
   
  timeout = setTimeout(getStatus, 2000);
}

    getStatus();