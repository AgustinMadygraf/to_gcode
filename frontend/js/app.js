/*
Path: frontend/js/app.js
*/

import { ApiGateway } from "./infrastructure/api_gateway.js";
import { MachineConfig } from "./domain/machine_config.js";

const api = new ApiGateway("http://localhost:8000");

async function loadConfig() {
    try {
        const data = await api.getConfig();
        document.getElementById("name").value = data.name;
        document.getElementById("width").value = data.width;
        document.getElementById("height").value = data.height;
        document.getElementById("pen_up").value = data.pen_up_command;
        document.getElementById("pen_down").value = data.pen_down_command;
    } catch (e) {
        console.error("Error al cargar configuración:", e);
        if (e.message.includes("not found")) {
            console.warn("Configuración no encontrada en el servidor.");
        }
    }
}

document.getElementById("configForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
        const config = new MachineConfig({
            name: document.getElementById("name").value,
            width: document.getElementById("width").value,
            height: document.getElementById("height").value,
            pen_up_command: document.getElementById("pen_up").value,
            pen_down_command: document.getElementById("pen_down").value
        });
        
        await api.saveConfig(config.toDTO());
        alert("Configuración guardada exitosamente");
    } catch (e) {
        console.error("Error al guardar configuración:", e);
        alert("Error: " + e.message);
    }
});

document.getElementById("convertBtn").addEventListener("click", async () => {
    const file = document.getElementById("svgFile").files[0];
    if (!file) {
        console.warn("Intento de conversión sin archivo seleccionado.");
        return alert("Selecciona un SVG primero");
    }
    
    try {
        const data = await api.convertSvg(file);
        const blob = new Blob([data.gcode], { type: "text/plain" });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "output.gcode";
        a.click();
        window.URL.revokeObjectURL(url);
    } catch (e) {
        console.error("Error en conversión de archivo:", e);
        alert("Error al convertir SVG: " + e.message);
    }
});

document.getElementById("convertUrlBtn").addEventListener("click", async () => {
    const url = document.getElementById("svgUrl").value;
    if (!url) {
        console.warn("Intento de conversión sin URL.");
        return alert("Ingresa una URL");
    }
    
    try {
        const data = await api.convertSvgFromUrl(url);
        const blob = new Blob([data.gcode], { type: "text/plain" });
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = downloadUrl;
        a.download = "output_url.gcode";
        a.click();
        window.URL.revokeObjectURL(downloadUrl);
    } catch (e) {
        console.error("Error en conversión desde URL:", e);
        alert("Error al convertir desde URL: " + e.message);
    }
});

document.getElementById("convertImageBtn").addEventListener("click", async () => {
    const file = document.getElementById("imageFile").files[0];
    if (!file) {
        console.warn("Intento de conversión de imagen sin archivo seleccionado.");
        return alert("Selecciona una imagen primero");
    }
    
    try {
        const data = await api.convertImage(file);
        const blob = new Blob([data.gcode], { type: "text/plain" });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "output_image.gcode";
        a.click();
        window.URL.revokeObjectURL(url);
    } catch (e) {
        console.error("Error en conversión de imagen:", e);
        alert("Error al convertir imagen: " + e.message);
    }
});
