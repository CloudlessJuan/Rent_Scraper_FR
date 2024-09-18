# Web Scraping Application

This application, built with Azure Functions, performs web scraping to extract data from websites, uses time-based triggers to automate data collection, exposes an API to access the obtained data through HTTP requests, and filters the necessary fields to provide useful and relevant information. It integrates with Azure storage and ETL services for efficient data management and processing.

## Description

The application is designed to collect data from web pages using web scraping techniques, triggered at specified intervals by Azure Functions. Once the data is obtained, it is uploaded to a datalake for further processing using Azure’s storage and ETL services.

## Features

- **Web Scraping**: Collects data from specific websites.
- **Time-Based Triggers**: Automates the scraping process using Azure Functions with scheduled triggers.
- **Field Filtering**: Selects and processes the relevant fields from the obtained data.
- **Integration with Azure Services**: Seamlessly integrates with Azure Blob Storage, Data Lakes, and ETL pipelines for efficient storage and processing.

---

# Aplicación de Web Scraping

Esta aplicación, construida con Azure Functions, realiza web scraping para extraer datos de sitios web, utiliza triggers temporales para automatizar la recolección de datos, expone una API para acceder a los datos obtenidos a través de solicitudes HTTP, y filtra los campos necesarios para proporcionar información útil y relevante. Se integra con servicios de almacenamiento y ETL de Azure para una gestión y procesamiento eficiente de los datos.

## Descripción

La aplicación está diseñada para recolectar datos de páginas web utilizando técnicas de web scraping, activadas a intervalos especificados mediante Azure Functions. Una vez que se obtienen los datos, se cargan a un datalake para su posterior procesamiento, utilizando los servicios de almacenamiento y ETL de Azure.

## Características

- **Web Scraping**: Recolecta datos de sitios web específicos.
- **Triggers Temporales**: Automatiza el proceso de scraping utilizando Azure Functions con triggers programados.
- **Filtrado de Campos**: Selección y procesamiento de los campos relevantes de los datos obtenidos.
- **Integración con Servicios de Azure**: Se integra fácilmente con Azure Blob Storage, Data Lakes y pipelines de ETL para almacenamiento y procesamiento eficientes.
