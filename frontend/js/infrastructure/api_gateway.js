/*
Path: frontend/js/infrastructure/api_gateway.js
*/

export class ApiGateway {
    constructor(baseUrl) { this.baseUrl = baseUrl; }

    async getConfig() {
        const response = await fetch(`${this.baseUrl}/config`);
        if (!response.ok) throw new Error("Error al obtener configuración");
        return response.json();
    }

    async saveConfig(configDTO) {
        const response = await fetch(`${this.baseUrl}/config`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(configDTO)
        });
        if (!response.ok) throw new Error("Error al guardar configuración");
        return response.json();
    }

    async convertSvgFromUrl(url, testMode) {
        const response = await fetch(`${this.baseUrl}/convert/url`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url, test_mode: testMode })
        });
        if (!response.ok) throw new Error("Error en conversión desde URL");
        return response.json();
    }

    async convertSvg(file, testMode) {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("test_mode", testMode);
        const response = await fetch(`${this.baseUrl}/convert`, { method: "POST", body: formData });
        if (!response.ok) throw new Error("Error en conversión");
        return response.json();
    }

    async convertImage(file, testMode) {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("test_mode", testMode);
        const response = await fetch(`${this.baseUrl}/convert/image`, { method: "POST", body: formData });
        if (!response.ok) throw new Error("Error en conversión de imagen");
        return response.json();
    }
}