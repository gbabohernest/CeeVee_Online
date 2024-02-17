const toggleSidebarBtn = document.querySelector('#toggle-sidebar-btn');
const sidebar = document.querySelector('.sidebar');

// categories navigation selections -> not functional yet
/* catMainControlBtn = document.querySelector('#categories-dropdown-main-control');
iconBTNS = document.querySelectorAll('.i-btn');
subCatTitleBtn = document.querySelectorAll('.sub-categories-UL');

const categoriesNavigationControl = () => {
  catMainUL = catMainControlBtn.querySelector('#categories-UL');
  console.log(iconBTNS);
};

categoriesNavigationControl();

catMainControlBtn.addEventListener('click', () => {
  catMainUL.classList.toggle('close');
}); */

//control the side with the hamburger btn in the navbar
toggleSidebarBtn.addEventListener('click', () => {
  if (!sidebar.classList.contains('close-sidebar')) {
    sidebar.classList.add('close-sidebar');
    sidebar.classList.remove('collapse-small-device');
  } else {
    sidebar.classList.remove('close-sidebar');
    sidebar.classList.remove('collapse-small-device');
  }
});
