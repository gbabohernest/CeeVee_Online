const hamburger = document.querySelector('#hamburger');
const mobileNavLinks = document.querySelector('#mobile_links');

// ! TOGGLE HAMBURGER MENU

const toggleHamburgerMenu = () => {
  const buttons = hamburger.querySelectorAll('.icon-btn');

  if (mobileNavLinks.classList.contains('close')) {
    buttons.forEach((btn) => {
      //* OPEN MOBILE NAV LINKS
      if (!btn.classList.contains('close')) {
        btn.classList.add('close');

        console.log('add close');
      } else {
        btn.classList.remove('close');
        mobileNavLinks.classList.add('close');
        console.log('remove close');
      }
    });
    mobileNavLinks.classList.remove('close');
  } else {
    buttons.forEach((btn) => {
      //* CLOSE MOBILE NAV LINKS
      if (btn.classList.contains('close')) {
        btn.classList.remove('close');
      } else {
        btn.classList.add('close');
      }
    });
    mobileNavLinks.classList.add('close');
  }
};

hamburger.addEventListener('click', toggleHamburgerMenu);
