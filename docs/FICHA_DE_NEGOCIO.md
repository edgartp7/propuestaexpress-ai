# FICHA DE NEGOCIO — PropuestaExpress AI
**Software:** PropuestaExpress AI  
**Categoría:** B2B SaaS / Productividad Comercial con IA Generativa  
**Programa:** Certificado en Prompt Engineering — Advanced Prompt Engineering 4 Generative AI · UAI  

---

## 1. Cliente Objetivo y Problema

### El Cliente
Consultores independientes, pequeñas agencias de marketing y desarrollo de software, y freelancers B2B que ofrecen servicios profesionales por proyecto o retención mensual.

### El Problema
Tras sostener reuniones de levantamiento con clientes potenciales, estos profesionales pierden entre **4 y 6 horas redactando propuestas comerciales formales** a partir de notas dispersas y notas de voz. La demora de 3 a 5 días en entregar la cotización enfría la venta y reduce drásticamente las tasas de conversión, además de consumir horas valiosas de trabajo técnico no facturable.

---

## 2. Propuesta de Valor y el Rol Central de la IA

### Propuesta de Valor
**PropuestaExpress AI** transforma notas crudas, fragmentadas y desordenadas de reuniones en **propuestas comerciales ejecutivas completas en menos de 10 segundos**. Entrega un diagnóstico empático, alcance delimitado con exclusiones claras, cronograma de hitos y una tabla presupuestaria matemáticamente coherente lista para ser presentada al cliente.

### Por qué la IA es Indispensable
No es un simple generador de plantillas fijas. La IA generativa (Gemini 1.5 Flash):
1. **Razona semánticamente** sobre requerimientos ambiguos para identificar el dolor de negocio real.
2. **Previene el "scope creep"** delimitando qué tareas quedan explícitamente fuera del presupuesto.
3. **Adapta el tono persuasivo** (ejecutivo, comercial o colaborativo) al perfil del tomador de decisiones.

---

## 3. Modelo de Negocio e Ingresos (SaaS Freemium)

* **Plan Starter (Gratuito):** Hasta 3 propuestas comerciales al mes. Diseñado como canal de adquisición y prueba de valor de bajo costo.
* **Plan Pro ($15 USD / mes):** Propuestas ilimitadas, exportación en Markdown y PDF formal, personalización de moneda y eliminación de marca de agua.
* **Plan Agency ($39 USD / mes):** Hasta 5 usuarios por equipo, repositorio centralizado de cotizaciones y soporte prioritario.

---

## 4. Costo Mensual Estimado de Operación y Rentabilidad

### Escenario Base: 1.000 Usuarios Activos (~10.000 propuestas generadas al mes)
* **Consumo de API de IA (Google Gemini 1.5 Flash):**  
  $10.000 \text{ solicitudes} \times (1.000 \text{ tokens entrada} + 1.500 \text{ tokens salida}) = 25 \text{M tokens/mes}$.  
  Tarifa: $0,075 / 1M entrada + $0,30 / 1M salida $\rightarrow$ **$1,13 USD / mes**. *(En Free Tier: $0,00 USD)*.
* **Hosting en la Nube (Contenedor Cloud Run / Render con auto-scaling):** **$7,00 USD / mes**.
* **Base de datos y almacenamiento ligero:** **$0,00 USD / mes** (arquitectura serverless).
* **COSTO TOTAL OPERATIVO MENSUAL:** **$8,13 USD / mes**.

### Rentabilidad y Margen
* Con apenas **1 cliente suscrito al Plan Pro ($15 USD/mes)**, la plataforma cubre el 100% de sus costos fijos y variables.
* Con 100 clientes de pago ($1.500 USD de facturación mensual), el **margen operativo bruto supera el 99,4%**.
