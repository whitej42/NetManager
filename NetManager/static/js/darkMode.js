function darkMode() {
    // change background to light/dark
    const body = document.body;
    body.classList.toggle("bg-light");

    // change widgets to light/dark
    const widget = document.getElementsByClassName('widget');
    for (let i = 0; i < widget.length; i++) {
        widget[i].classList.toggle("widget-light");
    }

    // change tables to light/dark
    const table = document.getElementsByClassName('table-dark');
    for (let i = 0; i < table.length; i++) {
        table[i].classList.toggle("table-light");
    }

    // change navbar to light/dark
    const navbar = document.getElementById('navbar');
    navbar.classList.toggle("nav-light");

    const links = document.getElementsByClassName('link')
    for (let i = 0; i < links.length; i++) {
        links[i].classList.toggle("link-light");
    }

    // change footer to light/dark
    const footer = document.getElementById('footer');
    footer.classList.toggle("footer-light");

    // change logo to light/dark
    const logo = document.getElementById('logo')
    if (logo.getAttribute('src') === "{% static 'images/logo-dark.png' %}") {
        console.log(logo.getAttribute('src'))
        // light logo
        logo.src = "{% static 'images/logo.png' %}";
    } else {
        // dark logo
        logo.src = "{% static 'images/logo-dark.png' %}";
    }

    // change text boxes to light/dark - Interface Page Only
    const textbox = document.getElementsByClassName('textbox');
    for (let i = 0; i < textbox.length; i++) {
        textbox[i].classList.toggle("textbox-light");
    }

    const title = document.getElementsByClassName('title');
    for (let i = 0; i < title.length; i++) {
        title[i].classList.toggle("title-light");
    }

    const add_device = document.getElementsByClassName('add-dark');
    for (let i = 0; i < add_device.length; i++) {
        add_device[i].classList.toggle("add-light");
    }
}