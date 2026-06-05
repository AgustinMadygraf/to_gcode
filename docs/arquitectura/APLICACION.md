# Capa de Aplicación - to_gcode

Esta capa contiene la lógica de orquestación y los casos de uso del sistema. Su responsabilidad es dirigir el flujo de datos desde y hacia el dominio, utilizando las interfaces definidas en los boundaries.

## Patrones de Diseño Utilizados

### 1. Template Method (BaseGCodeConverter)
Para evitar la duplicidad de lógica en el proceso de conversión, se utiliza una clase base abstracta `BaseGCodeConverter`. Esta define el algoritmo estándar:
1. **Obtención de Configuración:** Valida que la máquina esté configurada.
2. **Parseo (Paso Abstracto):** Cada subclase implementa su propio parser (SVG, Imagen).
3. **Preparación:** Escala y orienta las trayectorias mediante `PathPreparationService`.
4. **Optimización:** Aplica algoritmos de reducción de movimientos en vacío.
5. **Generación:** Transforma el dominio final en sintaxis G-Code.

### 2. Dependency Injection (DI)
Todos los servicios y casos de uso reciben sus dependencias por constructor. Esto permite:
- Cambiar algoritmos de optimización en tiempo de ejecución.
- Realizar pruebas unitarias utilizando Mocks para los Gateways.

## Servicios de Aplicación

### PathPreparationService
Servicio encargado de "preparar" las trayectorias crudas para la máquina real. Sus funciones incluyen:
- Inserción de patrones de prueba (marcas de registro).
- Cálculo de orientación (Landscape vs Portrait) para maximizar el área de uso.
- Escalado proporcional basado en los límites físicos definidos en el dominio.

## Boundaries (Interfaces de Aplicación)
Se encuentran en `src/application/boundaries/` y definen los contratos que la capa de infraestructura debe cumplir:
- **VectorParser / RasterParser:** Para la entrada de datos.
- **GCodeGenerator:** Para la salida de datos.
- **MachineConfigRepository:** Para la persistencia de la configuración.

## Flujo de Datos
`Entrada Técnica (Web/CLI)` -> `Controller` -> `Caso de Uso (Aplicación)` -> `Entidades (Dominio)` -> `Salida (G-Code)`
