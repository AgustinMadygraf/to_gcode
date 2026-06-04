/*
Path: frontend/js/domain/machine_config.js
*/

export class MachineConfig {
    constructor({ name, width, height, pen_up_command, pen_down_command }) {
        if (!name || width <= 0 || height <= 0) throw new Error("Configuración inválida");
        this.name = name;
        this.width = parseFloat(width);
        this.height = parseFloat(height);
        this.pen_up_command = pen_up_command;
        this.pen_down_command = pen_down_command;
    }

    toDTO() {
        return {
            name: this.name,
            width: this.width,
            height: this.height,
            pen_up_command: this.pen_up_command,
            pen_down_command: this.pen_down_command,
            feedrate_draw: 1000.0,
            feedrate_move: 2000.0
        };
    }
}
