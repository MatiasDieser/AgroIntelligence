# Plan de Negocio

## Servicios de Inteligencia Agronómica con Drones

### Argentina — La Pampa y Neuquén

*Documento de trabajo — etapa de validación temprana (pre-MVP comercial). Las cifras de mercado, precios y financieras son estimaciones a validar con clientes reales, no proyecciones cerradas.*

\---

## 1\. Resumen Ejecutivo

El proyecto propone un servicio de **inteligencia agronómica con drones** para productores agropecuarios de La Pampa y Neuquén. A diferencia de la mayoría de los operadores de drones en Argentina —enfocados en fumigación—, la propuesta de valor central es la **interpretación accionable de datos**: no se entregan mapas ni fotos aéreas, sino informes con diagnóstico, hallazgos y recomendaciones, validados por un ingeniero agrónomo matriculado.

El equipo fundador combina dos perfiles técnicos (desarrollo de software) y un perfil de dominio (ingeniería agronómica), una combinación poco común en el segmento y que constituye la principal ventaja competitiva del proyecto.

El proyecto se encuentra en etapa de **desarrollo de MVP técnico**, con el pipeline de procesamiento de datos (cálculo de índices vegetativos, generación de informes asistidos por IA) ya funcionando de punta a punta sobre datos de prueba. Aún no se ha adquirido el hardware de vuelo, no existen clientes pagos, y la validación comercial es la prioridad inmediata antes de continuar invirtiendo en desarrollo.

\---

## 2\. Descripción del Negocio y Propuesta de Valor

### 2.1 Qué se ofrece

Un servicio de relevamiento aéreo y análisis de campos que entrega:

* Detección de anomalías y zonas de estrés (hídrico, nutricional, sanitario)
* Conteo asistido de animales en ganadería extensiva
* Relevamiento post-evento (granizo, inundación, helada, incendio)
* Seguimiento temporal del estado de lotes y cultivos
* Informes en lenguaje claro, con mapas, hallazgos y recomendaciones, validados por un ingeniero agrónomo

### 2.2 Qué NO se ofrece (por decisión estratégica)

* **Fumigación con drones**: mercado ya ocupado por operadores establecidos (Tekron, Bidcom Agro, Summit Agro, AgriFly, Agropix), de mayor intensidad de capital y menor diferenciación.
* **Vuelo autónomo sin supervisión (BVLOS)**: el marco regulatorio argentino lo permite solo bajo autorización especial (RAAC Parte 102), inviable en el corto plazo.

### 2.3 Propuesta de valor

> \*"No vendemos fotos ni mapas. Vendemos inteligencia agronómica interpretada."\*

El diferencial no es la tecnología de captura (cualquier competidor puede comprar el mismo dron), sino la combinación de:

1. Procesamiento automatizado con IA para escalar el análisis
2. Validación y firma de un ingeniero agrónomo, que da respaldo profesional y credibilidad ante el productor
3. Conocimiento territorial directo de las dos zonas de operación

\---

## 3\. Análisis de Mercado

### 3.1 Tamaño y crecimiento

El parque de drones agrícolas en Argentina se estimaba en menos de 500 unidades en 2024, con proyecciones de alcanzar cerca de 3.000 unidades hacia 2026. El crecimiento está impulsado mayormente por la sustitución de pulverizadoras terrestres, no por servicios de análisis, lo que sugiere que el segmento de diagnóstico e interpretación está desatendido en relación al de aplicación.

### 3.2 Competencia

**En fumigación/aplicación** (no es el foco del proyecto, pero define el paisaje competitivo):
Tekron, Bidcom Agro, Summit Agro Argentina, AgriFly, Agropix, TodoDrones Agricultura. Mercado con jugadores establecidos, alta competencia de precio, baja diferenciación.

**En análisis y agricultura de precisión:**
Auravant es la referencia local más consolidada, con foco predominante en datos satelitales. No existe hoy un jugador dominante que combine drones + análisis interpretado + validación agronómica humana de forma productizada. Esta ausencia constituye la oportunidad central del proyecto, aunque no debe interpretarse automáticamente como demanda garantizada — requiere validación directa con productores.

### 3.3 Marco regulatorio

La Resolución ANAC 550/2025 estableció un marco simplificado (RAAC Parte 100/101/102):

|Categoría de dron|Requisito|
|-|-|
|Menos de 250 g|Sin licencia ni registro|
|250 g – 25 kg (Categoría Abierta)|Registro digital del equipo, sin licencia de piloto|
|Más de 25 kg / operación autónoma BVLOS (Categoría Específica)|Licencia de piloto y autorización basada en análisis de riesgo|

El equipo previsto (DJI Mini 4 Pro, luego Mavic 3M) opera en la categoría intermedia: solo requiere registro, sin trámites de piloto. La operación autónoma sin supervisión visual queda fuera de alcance en esta etapa por su mayor complejidad regulatoria.

### 3.4 Zonas de operación

||La Pampa|Neuquén|
|-|-|-|
|Perfil productivo|Agricultura extensiva (soja, maíz, trigo), ganadería bovina de escala|Fruticultura, vid, ganadería extensiva patagónica|
|Valor por hectárea del cultivo|Menor — el análisis debe orientarse a eventos puntuales (emergencias, daños) más que a monitoreo continuo por hectárea|Mayor — cultivos intensivos justifican mejor un servicio de monitoreo recurrente|
|Oferta inicial sugerida|Diagnóstico de anomalías por lote / informe de emergencia post-siembra|Monitoreo de vigor en vid y frutales|

La disparidad entre ambas zonas sugiere que **no conviene ofrecer un producto único**; probablemente se necesiten dos propuestas comerciales distintas adaptadas a cada perfil productivo.

\---

## 4\. Modelo de Negocio

### 4.1 Oferta inicial concreta (a validar)

En lugar de un servicio genérico de "monitoreo con drones", se recomienda arrancar con ofertas específicas y de fácil comprensión para el productor:

* **La Pampa**: "Diagnóstico de anomalías de lote" o "Informe de emergencia post-implantación" (fallas de siembra, anegamiento, daño puntual)
* **Neuquén**: "Monitoreo de vigor en viñedo/fruta" con seguimiento por sector

### 4.2 Estructura de precios (referencial, no validada)

|Servicio|Precio de mercado observado|
|-|-|
|Análisis básico|USD 5–20 por hectárea|
|Informe con validación e interpretación agronómica firmada|USD 30–50 por hectárea|
|Relevamiento puntual (ganadería, evento)|USD 300–800 por jornada de vuelo|

Estos valores provienen de referencias de mercado y **no deben usarse como proyección financiera hasta validarse con productores reales de cada zona**, especialmente en agricultura extensiva donde el margen por hectárea es más ajustado.

### 4.3 Posibles esquemas comerciales a futuro

* Por evento/vuelo puntual (el más simple para arrancar)
* Por campaña (paquete de vuelos con seguimiento a lo largo de la temporada)
* Suscripción mensual con vuelos incluidos (más adelante, cuando haya volumen)
* Licenciamiento de la plataforma a otros ingenieros agrónomos (a largo plazo)

### 4.4 Canal de entrega

Informe en PDF entregado por **link único vía WhatsApp**, sin portal web ni sistema de login. Decisión deliberada: el productor agropecuario no adopta fácilmente sistemas con fricción de acceso. Se prioriza la simplicidad de uso por sobre la sofisticación del producto.

\---

## 5\. Equipo

|Rol|Perfil|Responsabilidad|
|-|-|-|
|Socio 1 (Santa Rosa, La Pampa)|Desarrollador de software|Arquitectura del sistema, backend, infraestructura|
|Socio 2 (Aluminé, Neuquén)|Desarrollador de software|Pipeline de procesamiento de datos, piloto en zona patagónica|
|Socio 3|Ingeniero agrónomo matriculado|Validación de hallazgos, firma de informes, contacto comercial con productores|

Los tres socios operan **part-time** en esta etapa, lo cual condiciona el ritmo de avance y hace prioritario acotar el alcance de trabajo a lo estrictamente necesario para validar el negocio.

\---

## 6\. Plan Operativo y Tecnológico

### 6.1 Arquitectura del sistema

```
Dron (captura offline)
      ↓ (microSD / sync manual)
Worker de procesamiento (Python)
  → cálculo de índices vegetativos (NDVI y aproximaciones RGB)
  → generación de mapas de color
  → redacción de análisis asistida por IA (LLM)
      ↓
Generación de informe (PDF)
      ↓
Entrega al cliente (link único por WhatsApp)
      ↓
Feedback del agrónomo (confirma / corrige hallazgos)
      ↓
Refinamiento continuo del sistema
```

Backend en ASP.NET Core (.NET 8), procesamiento en Python, base de datos PostgreSQL con extensión PostGIS para datos geoespaciales, todo containerizado con Docker para facilitar la futura migración a infraestructura en la nube.

El dron opera de forma **desconectada** ("dron tonto"): no transmite datos en tiempo real a ningún sistema. Esto simplifica la arquitectura inicial y evita complejidad regulatoria asociada a operación conectada o autónoma.

Se incorpora un mecanismo de **feedback del agrónomo**: cada hallazgo del sistema puede ser confirmado, corregido o complementado por el agrónomo, generando un historial que permite refinar los umbrales de detección y mejorar la calidad de los informes con el tiempo.

### 6.2 Hoja de ruta tecnológica por fases

**Fase 0 — Validación (actual)**
Pipeline de procesamiento funcionando sobre datos satelitales gratuitos (Sentinel-2), sin inversión en hardware de vuelo. Objetivo: validar disposición de pago antes de invertir en equipo.

**Fase 1 — MVP con dron básico**
Adquisición de DJI Mini 4 Pro (RGB, sin sensor multiespectral). Validación operativa de vuelo, generación de ortomosaicos, primeros clientes piloto.

**Fase 2 — Servicio profesional**
Adquisición de DJI Mavic 3M (multiespectral real: NDVI y NDRE verdaderos) cuando exista base de clientes que justifique la inversión (\~USD 6.400).

**Fase 3 — Escalamiento**
Automatización de la ingesta de imágenes, incorporación de detección de objetos (conteo de animales) y evaluación de técnicas de generación de índices vegetativos aproximados a partir de cámaras RGB económicas (reduciendo la dependencia del sensor multiespectral costoso).

### 6.3 Decisiones técnicas deliberadamente pospuestas

Para mantener foco en la validación comercial, se descartan explícitamente en esta etapa: portal web con autenticación, aplicación móvil propia, operación autónoma de vuelo (BVLOS), estaciones de carga automática ("drone-in-a-box"), y arquitecturas de microservicios complejas. Estas decisiones se revisarán únicamente cuando exista tracción comercial que las justifique.

\---

## 7\. Plan Financiero Preliminar

*Advertencia: las siguientes cifras son estimaciones de referencia para dimensionar la inversión inicial. No constituyen una proyección de ingresos validada.*

### 7.1 Inversión inicial estimada

|Concepto|USD estimado|
|-|-|
|Dron DJI Mini 4 Pro (Fly More Combo)|850 – 1.000|
|Software de procesamiento (open source, costo marginal)|0|
|Infraestructura cloud / cómputo básico|50 – 100/mes|
|Registro ante ANAC y seguro de responsabilidad civil|500 – 1.500/año|
|**Subtotal etapa de validación**|**\~1.600 – 2.600**|
|DJI Mavic 3M (Fase 2, condicionado a tracción)|6.400|

### 7.2 Estructura de costos operativos recurrentes

* Cómputo/infraestructura cloud
* API de modelos de lenguaje para generación de informes (costo marginal muy bajo, centavos de dólar por informe)
* Mantenimiento de equipo de vuelo (baterías, repuestos)
* Seguro de responsabilidad civil

### 7.3 Consideración sobre precios y rentabilidad

Dado que los precios de referencia de mercado (USD 5–50/ha) no han sido validados localmente, **no se debe proyectar rentabilidad hasta contar con al menos 3 a 5 clientes reales pagando**, en ambas zonas de operación, que permitan calibrar precio, tiempo de entrega y costo real por informe.

\---

## 8\. Análisis de Riesgos

|Riesgo|Descripción|Mitigación propuesta|
|-|-|-|
|Disposición de pago incierta|El productor puede valorar el informe pero no estar dispuesto a pagar el precio de mercado de referencia|Validar con informes piloto (incluso con datos satelitales) antes de invertir en hardware avanzado|
|Sobrepromesa técnica|El DJI Mini 4 Pro no tiene sensor multiespectral real; prometer NDVI/NDRE preciso con este equipo dañaría la credibilidad|Comunicar con claridad las limitaciones de cada fase de hardware al cliente|
|Capacidad limitada del equipo|Los tres socios trabajan part-time|Acotar el alcance de cada etapa a lo mínimo necesario para validar, evitar sobre-ingeniería|
|Heterogeneidad geográfica|La Pampa y Neuquén tienen perfiles productivos muy distintos|Diseñar ofertas comerciales diferenciadas por zona en lugar de un producto único|
|Marco regulatorio de vuelo autónomo inmaduro|La operación BVLOS requiere autorización especial compleja|Mantener operación con piloto presente en el corto y mediano plazo; no depender de autonomía total en el plan de negocio actual|

\---

## 9\. Hoja de Ruta de Validación y Financiamiento

### Corto plazo (0–3 meses)

* Generar los primeros informes con datos satelitales gratuitos y mostrarlos al agrónomo socio y a productores conocidos de ambas zonas
* Validar disposición de pago y precio percibido antes de adquirir el dron
* Definir una oferta comercial concreta por zona

### Mediano plazo (3–12 meses)

* Adquisición del primer dron y primeros vuelos reales
* Primeros clientes pagos, aunque sea a precio reducido
* Recolección sistemática de feedback del agrónomo para refinar el sistema

### Financiamiento futuro (condicionado a tracción demostrada)

**Fondos públicos** (más accesibles en etapa temprana): líneas FONTAR/ANPCyT como ANR Emprendedores (subsidio no reembolsable), posible articulación con INTA/INTI, agencias de desarrollo productivo de Neuquén y La Pampa.

**Fondos privados** (solo con tracción real): aceleradoras especializadas en agtech, ángeles inversores. No se recomienda buscar este tipo de financiamiento antes de contar con clientes y datos de uso reales — ningún inversor privado invierte en una idea sin validación de mercado.

\---

## 10\. Conclusión

El proyecto combina una oportunidad de mercado real (segmento de análisis interpretado desatendido en Argentina) con un equipo cuya composición —desarrollo de software más dominio agronómico— constituye una ventaja competitiva genuina y poco común. El riesgo principal no es tecnológico sino comercial: la validación de que el productor agropecuario está dispuesto a pagar por este tipo de servicio debe preceder a cualquier inversión significativa en hardware o desarrollo adicional. La estrategia recomendada prioriza informes piloto de bajo costo antes de escalar la inversión.

