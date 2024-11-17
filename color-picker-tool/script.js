colorInput = document.getElementById('colorInput');
hexValue = document.getElementById('hexValue');
rgbValue = document.getElementById('rgbValue');

colorInput.addEventListener('input', () => {
    const color = colorInput.value;
    hexValue.textContent = color;
    rgbValue.textContent = hexToRgb(color);
})

const hexToRgb = (hex) => {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);

    return `rgb(${r}, ${g}, ${b})`
}
