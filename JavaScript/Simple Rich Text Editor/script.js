const tooltip = document.getElementById('tooltip');

    document.addEventListener('click', (event) => {
        const clickedElement = event.target;
        const position = clickedElement.getBoundingClientRect();

        // Get the tag name of the clicked element
        const elementTag = clickedElement.tagName;

        // Get the element's current position
        const top = position.top + window.scrollY; // Account for page scroll
        const left = position.left + window.scrollX;

        // Display the tooltip near the clicked element
        tooltip.innerHTML = `Tag: ${elementTag}<br>Position: Top - ${Math.round(top)}px, Left - ${Math.round(left)}px`;
        tooltip.style.display = 'block';
        tooltip.style.top = `${top + 20}px`; // Offset to position below the element
        tooltip.style.left = `${left + 20}px`; // Offset to position to the right of the element
    });

    document.addEventListener('scroll', () => {
        tooltip.style.display = 'none'; // Hide the tooltip when the user scrolls
    });