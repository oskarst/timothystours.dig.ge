document.addEventListener('DOMContentLoaded', () => {
    const carousels = document.querySelectorAll('.carousel-container');
    
    carousels.forEach(container => {
        const wrapper = container.parentElement;
        const prevBtn = wrapper.querySelector('.carousel-prev');
        const nextBtn = wrapper.querySelector('.carousel-next');
        
        if (!prevBtn || !nextBtn) return;
        
        // Scroll amount is roughly one image width + gap
        // Image width is w-80 (20rem = 320px), plus gap-4 (1rem = 16px)
        const scrollAmount = 336;
        
        prevBtn.addEventListener('click', () => {
            container.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
        });
        
        nextBtn.addEventListener('click', () => {
            container.scrollBy({ left: scrollAmount, behavior: 'smooth' });
        });
        
        // Drag to scroll functionality
        let isDown = false;
        let startX;
        let scrollLeft;

        container.addEventListener('mousedown', (e) => {
            isDown = true;
            startX = e.pageX - container.offsetLeft;
            scrollLeft = container.scrollLeft;
            // Temporarily remove smooth scroll and snapping during drag
            container.style.scrollBehavior = 'auto';
            container.style.scrollSnapType = 'none';
            // Prevent default image drag
            e.preventDefault();
        });

        container.addEventListener('mouseleave', () => {
            if(!isDown) return;
            isDown = false;
            container.style.scrollBehavior = 'smooth';
            container.style.scrollSnapType = 'x mandatory';
        });

        container.addEventListener('mouseup', () => {
            if(!isDown) return;
            isDown = false;
            container.style.scrollBehavior = 'smooth';
            container.style.scrollSnapType = 'x mandatory';
        });

        container.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - container.offsetLeft;
            const walk = (x - startX) * 2; // scroll speed multiplier
            container.scrollLeft = scrollLeft - walk;
        });
    });
});
