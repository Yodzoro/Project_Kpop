/*
Notes générales pour pas oublier

Variables :
- currentMonth et currentYear : mois et année affichés
- selectedArtistSlug : artiste filtré (« all » = tous par défaut)
- currentPage : pour la pagination (3 événements par page, nous tournons les pages)
- eventsData : événements de Django

Fonctions principales :
- renderCalendar() : crée le calendrier du mois
- filterEvents() : filtre par date + artiste
- updatePagination() : montre 3 events par page
- changeMonth()/changeYear() : changent le mois/année
- filterArtist() : filtre par artiste

Fonctionnement du code :
1. Quand page charge renderCalendar() et filterEvents() sont déjà affichés.
2. Si l'utilisateur clique sur filterEvents(), ça cache/montre les events par les artistes.
3. L'utilisateur peut choisir aussi bien le mois/année en utilisant changeMonth()/changeYear().
4. Si il y a plus de 3 events pour le mois/année choisie, il y a pagination active.
*/

// Variables globales
let currentMonth = new Date().getMonth() + 1; // +1 car le compteur dans js commence à 0, donc avant janvier = 0, maintenant janvier = 0 + 1 = 1
let currentYear = new Date().getFullYear();
let selectedArtistSlug = 'all';
let currentPage = 0;

if (typeof eventsData === 'undefined') {
    var eventsData = [];
}

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    renderCalendar(currentMonth, currentYear);
    filterEvents();
    initializePagination();
});

// Dropdown artiste
function toggleArtistDropdown() {
    const dropdown = document.getElementById('artistDropdown');
    dropdown.classList.toggle('active');
}

// Filtrer par artiste
function filterArtist(event, artistSlug, artistName) {
    if (event) event.preventDefault();
    selectedArtistSlug = artistSlug;
    currentPage = 0;
    document.getElementById('selected_artist').textContent = artistName;
    document.getElementById('artistDropdown').classList.remove('active');
    filterEvents();
    renderCalendar(currentMonth, currentYear);
}

// Dropdown mois
function toggleMonthDropdown(event) {
    if (event) event.preventDefault();
    const dropdown = document.getElementById('monthDropdown');
    dropdown.classList.toggle('active');
    document.getElementById('yearDropdown').classList.remove('active');
}

// Dropdown année
function toggleYearDropdown(event) {
    if (event) event.preventDefault();
    const dropdown = document.getElementById('yearDropdown');
    dropdown.classList.toggle('active');
    document.getElementById('monthDropdown').classList.remove('active');
}

// Changer le mois
function changeMonth(event, month, monthName) {
    event.preventDefault();
    currentMonth = month;
    currentPage = 0;
    document.getElementById('current_month').textContent = monthName;
    document.getElementById('monthDropdown').classList.remove('active');
    renderCalendar(currentMonth, currentYear);
    filterEvents();
}

// Changer l'année
function changeYear(event, year) {
    event.preventDefault();
    currentYear = year;
    currentPage = 0;
    document.getElementById('current_year').textContent = year;
    document.getElementById('yearDropdown').classList.remove('active');
    renderCalendar(currentMonth, currentYear);
    filterEvents();
}

// Filtrer les événements
function filterEvents() {
    const eventItems = document.querySelectorAll('.event_item');
    let visibleCount = 0;

    eventItems.forEach(item => {
        const eventDate = item.dataset.date;
        const eventArtistSlug = item.dataset.artistSlug;

        let showByDate = false;
        let showByArtist = false;

        // Verifier la date
        if (eventDate) {
            const [eventYear, eventMonth] = eventDate.split('-');
            showByDate = (parseInt(eventYear) === currentYear && parseInt(eventMonth) === currentMonth);
        }

         // Verifier l'artiste
        showByArtist = (selectedArtistSlug === 'all' || eventArtistSlug === selectedArtistSlug);

        // Montre si date et artiste ok
        if (showByDate && showByArtist) {
            item.classList.remove('hidden-event');
            visibleCount++;
        } else {
            item.classList.add('hidden-event');
        }
    });

    // Message si pas d'events
    const noEventsMsg = document.querySelector('.no_events');
    if (noEventsMsg) {
        noEventsMsg.style.display = visibleCount === 0 ? 'block' : 'none';
    }

    updatePagination();
}

// Initialiser la pagination
function initializePagination() {
    const eventsList = document.querySelector('.events_list');
    if (!eventsList) return;

    // Bouton précédent (haut)
    let showPrevBtn = document.getElementById('show_prev_events_btn');
    if (!showPrevBtn) {
        showPrevBtn = document.createElement('button');
        showPrevBtn.id = 'show_prev_events_btn';
        showPrevBtn.className = 'event_toggle_btn event_toggle_btn_top';
        showPrevBtn.style.display = 'none';
        showPrevBtn.onclick = showPreviousEvents;

        const img = document.createElement('img');
        img.src = '/static/main/img/event_bttn_up.png';
        img.alt = 'Show previous';
        showPrevBtn.appendChild(img);

        const firstEvent = eventsList.querySelector('.event_item');
        if (firstEvent) {
            eventsList.insertBefore(showPrevBtn, firstEvent);
        } else {
            eventsList.appendChild(showPrevBtn);
        }
    }

    // Bouton suivant (bas)
    let showNextBtn = document.getElementById('show_next_events_btn');
    if (!showNextBtn) {
        showNextBtn = document.createElement('button');
        showNextBtn.id = 'show_next_events_btn';
        showNextBtn.className = 'event_toggle_btn event_toggle_btn_bottom';
        showNextBtn.onclick = showNextEvents;

        const img = document.createElement('img');
        img.src = '/static/main/img/event_bttn.png';
        img.alt = 'Show next';
        showNextBtn.appendChild(img);

        eventsList.appendChild(showNextBtn);
    }

    updatePagination();
}

// Événements précédents
function showPreviousEvents() {
    if (currentPage > 0) {
        currentPage--;
        updatePagination();
    }
}

// Événements suivants
function showNextEvents() {
    const visibleEvents = getVisibleEvents();
    const maxPage = Math.floor((visibleEvents.length - 1) / 3);

    if (currentPage < maxPage) {
        currentPage++;
        updatePagination();
    }
}

// Obtenir les événements visibles
function getVisibleEvents() {
    const allEvents = document.querySelectorAll('.event_item');
    const visible = [];

    allEvents.forEach(item => {
        if (!item.classList.contains('hidden-event')) {
            visible.push(item);
        }
    });

    return visible;
}

/*
* Met à jour pagination
* Montre 3 events par page
* startIndex = currentPage * 3
* Cache les autres events
* */
function updatePagination() {
    const visibleEvents = getVisibleEvents();
    const totalEvents = visibleEvents.length;
    const showPrevBtn = document.getElementById('show_prev_events_btn');
    const showNextBtn = document.getElementById('show_next_events_btn');

    if (!showPrevBtn || !showNextBtn) return;

    // Si 3 ou moins, tout montrer
    if (totalEvents <= 3) {
        visibleEvents.forEach(item => {
            item.style.display = 'flex';
        });
        showPrevBtn.style.display = 'none';
        showNextBtn.style.display = 'none';
        currentPage = 0;
        return;
    }

    // Calcul index
    const startIndex = currentPage * 3;
    const endIndex = Math.min(startIndex + 3, totalEvents);

    // Afficher events[startIndex:endIndex]
    visibleEvents.forEach((item, index) => {
        if (index >= startIndex && index < endIndex) {
            item.style.display = 'flex';
        } else {
            item.style.display = 'none';
        }
    });

    // Boutons
    showPrevBtn.style.display = currentPage > 0 ? 'flex' : 'none';

    const isLastPage = endIndex >= totalEvents;
    showNextBtn.style.display = !isLastPage ? 'flex' : 'none';
}

/*
* Crée le calendrier
* firstDay = premier jour du mois
* firstDayOfWeek = jour semaine (0=lundi)
* Ajoute cases vides avant jour 1
* Puis ajoute tous les jours
* Si event ce jour donc classe has_event
* */
function renderCalendar(month, year) {
    const calendarDays = document.getElementById('calendarDays');
    if (!calendarDays) return;

    calendarDays.innerHTML = '';

    const firstDay = new Date(year, month - 1, 1);
    const lastDay = new Date(year, month, 0);

    // 0=dimanche, convertir en 0=lundi (1-1 = 0) et dimanche = 6
    let firstDayOfWeek = firstDay.getDay();
    firstDayOfWeek = firstDayOfWeek === 0 ? 6 : firstDayOfWeek - 1;

    //jours dans un mois
    const daysInMonth = lastDay.getDate();

    // Cases vides
    for (let i = 0; i < firstDayOfWeek; i++) {
        const emptyDay = document.createElement('div');
        emptyDay.className = 'calendar_day empty';
        calendarDays.appendChild(emptyDay);
    }

    // Jours du mois
    for (let day = 1; day <= daysInMonth; day++) {
        const dayElement = document.createElement('div');
        dayElement.className = 'calendar_day';
        dayElement.textContent = day;

        // Date format YYYY-MM-DD en String
        //.padStart(2, '0') : 12 - 2 chiffres -> on change rien, 8 - 1 chiffre -> on ajout 0 au début
        const dateStr = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;

        // Verifier si events ce jour
        const dayEvents = eventsData.filter(e => {
            const matchDate = e.date === dateStr;
            const matchArtist = (selectedArtistSlug === 'all' || e.artist_slug === selectedArtistSlug);
            return matchDate && matchArtist;
        });

        // Ajoute classe couleur (has_event)
        if (dayEvents.length > 0) {
            dayElement.classList.add('has_event');
            dayElement.classList.add(dayEvents[0].type);
        }

        calendarDays.appendChild(dayElement);
    }
}

// Fermer les dropdowns
document.addEventListener('click', function(e) {
    if (!e.target.closest('.filter_artist_dropdown')) {
        document.getElementById('artistDropdown')?.classList.remove('active');
    }
    if (!e.target.closest('.calendar_controls')) {
        document.getElementById('monthDropdown')?.classList.remove('active');
        document.getElementById('yearDropdown')?.classList.remove('active');
    }
});