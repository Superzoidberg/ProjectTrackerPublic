var dryclass = document.getElementById('dryclass');
var reeferclass = document.getElementById('reeferclass');

if (window.location.href.includes('knig')) {
    dryclass.className += ' badge badge-danger';
}
if (window.location.href.includes('ktps')) {
    reeferclass.className += ' badge badge-info';
}