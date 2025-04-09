# Documentación Sistema de Misiones RPG

## Índice

1. [Estructura de la aplicación](./estructura.md)
2. [Patrones de diseño implementados](./patrones-diseno.md)
3. [Sistema de cola FIFO](./cola-fifo.md)
4. [API REST con FastAPI](./api-endpoints.md)
5. [Guía de instalación y uso](./instalacion.md)
6. [Diagramas](#diagramas)
   - [Diagrama de Clases](./diagramas-clase.md)
   - [Diagrama de Componentes](./diagramas-componentes.md)
   - [Diagramas de Patrones de Diseño](./diagramas-patrones.md)

## Descripción general

Este proyecto implementa un sistema de gestión de misiones para un juego de rol (RPG) utilizando Python, SQLAlchemy para la persistencia de datos y FastAPI para la exposición de endpoints REST. La aplicación permite la creación de personajes y misiones, así como la asignación y realización de misiones siguiendo un sistema de cola FIFO.

El sistema está diseñado siguiendo principios SOLID, arquitectura por capas y varios patrones de diseño para garantizar su mantenibilidad y escalabilidad.

## Principales características

- Creación y gestión de personajes y misiones
- Sistema de asignación de misiones mediante cola FIFO
- Sistema de progreso de personajes mediante experiencia
- API REST documentada con Swagger
- Patrón repositorio para acceso a datos
- Arquitectura por capas (modelos, repositorios, servicios, controladores)

## Diagramas

Para entender mejor la arquitectura del sistema, se han creado varios diagramas:

### Diagrama de Clases
El [diagrama de clases](./diagramas-clase.md) muestra las principales clases del sistema y sus relaciones, incluyendo modelos, repositorios, servicios y DTOs.

### Diagrama de Componentes
El [diagrama de componentes](./diagramas-componentes.md) muestra los principales componentes del sistema y cómo interactúan entre sí, ilustrando la arquitectura por capas implementada.

### Diagramas de Patrones de Diseño
Los [diagramas de patrones](./diagramas-patrones.md) ilustran los principales patrones de diseño utilizados en el proyecto:
- Patrón Repositorio
- Patrón Singleton
- Patrón DTO (Data Transfer Object)
- Patrón Inyección de Dependencias
- Patrón FIFO (First In, First Out)
- Arquitectura por Capas
