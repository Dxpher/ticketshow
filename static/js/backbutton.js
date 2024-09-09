
  // Detect back button click
  window.addEventListener('popstate', function (event) {
    // Display confirmation dialog
    var logout = confirm('Do you want to log out?');
    
    if (logout) {
      // Perform logout request
      window.location.href = '/logout';  // Redirect to the logout route
      
      // Alternatively, you can use an AJAX request to trigger the logout without a page reload
      // Example using jQuery: $.get('/logout');
    } else {
      // Prevent going back further in the history
      history.pushState(null, document.title, location.href);
    }
  });

