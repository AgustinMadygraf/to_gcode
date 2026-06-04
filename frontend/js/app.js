const API_URL = 'http://localhost:8000';

async function loadConfig() {
    try {
        const response = await fetch(`${API_URL}/config`);
        if (response.ok) {
            const data = await response.json();
            document.getElementById('name').value = data.name;
            document.getElementById('width').value = data.width;
            document.getElementById('height').value = data.height;
            document.getElementById('pen_up').value = data.pen_up_command;
            document.getElementById('pen_down').value = data.pen_down_command;
        }
    } catch (error) { console.error('Error cargando config:', error); }
}

document.getElementById('configForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const config = {
        name: document.getElementById('name').value,
        width: parseFloat(document.getElementById('width').value),
        height: parseFloat(document.getElementById('height').value),
        pen_up_command: document.getElementById('pen_up').value,
        pen_down_command: document.getElementById('pen_down').value,
        feedrate_draw: 1000.0,
        feedrate_move: 2000.0
    };
    
    await fetch(`${API_URL}/config`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config)
    });
    alert('Configuración guardada');
});

document.getElementById('convertBtn').addEventListener('click', async () => {
    const file = document.getElementById('svgFile').files[0];
    if (!file) return alert('Selecciona un SVG');
    
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`${API_URL}/convert`, { method: 'POST', body: formData });
    if (!response.ok) return alert('Error en conversión');
    
    const data = await response.json();
    const blob = new Blob([data.gcode], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'output.gcode';
    a.click();
});

loadConfig();