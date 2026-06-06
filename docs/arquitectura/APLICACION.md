# Capa de Aplicación - to_gcode

Esta capa contiene la lógica de orquestación y los casos de uso del sistema. Su responsabilidad es dirigir el flujo de datos desde y hacia el dominio, utilizando las interfaces definidas en los puertos.

## Patrones de Diseño Utilizados

### 1. Template Method (ConvertidorBaseGCode)
Para evitar la duplicidad de lógica en el proceso de conversión, se utiliza una clase base abstracta `ConvertidorBaseGCode`. Esta define el algoritmo estándar:
1. **Obtención de Configuración:** Valida que la máquina esté configurada.
2. **Parseo (Paso Abstracto):** Cada subclase implementa su propio parser (SVG, Imagen).
3. **Preparación:** Escala y orienta las trayectorias mediante `ServicioPreparacionTrayectoria`.
4. **Optimización:** Aplica algoritmos de reducción de movimientos en vacío.
5. **Generación:** Transforma el dominio final en sintaxis G-Code.

### 2. Inyección de Dependencias (DI)
Todos los servicios y casos de uso reciben sus dependencias por constructor.

## Servicios de Aplicación

### ServicioPreparacionTrayectoria
Servicio encargado de "preparar" las trayectorias crudas para la máquina real. Sus funciones incluyen:
- Inserción de patrones de prueba (marcas de registro).
- Cálculo de orientación para maximizar el área de uso.
- Escalado proporcional basado en los límites físicos definidos en el dominio.

## Puertos (Interfaces de Aplicación)
Se encuentran en `src/aplicacion/limites/` y definen los contratos que la capa de infraestructura debe cumplir:
- `AnalizadorVectorial / AnalizadorRaster`: Para la entrada de datos.
- `GeneradorGCode`: Para la salida de datos.
- `RepositorioConfiguracionMaquina`: Para la persistencia de la configuración.
