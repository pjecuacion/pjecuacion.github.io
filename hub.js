// Custom cursor
const cursor = document.querySelector('.cursor');
if (cursor && !window.matchMedia('(pointer: coarse)').matches) {
    document.addEventListener('mousemove', e => {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
    });
    document.querySelectorAll('a, button, .app-card').forEach(el => {
        el.addEventListener('mouseenter', () => cursor.classList.add('active'));
        el.addEventListener('mouseleave', () => cursor.classList.remove('active'));
    });
}

// Scroll reveal
const revealOnScroll = () => {
    document.querySelectorAll('.reveal').forEach(el => {
        if (el.getBoundingClientRect().top < window.innerHeight - 80) el.classList.add('visible');
    });
};
window.addEventListener('scroll', revealOnScroll);
revealOnScroll();

// Parallax orbs on mouse move
if (!window.matchMedia('(pointer: coarse)').matches) {
    document.addEventListener('mousemove', e => {
        const x = e.clientX / window.innerWidth;
        const y = e.clientY / window.innerHeight;
        document.querySelectorAll('.floating-orb').forEach((orb, i) => {
            const s = (i + 1) * 16;
            orb.style.transform = `translate(${x * s}px, ${y * s}px)`;
        });
    });
}

// Nav darkens on scroll
const nav = document.getElementById('main-nav');
if (nav) {
    window.addEventListener('scroll', () => {
        nav.style.background = window.scrollY > 60 ? 'rgba(3,3,6,0.96)' : 'rgba(5,5,10,0.75)';
    });
}