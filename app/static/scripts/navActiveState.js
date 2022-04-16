/**
 * Generate active state for navigation page links
 */
(function () {

  // Get all of our nav-links in an array
  const navLinks = document.getElementsByClassName("nav-link");
  let index, favorites, login, register;

  // Assign all possible routes to their respective variables
  for (let i = 0; i < navLinks.length; i++) {
    switch (navLinks[i].pathname) {

      case "/":
        index = navLinks[i];
        break;

      case "/index":
        index = navLinks[i];
        break;

      case "/login":
        login = navLinks[i];
        break;

      case "/register":
        register = navLinks[i];
        break;

      case '/favorites':
        favorites = navLinks[i];
        break;

      default:
        break;
    }
  }

  // Add the .active-nav class to the link which contains the same pathname as the current page
  switch (window.location.pathname) {

    case "/":
      index.classList.add("active-nav");
      break;

    case "/index":
      index.classList.add("active-nav");
      break;

    case "/login":
      login.classList.add("active-nav");
      break;

    case "/register":
      register.classList.add("active-nav");
      break;

    case '/favorites':
      favorites.classList.add("active-nav")
      break;

    default:
      break;
  }

})();
